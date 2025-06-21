from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv

URL = "https://www.salliemae.com/scholarships/scholly?level_of_study=College+Junior&page=1"

def get_soup_with_selenium(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # run without opening a browser window
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(5)  # wait for JS to load
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    return soup

def scrape_sallie_scholly():
    soup = get_soup_with_selenium(URL)
    cards = soup.select(".search-result__card")
    results = []

    for card in cards:
        try:
            name = card.select_one(".search-result__card-title").text.strip()
        except:
            name = "N/A"

        try:
            amount = card.select_one(".search-result__card-amount").text.strip()
        except:
            amount = "N/A"

        try:
            deadline = card.select_one(".search-result__card-deadline").text.strip()
        except:
            deadline = "N/A"

        try:
            description = card.select_one(".search-result__card-summary").text.strip()
        except:
            description = "N/A"

        try:
            link = "https://www.salliemae.com" + card.select_one("a")["href"]
        except:
            link = "N/A"

        type_ = "N/A"

        results.append([name, amount, description, deadline, type_, link])

    return results

def save_to_csv(data, filename="sallie_scholarships.csv"):
    headers = ["Name", "Amount", "Eligibility", "Deadline", "Type", "URL"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)
    print(f" Saved {len(data)} scholarships to {filename}")

if __name__ == "__main__":
    data = scrape_sallie_scholly()
    save_to_csv(data)
