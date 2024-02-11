# Climate Neutral Certification Analysis

This repository analyzes carbon offset purchases by Climate Neutral certified companies. The data was scraped around September 2023, and includes offset purchases from the year 2022.

![The output graph from this repository](/data/demo.png)

## Setup

Dependencies are captured in the `Pipfile`.

```bash
# From the top of the repository:
pipenv install --dev
```

## Usage

### Scraping Brands

First, run `scrape_brands.py` to get a list of Climate Neutral certified companies.

Unfortunately, you'll need to manually download each page of HTML from the company
directory, since pagination via code doesn't seem to work. See the script for details.

### Parsing

Next, run `scrape_offsets.py` to gather information about each company's offset purchases.

### Visualization

See `results.ipynb` for plotting results.