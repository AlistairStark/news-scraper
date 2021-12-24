from bs4 import BeautifulSoup
import requests
from csv import writer
import csv
import urllib
import os.path
import json
import datetime

globalnews_links = {
    "NY Times": "https://www.nytimes.com/section/world/asia",
    "WashPost": "https://www.washingtonpost.com/world/asia-pacific/?itid=nb_hp_world_asia-pacific",
    "WashPost1": "https://www.washingtonpost.com/global-opinions/?itid=sf_opinions_subnav",
    "WashPost2": "https://www.washingtonpost.com/opinions/?itid=sf_global-opinions_subnav",
    "BBC": "https://www.bbc.com/news/world/asia",
    "BBC1": "https://www.bbc.com/news",
    "BBC2": "https://www.bbc.com/news/reality_check",
    "CBC": "https://www.cbc.ca/news/world",
    "CBC1": "https://www.cbc.ca/news/opinion",
    "CBC2": "https://www.cbc.ca/news",
    "Globe & Mail": "https://www.theglobeandmail.com/",
    "Globe & Mail1": "https://www.theglobeandmail.com/world/",
    "Globe & Mail 2": "https://www.theglobeandmail.com/opinion/",
    "Aljazeera": "https://www.aljazeera.com/topics/regions/asia.html",
    "Reuters": "https://www.reuters.com/world",
    "Reuters Asia": "https://www.reuters.com/world/asia-pacific",
    "Gulf News": "https://gulfnews.com/",
    "Guardian": "https://www.theguardian.com/international",
    "Modern Diplomacy": "https://moderndiplomacy.eu/",
    "The Diplomat": "https://thediplomat.com/",
    "Aljazeera 2": "https://www.aljazeera.com/",
    "Aljazeera 3": "https://www.aljazeera.com/opinion/",
    "Toronto Star": "https://www.thestar.com/news/world/asia.html",
}
globalnews_terms = [
    "pakistan",
    "Pakistan",
    "Pak",
    "pak",
    "Qureshi",
    "qureshi",
    "Khan",
    "khan",
    "Bajwa",
    "bajwa",
    "Kashmir",
    "kashmir",
    "Islamabad",
    "islamabad",
    "Karachi",
    "karachi",
    "Lahore",
    "lahore",
    "Rawalpindi",
    "rawalpindi",
    "Peshawar",
    "peshawar",
    "Multan",
    "multan",
    "Faisalabad",
    "faisalabad",
    "quetta",
    "Quetta",
    "Hyderabad",
    "hyderabad",
    "Sindh",
    "sindh",
    "Gujaranwala",
    "gujanwala",
    "Durand Line",
    "durand line",
    "Balochistan",
    "balochistan",
    "Khyber Pakhtunkhwa",
    "khyber pakhtunkhwa",
    "Punjab",
    "punjab",
    "gilgit-baltistan",
    "Gilgit-Baltistan",
    "gilgit baltistan",
    "Gilgit Baltistan",
]


def globalnews_scraper(dict_of_links, search_terms):
    potential_links = []
    for site, link in dict_of_links.items():
        res = requests.get(link)

        parsed_url = urllib.parse.urlparse(link)
        base_url = f"{parsed_url[0]}://{parsed_url[1]}"

        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            list_of_links = soup.select("a")
            for item in list_of_links:
                if any(term in item.text for term in search_terms):
                    if "http" in item["href"]:
                        potential_links.append(
                            {
                                "news agency": site,
                                "title": item.text.strip().split("\n")[0],
                                "link": item["href"],
                            }
                        )
                    else:
                        relative_path = item["href"]
                        complete_url = f"{base_url}{relative_path}"
                        potential_links.append(
                            {
                                "news agency": site,
                                "title": item.text.strip().split("\n")[0],
                                "link": complete_url,
                            }
                        )
        else:
            print(f"Error {res.status_code}: {link}")

    return potential_links


def globallist_to_csvs(scraper_results):
    if not (os.path.isfile("all_global_results.csv")):
        with open("all_global_results.csv", "w", newline="") as csv_file:
            csv_writer = csv.DictWriter(
                csv_file, fieldnames=["news agency", "title", "link"]
            )
            csv_writer.writeheader()

    oldlinks = []
    oldlinks2 = []
    with open("all_global_results.csv", "r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            oldlinks.append(row["link"])
            oldlinks2.append(row["link"])

    with open("new_global_results.csv", "w", encoding="utf-8", newline="") as csv_file:
        csv_writer = csv.DictWriter(
            csv_file, fieldnames=["news agency", "title", "link"]
        )
        csv_writer.writeheader()
        for result in scraper_results:
            if result["link"] not in oldlinks:
                csv_writer.writerow(result)
                oldlinks.append(result["link"])

    with open("all_global_results.csv", "a+", encoding="utf-8", newline="") as csv_file:
        csv_writer = csv.DictWriter(
            csv_file, fieldnames=["news agency", "title", "link"]
        )
        for result in scraper_results:
            if result["link"] not in oldlinks2:
                csv_writer.writerow(result)
                oldlinks2.append(result["link"])


globalresults = globalnews_scraper(globalnews_links, globalnews_terms)
globallist_to_csvs(globalresults)
