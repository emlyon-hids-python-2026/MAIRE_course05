# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Download the `medicstore` dataset into ../data/.

Copy this file into your project folder and run:

    MacOS / Linux:
    cd scripts && uv run download_data.py && cd ..

    Windows:
    cd scripts ; uv run download_data.py ; cd ..

Files are saved to `../data/` (relative to this script) and overwritten if
they already exist. Only the Python standard library is used.
"""

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

OWNER = "emlyon-hids-python-2026"
REPO = "course_dataset"
BRANCH = "main"
FOLDER = "medicstore"

DEST = Path(__file__).resolve().parent.parent / "data"
API_URL = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{FOLDER}?ref={BRANCH}"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "download_data.py"})
    with urllib.request.urlopen(req) as resp:
        return resp.read()


def main():
    try:
        entries = json.loads(fetch(API_URL))
        files = [e for e in entries if e["type"] == "file"]
        DEST.mkdir(parents=True, exist_ok=True)
        print(f"Downloading {len(files)} files to {DEST}")
        for entry in files:
            target = DEST / entry["name"]
            target.write_bytes(fetch(entry["download_url"]))
            print(f"  {entry['name']} ({target.stat().st_size:,} bytes)")
    except urllib.error.HTTPError as e:
        sys.exit(f"Download failed: HTTP {e.code} for {e.url}")
    except urllib.error.URLError as e:
        sys.exit(f"Network error: {e.reason}")
    print("Done.")


if __name__ == "__main__":
    main()
