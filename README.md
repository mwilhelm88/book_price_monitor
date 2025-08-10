# Book Price Monitor

A Python project that scrapes book data from [Books to Scrape](http://books.toscrape.com), 
stores it in a CSV file, and visualizes price trends with matplotlib.

## Features
- Scrapes all pages from Books to Scrape
- Saves book data (title, price, stock, rating, date) to CSV
- Plots:
  - **Top 10 cheapest books**
  - **Average book price over time**

## Requirements
Install dependencies with:
```bash
pip install -r requirements.txt