
import re
import time
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://australia.national-lottery.com/oz-lotto/results-archive-{}"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

with open("ozlotto_results.txt", "w", encoding="utf-8") as outfile:

    for year in range(2026, 2021, -1):

        print(f"Downloading {year}...")

        response = requests.get(BASE_URL.format(year), headers=HEADERS)

        if response.status_code != 200:
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.find("table")

        if table is None:
            continue

        rows = table.find_all("tr")[1:]

        for row in rows:

            cols = row.find_all("td")

            if len(cols) < 3:
                continue

            # Draw information
            draw_text = cols[0].get_text(" ", strip=True)

            match = re.search(r"Draw\s+(\d+)", draw_text)
            draw_number = match.group(1) if match else ""

            draw_date = draw_text.replace(f"Draw {draw_number}", "").strip()

            # Numbers
            numbers = [
                int(li.get_text(strip=True))
                for li in cols[1].find_all("li")
            ]

            if len(numbers) == 8:
                main = numbers[:6]
                supp = numbers[6:]
            elif len(numbers) == 9:
                main = numbers[:7]
                supp = numbers[7:]
            elif len(numbers) == 10:
                main = numbers[:7]
                supp = numbers[7:]
            else:
                main = numbers
                supp = []

            # Each number occupies two spaces
            main_str = " ".join(f"{n:2d}" for n in main)
            supp_str = " ".join(f"{n:2d}" for n in supp)

            outfile.write(
                f"{year} | {draw_date:<22} | {main_str:<20} | {supp_str}\n"
            )

        time.sleep(1)

print("Finished.")

