"""Local browser checks. Requires playwright and its Chromium browser."""

import json
import runpy
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_handoff" / "qa"
BASE = "http://127.0.0.1:8000/"
VIEWPORTS = [(1440, 1000), (390, 844), (320, 740), (768, 1024)]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    # A failed run must never leave an older success report for check_links.py.
    for name in ["browser-results.json", "link-results.json"]:
        (OUT / name).unlink(missing_ok=True)
    site = runpy.run_path(str(ROOT / "scripts" / "build.py"))
    projects = site["PROJECTS"]
    routes = ["", *(f"projects/{p['slug']}/" for p in projects)]
    expected = {"index.html": site["home"]()}
    expected.update({f"projects/{p['slug']}/index.html": site["detail"](p) for p in projects})
    for path, content in expected.items():
        if not (ROOT / path).is_file() or (ROOT / path).read_text(encoding="utf-8") != content:
            raise SystemExit(f"Generated HTML is out of date: {path}. Run python scripts/build.py first.")
    results = []
    errors = []
    external = set()
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for width, height in VIEWPORTS:
            page = browser.new_page(
                viewport={"width": width, "height": height}, device_scale_factor=1
            )
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.on(
                "console",
                lambda msg: errors.append(msg.text) if msg.type == "error" else None,
            )
            for route in routes:
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
                    if parsed.netloc != urlparse(BASE).netloc:
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
                for zoom in page.locator(".zoom-link").all():
                    zoom.click()
                    assert page.locator("dialog").is_visible()
                    assert page.locator("html").evaluate(
                        '(e)=>getComputedStyle(e).overflow === "hidden"'
                    )
                    bounds = page.locator("dialog").bounding_box()
                    page.mouse.click(bounds["x"] + 2, bounds["y"] + 2)
                    assert page.locator("dialog").is_visible(), "dialog padding must not close it"
                    picture = page.locator("dialog img")
                    picture.evaluate("(img)=>img.decode()")
                    original_width = picture.bounding_box()["width"]
                    page.get_by_role("button", name="2배 확대").click()
                    assert picture.bounding_box()["width"] >= original_width * 1.95
                    page.get_by_role("button", name="화면에 맞추기").click()
                    assert abs(picture.bounding_box()["width"] - original_width) < 2
                    page.keyboard.press("Escape")
                    assert not page.locator("dialog").is_visible()
                    page.wait_for_function(
                        '!document.documentElement.classList.contains("image-open")'
                    )
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
        for project in projects:
            page.goto(BASE)
            page.locator(f'a[href="projects/{project["slug"]}/"]').click()
            assert page.url == urljoin(BASE, f"projects/{project['slug']}/")
            page.reload()
            assert page.locator("h1").inner_text() == project["title"]
            page.go_back()
            assert page.locator("#projects").count() == 1
            if not urlparse(project["demo"]).scheme:
                page.goto(urljoin(BASE, f"projects/{project['slug']}/"))
                # Play the actual linked media; the page itself keeps manual playback.
                page.evaluate(
                    """async src => {
                        const video = document.createElement('video');
                        video.src = src;
                        video.muted = true;
                        document.body.append(video);
                        await video.play();
                    }""",
                    project["demo"],
                )
                page.wait_for_function('document.querySelector("video").currentTime > 0.2')
        pdf = page.request.get(BASE + "assets/resume.pdf")
        assert pdf.status == 200 and pdf.body() == (ROOT / "assets/resume.pdf").read_bytes()
        for route in routes:
            nojs = browser.new_page(
                java_script_enabled=False, viewport={"width": 390, "height": 844}
            )
            nojs.goto(BASE + route)
            assert nojs.locator(".nav-links").is_visible()
            assert nojs.locator("h1").is_visible()
            nojs.close()
        assert not errors, errors
        report = {
            "browser": browser.version,
            "pages": results,
            "console_errors": errors,
            "additional": [
                "all image dialogs + padding click + scroll lock + Escape + focus restore",
                "mobile menu + close after navigation",
                "all detail links + reload + back",
                "PDF HTTP 200 and bytes",
                "no-JS navigation on all routes",
                "local demo playback",
                "generated HTML matches source",
            ],
            "external_links": sorted(external),
        }
        (OUT / "browser-results.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        browser.close()
    print(
        f"PASS: {len(results)} page/viewport combinations; navigation, image zoom, PDF and no-JS checks."
    )


if __name__ == "__main__":
    main()
