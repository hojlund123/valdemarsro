from bs4 import BeautifulSoup
import requests
import re
import time

def get_parsed_page(url, delay=0.5):
    # This fixes blocked by cloudflare
    headers = {
        "referer": "https://www.valdemarsro.dk/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    time.sleep(delay)

    return BeautifulSoup(requests.get(url, headers=headers).text, "lxml")

def get_matches():
    matches = get_parsed_page("https://www.valdemarsro.dk/opskrifter/page/1/")
    matches_list = []

    matchdays = matches.find_all("div", {"class": "post-list-item"})

    for match in matchdays:
        matchDetails = match.find_all("span", {"class": "post-list-item-title"})
        
        for getMatch in matchDetails:
        	#datee = match.find({'span': {'class': 'post-list-item-title'}})
            timee = match.find("a")
            print(timee['href'])
            file1 = open("myfile.txt", "a")  # append mod
            file1.write(timee['href'] + "\n")
            file1.close()
    return matches_list
