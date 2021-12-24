from bs4 import BeautifulSoup
import requests
from csv import writer
import csv
import urllib
import os.path
import json
import datetime

dailynews_links = {
    "Dawn": "https://www.dawn.com/feeds/home",
    "The News Intl": "https://www.thenews.com.pk/rss/1/1",
    "Tribune": "https://tribune.com.pk/feed/home",
}


def dailynews_scraper(dict_of_links):
    potential_links = []

    for site, link in dict_of_links.items():
        res = requests.get(link)
        soup = BeautifulSoup(res.content, features="xml")
        parsed_url = urllib.parse.urlparse(link)
        base_url = f"{parsed_url[0]}://{parsed_url[1]}"
        list_of_links = soup.findAll("item")
        for item in list_of_links:
            try:
                if "http" in item.link.text:
                    potential_links.append(
                        {
                            "news agency": site,
                            "title": item.title.text.strip().split("\n")[0],
                            "link": item.link.text,
                        }
                    )
                else:
                    relative_path = item.link.text
                    complete_url = f"{base_url}{relative_path}"
                    potential_links.append(
                        {
                            "news agency": site,
                            "title": item.title.text.strip().split("\n")[0],
                            "link": complete_url,
                        }
                    )
            except:
                print("Error Found!")
    return potential_links


def dailylist_to_csvs(scraper_results):
    if not (os.path.isfile("all_daily_results.csv")):
        with open("all_daily_results.csv", "w", newline="") as csv_file:
            csv_writer = csv.DictWriter(
                csv_file, fieldnames=["news agency", "title", "link"]
            )
            csv_writer.writeheader()

    oldlinks = []
    oldlinks2 = []
    with open("all_daily_results.csv", "r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            oldlinks.append(row["link"])
            oldlinks2.append(row["link"])

    with open("new_daily_results.csv", "w", encoding="utf-8", newline="") as csv_file:
        csv_writer = csv.DictWriter(
            csv_file, fieldnames=["news agency", "title", "link"]
        )
        csv_writer.writeheader()
        for result in scraper_results:
            if result["link"] not in oldlinks:
                csv_writer.writerow(result)
                oldlinks.append(result["link"])

    with open("all_daily_results.csv", "a+", encoding="utf-8", newline="") as csv_file:
        csv_writer = csv.DictWriter(
            csv_file, fieldnames=["news agency", "title", "link"]
        )
        for result in scraper_results:
            if result["link"] not in oldlinks2:
                csv_writer.writerow(result)
                oldlinks2.append(result["link"])


dailyresults = dailynews_scraper(dailynews_links)
dailylist_to_csvs(dailyresults)
