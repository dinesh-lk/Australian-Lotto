import os, re
import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://www.powerball.net/australia/archive/{}"
OUTPUT_FILE = "powerball_1996_2026.txt"

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

    for year in range(2018, 2027):
        print(f"Scraping year {year}...")

        url = BASE_URL.format(year)
        response = requests.get(url, timeout=15)

        if response.status_code != 200:
            f.write(f"\n===== YEAR {year} FAILED =====\n")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        f.write(f"\n===== YEAR {year} =====\n")

        # 🔥 KEY FIX: select correct containers
        boxes = soup.select("a.archive-box")

        for box in boxes:

            # ---- Extract date + draw ----
            text = box.get_text(" ", strip=True)

            # Example: "May 30th 1996 - Draw 2 › 6 8 15 23 44 5"
            # Split safely
            try:
                date_part = text.split("-")[0].strip()
                # print(text.split("-")[1]).strip()
                # pattern = r'Draw\s+(\d+)'
                # matches = re.findall(pattern, text.split("-")[1].strip())
                # print(matches)
                draw_part = text.split("-")[1].split("›")[0].strip()
            except:
                date_part = text
                draw_part = "Unknown Draw"

            # ---- Extract numbers ----
            balls = box.select("div.ball")
            numbers = [b.get_text(strip=True) for b in balls]

            powerball = box.select_one("div.powerball")
            pb = powerball.get_text(strip=True) if powerball else "?"

            main_numbers = " ".join(numbers)

            # ---- Write line ----
            # f.write(f"{year} | {date_part} | {draw_part} | {main_numbers} | PB {pb}\n")
            f.write(f"{year} | {date_part} | {main_numbers} | PB {pb}\n")

        time.sleep(0.5)

print(f"\nDONE ✅ Saved to {OUTPUT_FILE}")
# os.remove(OUTPUT_FILE)
 

