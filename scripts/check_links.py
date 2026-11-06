"""Read-only HTTP checks for external links from scripts/verify.py."""

import concurrent.futures
import json
from pathlib import Path
from urllib.request import Request, urlopen

OUT = Path(__file__).resolve().parents[1] / "_handoff" / "qa"


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


def main():
    (OUT / "link-results.json").unlink(missing_ok=True)
    report_path = OUT / "browser-results.json"
    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
        urls = report["external_links"]
        if (
            not isinstance(urls, list)
            or not urls
            or not all(
                isinstance(url, str) and url.startswith(("https://", "http://"))
                for url in urls
            )
        ):
            raise ValueError("external_links must be a nonempty HTTP URL list")
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise SystemExit(
            f"Run python scripts/verify.py successfully first: {error}"
        ) from error
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        results = list(executor.map(check, urls))
    (OUT / "link-results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    failed = [r for r in results if r.get("status") != 200]
    print(
        f"{len(results) - len(failed)}/{len(results)} external links return HTTP 200."
    )
    if failed:
        print(json.dumps(failed, ensure_ascii=False))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
