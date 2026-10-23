"""Local browser checks. Requires playwright and its Chromium browser."""

import json
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_handoff" / "qa"
OUT.mkdir(parents=True, exist_ok=True)
BASE = "http://127.0.0.1:8000/"
ROUTES = [
    "",
    "projects/smart-fan/",
    "projects/smart-recycling/",
    "projects/smart-monitoring/",
]
results = []
errors = []
external = set()
with sync_playwright() as pw:
    browser = pw.chromium.launch()
    for width, height in [(1440, 1000), (390, 844), (320, 740), (768, 1024)]:
        page = browser.new_page(
            viewport={"width": width, "height": height}, device_scale_factor=1
        )
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on(
            "console",
            lambda msg: errors.append(msg.text) if msg.type == "error" else None,
        )
        for route in ROUTES:
            response = page.goto(BASE + route, wait_until="networkidle")
            assert response.status == 200
            for img in page.locator("img[src]").all():
                img.scroll_into_view_if_needed()
                img.evaluate("(img)=>img.decode()")
            page.evaluate("window.scrollTo(0,0)")
            page.wait_for_timeout(250)
            assert page.locator("h1").count() == 1
            assert page.evaluate(
                "document.documentElement.scrollWidth <= window.innerWidth"
            ), (route, width, "overflow")
            assert page.locator("img[src]").evaluate_all(
                "(imgs)=>imgs.every(i=>i.complete && i.naturalWidth>0)"
            ), (route, "broken image")
            for anchor in page.locator("a[href]").all():
                href = anchor.get_attribute("href")
                url = urljoin(BASE + route, href)
                parsed = urlparse(url)
                if parsed.scheme == "mailto":
                    assert parsed.path == "yp0504@naver.com"
                    continue
                if parsed.netloc != "127.0.0.1:8000":
                    external.add(url)
                    continue
                path = ROOT / unquote(parsed.path.lstrip("/"))
                if path.is_dir():
                    path = path / "index.html"
                assert path.exists(), ("missing", path)
                if parsed.fragment:
                    assert f'id="{parsed.fragment}"' in path.read_text(
                        encoding="utf-8"
                    ), ("anchor missing", url)
            if width in [1440, 390]:
                slug = route.strip("/").replace("/", "-") or "home"
                page.screenshot(path=str(OUT / f"{slug}-{width}.png"), full_page=True)
            zoom = page.locator(".zoom-link").first
            zoom.click()
            assert page.locator("dialog").is_visible()
            picture = page.locator("dialog img")
            picture.evaluate("(img)=>img.decode()")
            original_width = picture.bounding_box()["width"]
            page.get_by_role("button", name="2배 확대").click()
            assert picture.bounding_box()["width"] >= original_width * 1.95
            page.get_by_role("button", name="화면에 맞추기").click()
            assert abs(picture.bounding_box()["width"] - original_width) < 2
            page.keyboard.press("Escape")
            assert not page.locator("dialog").is_visible()
            assert zoom.evaluate("(e)=>e===document.activeElement")
            if width < 620:
                menu = page.get_by_role("button", name="메뉴")
                menu.click()
                assert menu.get_attribute("aria-expanded") == "true"
                page.locator(".nav-links a").first.click()
                assert menu.get_attribute("aria-expanded") == "false"
            results.append({"route": route or "/", "width": width, "status": "pass"})
        page.close()
    page = browser.new_page()
    page.goto(BASE)
    page.locator('a[href="projects/smart-fan/"]').click()
    assert "/projects/smart-fan/" in page.url
    page.reload()
    assert page.locator("h1").inner_text() == "Jetson Smart Fan Controller"
    page.go_back()
    assert page.locator("#projects").count() == 1
    pdf = page.request.get(BASE + "assets/resume.pdf")
    assert pdf.status == 200 and pdf.body() == (ROOT / "assets/resume.pdf").read_bytes()
    nojs = browser.new_page(
        java_script_enabled=False, viewport={"width": 390, "height": 844}
    )
    nojs.goto(BASE)
    assert nojs.locator(".nav-links").is_visible()
    assert nojs.locator("h1").is_visible()
    nojs.close()
    assert not errors, errors
    report = {
        "browser": browser.version,
        "pages": results,
        "console_errors": errors,
        "additional": [
            "image dialog + Escape + focus restore",
            "mobile menu + close after navigation",
            "detail link + reload + back",
            "PDF HTTP 200 and bytes",
            "no-JS navigation",
        ],
        "external_links": sorted(external),
    }
    (OUT / "browser-results.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    browser.close()
print(
    "PASS: 16 page/viewport combinations; navigation, image zoom, PDF and no-JS checks."
)
