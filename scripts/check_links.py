"""Read-only HTTP checks for external links from scripts/verify.py."""

import concurrent.futures
import json
from pathlib import Path
from urllib.request import Request, urlopen

OUT = Path(__file__).resolve().parents[1] / "_handoff" / "qa"
urls = json.loads((OUT / "browser-results.json").read_text(encoding="utf-8"))[
    "external_links"
]


def check(url):
    try:
        with urlopen(
            Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=25
        ) as response:
            return {
                "url": url,
                "status": response.status,
                "content_type": response.headers.get("Content-Type"),
            }
    except Exception as error:
        return {"url": url, "error": str(error)}


with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
    results = list(executor.map(check, urls))
(OUT / "link-results.json").write_text(
    json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
)
failed = [r for r in results if r.get("status") != 200]
print(f"{len(results) - len(failed)}/{len(results)} external links return HTTP 200.")
if failed:
    print(json.dumps(failed, ensure_ascii=False))
    raise SystemExit(1)
