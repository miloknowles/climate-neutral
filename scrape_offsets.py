import pandas as pd
import requests
from bs4 import BeautifulSoup


def main():
  """
  Retrieve offset purchasing statistics for each company.

  Input
  -----
  You'll need to generate `data/brands.csv` first, using the `scrape_brands.py` script.

  Output
  ------
  Generates the `data/results.csv` file.
  """
  df = pd.read_csv("data/brands.csv")

  results = []
  for i in range(len(df)):
    data = dict()

    # The `pathname` column has a URL to scrape for each company.
    pathname = df.iloc[i].pathname
    data["url"] = pathname

    res = requests.get(pathname)
    print("Scraping company:", pathname, "STATUS", res.status_code)

    soup = BeautifulSoup(res.text)
    metrics_emissions = soup.find("div", class_="metrics-wrapper")

    name = soup.find("p", class_="p-bold w-condition-invisible").text
    data["name"] = name

    try:
      # Scope 1,2,3
      scopes_p = metrics_emissions.find_all("p", class_="p-sm-bold")
      data["scope_1"] = float(scopes_p[0].text.replace("tCO2e", "").replace(" ", "").replace(",", ""))
      data["scope_2"] = float(scopes_p[1].text.replace("tCO2e", "").replace(" ", "").replace(",", ""))
      data["scope_3"] = float(scopes_p[2].text.replace("tCO2e", "").replace(" ", "").replace(",", ""))

      # Offset Expenditure
      search = "Total Expenditures in Carbon Credits"
      metrics_offsets = soup.find("div", class_="metrics-group_compensate")
      total_expenditures = metrics_offsets.find_all(lambda tag: tag.name == "p" and search in tag.text)[0]\
        .find_parent().find_parent().find("p", class_="p-sm-bold")
      data["total_offset_expenditure"] = float(total_expenditures.text.replace("$", "").replace(" ", "").replace(",", ""))

      total_offsets = metrics_offsets.find_all(lambda tag: tag.name == "div" and "Emissions Offset" in tag.text)[0]\
        .find_parent().find_parent().find("h4", class_="heading-no-margin")
      data["total_offsets_tons_co2"] = float(total_offsets.text.replace("tCO2e", "").replace(" ", "").replace(",", ""))

      print(data)
      results.append(data)
    
    # NOTE(milo): Some companies are missing data - just skip them for now.
    except:
      print("FAIL!", pathname)
      continue

  out = pd.DataFrame(results)
  out.set_index("name", inplace=True)
  out.to_csv("data/results.csv")


if __name__ == "__main__":
  main()