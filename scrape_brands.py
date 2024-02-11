from bs4 import BeautifulSoup
import pandas as pd
import glob


def main():
  """
  Scrapes a list of brands from the Climate Neutral website, and writes to a CSV.

  Input
  -----
  Unfortunately, I found that iterating over pages via their API didn't seem to
  work. The same list of 100 companies were returned each time, despite changing
  the `page` argument.

  Instead, I had to go through the pages of their company listings myself, and
  download the raw HTML of the page.

  You can see brands here:
  https://www.climateneutral.org/certified-brands


  Output
  ------
  Generates the `data/brands.csv` file.
  """
  brand_urls = set([])
  html_files = glob.glob("data/html/*.html")

  for filename in html_files:
    with open(filename, "r") as f:
      html = f.read()

    print("Parsing:", filename)
    soup = BeautifulSoup(html)

    container_class = "brands-list_collection-wrapper"

    item = soup.find("div", class_=container_class)
    brands = item.find_all("div", class_="brand-item-container")

    for b in brands:
      a = b.find("a", class_="brand-item", href=True)
      brand_urls.add(a["href"])

    print(f"Found {len(brand_urls)} brands so far")

  for url in brand_urls:
    print(url)

  df = pd.DataFrame({
    "pathname": sorted(list(brand_urls))
  })

  df.to_csv("data/brands.csv", index=False)


if __name__ == "__main__":
  main()