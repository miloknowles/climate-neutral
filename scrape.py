from bs4 import BeautifulSoup
import requests
import pandas as pd
import glob

url = "https://www.climateneutral.org/certified-brands"
brand_urls = set([])

html_files = glob.glob("data/html/*.html")

# pagination doesn't work
# for page in range(0, 1):
for filename in html_files:
  with open(filename, "r") as f:
    html = f.read()

  print(filename)
  # print(f"Scraping page {page}")
  # res = requests.get(f"{url}{'?page={page}' if page > 0 else ''}")
  # print(res.status_code)
    # soup = BeautifulSoup(res.text)

  soup = BeautifulSoup(html)

  container_class = "brands-list_collection-wrapper"

  item = soup.find("div", class_=container_class)
  brands = item.find_all("div", class_="brand-item-container")

  for b in brands:
    a = b.find("a", class_="brand-item", href=True)
    brand_urls.add(a["href"])

  print(f"Found {len(brand_urls)} brands so far")

print(brand_urls)

df = pd.DataFrame({
  "pathname": sorted(list(brand_urls))
})

df.to_csv("data/brands.csv", index=False)