import requests
from bs4 import BeautifulSoup
import csv
import time

BASE_URL = "https://www.scholarships.com"
FEATURED_URL = f"{BASE_URL}/financial-aid/college-scholarships/featured-scholarships/"

def get_featured_scholarships():
    response = requests.get(FEATURED_URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    cards = soup.select('.card')
    results = []

    for card in cards:
        try:
            name = card.select_one('h3').text.strip()
        except:
            name = "N/A"

        try:
            amount = card.find(text='Amount:').find_next().strip()
        except:
            amount = "N/A"

        try:
            deadline = card.find(text='Deadline:').find_next().strip()
        except:
            deadline = "N/A"

        try:
            link = BASE_URL + card.select_one('a')['href']
        except:
            link = "N/A"

        # Type and Eligibility not available directly; mark placeholder
        type_ = "N/A"
        eligibility = "See link"

        results.append([name, amount, eligibility, deadline, type_, link])
    
    return results

def save_to_csv(data, filename="scholarships.csv"):
    headers = ["Name", "Amount", "Eligibility", "Deadline", "Type", "URL"]
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    data = get_featured_scholarships()
    print(f"Found {len(data)} scholarships.")
    save_to_csv(data)


