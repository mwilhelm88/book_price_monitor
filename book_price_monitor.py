"""
Book Price Monitor
------------------
Scrapes book data from Books to Scrape, stores results in a CSV,
and plots the 10 cheapest books and average price trends over time.
"""

import csv
import requests
from bs4 import BeautifulSoup
from datetime import date
import matplotlib.pyplot as plt
import os
import re
import time

BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"
CSV_FILE = "books.csv"

def scrape_books():
    """
    Scrape all pages of Books to Scrape and return a list of book data.
    Each book includes: title, price, stock, rating, and scrape date.
    """
    books = []
    today = date.today().isoformat()
    page = 1

    while True:
        url = BASE_URL.format(page)
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 404:
                break  # no more pages
            res.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            break

        soup = BeautifulSoup(res.text, "html.parser")
        items = soup.select(".product_pod")
        if not items:
            break

        for item in items:
            title = item.h3.a["title"]
            price_text = item.select_one(".price_color").text.strip()
            price = float(re.search(r"\d+\.\d+", price_text).group())
            stock = item.select_one(".availability").text.strip()
            rating = item.p["class"][1]  # e.g., "Three"

            books.append({
                "title": title,
                "price": price,
                "stock": stock,
                "rating": rating,
                "date": today
            })

        print(f"Scraped page {page} ({len(items)} books)")
        page += 1
        time.sleep(0.5)  # be polite

    return books

def save_to_csv(data, filename=CSV_FILE):
    """
    Save book data to CSV. Appends if file exists, otherwise creates a new file.
    """
    fieldnames = ["title", "price", "stock", "rating", "date"]
    file_exists = os.path.exists(filename)

    with open(filename, "a" if file_exists else "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerows(data)

def plot_cheapest_books(filename=CSV_FILE):
    """
    Plot the top 10 cheapest books from the CSV file.
    """
    books = []
    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            books.append({"title": row["title"], "price": float(row["price"])})

    books_sorted = sorted(books, key=lambda x: x["price"])[:10]

    plt.figure(figsize=(10, 6))
    plt.barh([b["title"] for b in books_sorted], [b["price"] for b in books_sorted], color="skyblue")
    plt.xlabel("Price (£)")
    plt.ylabel("Book Title")
    plt.title("Top 10 Cheapest Books")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()

def plot_price_trends(filename=CSV_FILE):
    """
    Plot the average book price over time from the CSV file.
    """
    price_by_date = {}
    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["price"]:
                date_key = row["date"]
                price_by_date.setdefault(date_key, []).append(float(row["price"]))

    dates = sorted(price_by_date.keys())
    avg_prices = [sum(prices) / len(prices) for prices in (price_by_date[d] for d in dates)]

    plt.figure(figsize=(8, 5))
    plt.plot(dates, avg_prices, marker="o", color="orange")
    plt.xlabel("Date")
    plt.ylabel("Average Price (£)")
    plt.title("Average Book Price Over Time")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def run_tracker():
    """
    Run the scraper, save data, and generate plots.
    """
    print("Scraping book data...")
    new_data = scrape_books()
    save_to_csv(new_data)
    print(f"Saved {len(new_data)} books to {CSV_FILE}")
    plot_cheapest_books()
    plot_price_trends()

if __name__ == "__main__":
    run_tracker()