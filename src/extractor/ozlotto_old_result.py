import csv
import re
import time
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://australia.national-lottery.com/oz-lotto/results-archive-{}"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

with open("ozlotto_results.csv", "w", newline="", encoding="utf-8") as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "Year",
        "Draw",
        "Date",
        "Main Numbers",
        "Supplementary Numbers",
        "Total Winners"
    ])

    for year in range(2026, 2021, -1):

        print(f"Downloading {year}...")

        url = BASE_URL.format(year)

        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            print(f"Failed: {year}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.find("table")

        if table is None:
            print(f"No table found for {year}")
            continue

        rows = table.find_all("tr")[1:]

        for row in rows:

            cols = row.find_all("td")

            if len(cols) < 3:
                continue

            # ------------------------
            # Draw number and date
            # ------------------------
            draw_text = cols[0].get_text(" ", strip=True)

            match = re.search(r"Draw\s+(\d+)", draw_text)

            draw_number = match.group(1) if match else ""

            draw_date = draw_text.replace(f"Draw {draw_number}", "").strip()

            # ------------------------
            # Numbers
            # ------------------------
            numbers = [
                int(li.get_text(strip=True))
                for li in cols[1].find_all("li")
            ]

            if len(numbers) == 8:
                # 6 main + 2 supplementary
                main = numbers[:6]
                supp = numbers[6:]

            elif len(numbers) == 9:
                # 7 main + 2 supplementary
                main = numbers[:7]
                supp = numbers[7:]

            elif len(numbers) == 10:
                # 7 main + 3 supplementary
                main = numbers[:7]
                supp = numbers[7:]

            else:
                main = numbers
                supp = []

            winners = cols[2].get_text(strip=True).replace(",", "")

            writer.writerow([
                year,
                draw_number,
                draw_date,
                ",".join(map(str, main)),
                ",".join(map(str, supp)),
                winners
            ])

        time.sleep(1)

print("Finished.")



