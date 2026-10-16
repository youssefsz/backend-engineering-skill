"""Optional network-only reachability check; never update source review dates."""

import concurrent.futures
import shutil
import subprocess
from urllib.parse import urlsplit

from validate import ROOT, markdown_body, markdown_links, markdown_paths


def check(url):
    command = [
        "curl", "--fail", "--location", "--silent", "--show-error",
        "--proto", "=https", "--proto-redir", "=https", "--max-time", "30",
        "--output", "/dev/null", "--write-out", "%{http_code} %{url_effective}",
        "--", url,
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=35)
        return url, result.returncode == 0, (result.stdout + " " + result.stderr).strip()
    except subprocess.TimeoutExpired:
        return url, False, "check exceeded 35 seconds"


def main():
    if not shutil.which("curl"):
        raise SystemExit("curl is required only for this optional network check")
    urls = sorted({
        href.split("#", 1)[0]
        for path in markdown_paths(ROOT)
        for href in markdown_links(markdown_body(path))
        if urlsplit(href).scheme == "https"
    })
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(check, urls))
    for url, passed, detail in results:
        print(f"{'REACHABLE' if passed else 'REVIEW'} {url}: {detail}")
    failures = sum(not passed for _, passed, _ in results)
    print(f"Checked {len(results)} URLs; {failures} need review. Reachability does not establish content support or version applicability.")
    return bool(failures)


if __name__ == "__main__":
    raise SystemExit(main())
