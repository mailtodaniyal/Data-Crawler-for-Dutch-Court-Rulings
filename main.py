import time
import json
import csv
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://uitspraken.rechtspraak.nl/"
DETAIL_URL = "https://uitspraken.rechtspraak.nl/#!/details?id="
OUTPUT_CSV = "court_rulings.csv"
OUTPUT_JSON = "court_rulings.json"
TOTAL_CASES = 1000

options = Options()
options.headless = True
service = Service("chromedriver")

driver = webdriver.Chrome(service=service, options=options)
driver.get(BASE_URL)
time.sleep(5)

def get_case_details(ecli):
    case_url = DETAIL_URL + ecli
    driver.get(case_url)
    time.sleep(3)
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    try:
        title = soup.find("h1").text.strip()
        date = soup.find("span", class_="publication-date").text.strip()
        court_name = soup.find("div", class_="metadata").find_all("span")[1].text.strip()
        full_text = soup.find("div", class_="ruling-text").text.strip()
    except:
        return None
    
    return {
        "ECLI Number": ecli,
        "Date": date,
        "Court Name": court_name,
        "Title": title,
        "Full Text": full_text
    }

case_list = []
ecli_seen = set()
while len(case_list) < TOTAL_CASES:
    soup = BeautifulSoup(driver.page_source, "html.parser")
    links = soup.find_all("a", href=True)
    
    for link in links:
        if "ECLI:" in link["href"] and len(case_list) < TOTAL_CASES:
            ecli = link["href"].split("id=")[-1]
            if ecli not in ecli_seen:
                case_data = get_case_details(ecli)
                if case_data:
                    case_list.append(case_data)
                    ecli_seen.add(ecli)
                    print(f"Scraped {len(case_list)} cases so far...")

    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
    time.sleep(3)

driver.quit()

df = pd.DataFrame(case_list)
df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(case_list, f, ensure_ascii=False, indent=4)

print(f"Scraping complete! Data saved to {OUTPUT_CSV} and {OUTPUT_JSON}")
