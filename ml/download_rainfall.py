import os
import requests
from urllib.parse import urlparse, parse_qs

LINKS_FILE = "data/rainfall/download_links.txt"
OUTPUT_DIR = "data/rainfall/2024-07"

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(LINKS_FILE, "r") as f:
    urls = [
        line.strip()
        for line in f
        if "HTTP_services.cgi" in line and "precipitation" in line
    ]

print(f"Found {len(urls)} rainfall files.")

for i, url in enumerate(urls, 1):

    # Get filename from LABEL parameter
    params = parse_qs(urlparse(url).query)
    filename = params.get("LABEL", [None])[0]

    if not filename:
        print(f"[{i}] Could not determine filename")
        continue

    output_path = os.path.join(OUTPUT_DIR, filename)

    if os.path.exists(output_path):
        print(f"[{i}/{len(urls)}] Already exists: {filename}")
        continue

    print(f"[{i}/{len(urls)}] Downloading: {filename}")

    try:
        response = requests.get(url, timeout=120)

        if response.status_code == 200:
            with open(output_path, "wb") as out:
                out.write(response.content)

            print("    ✓ Downloaded")

        else:
            print(f"    ✗ Failed: HTTP {response.status_code}")

    except Exception as e:
        print(f"    ✗ Error: {e}")

print("\n========== DOWNLOAD COMPLETE ==========")
