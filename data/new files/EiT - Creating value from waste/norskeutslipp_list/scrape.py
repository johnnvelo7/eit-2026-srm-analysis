import csv
from bs4 import BeautifulSoup


with open("companylist.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")
table = soup.find("table", id="tblListVirksomhet")

if table is None:
    print("Table with id 'tblListVirksomhet' not found.")
else:
    rows = table.find_all("tr")
    data = []
    for row in rows:
        cells = row.find_all(["th", "td"])
        data.append([cell.get_text(strip=True) for cell in cells])

    with open("virksomheter.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(data)

    print(f"Saved {len(data)} rows to virksomheter.csv")
