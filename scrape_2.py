import os
import json
import requests
from bs4 import BeautifulSoup
import random

# Define the path for storing raw data
RAW_DATA_PATH = "raw_2"
os.makedirs(RAW_DATA_PATH, exist_ok=True)

# List of All-American team URLs and their corresponding years and divisions
all_american_urls = [
    ("https://www.iwlca.org/layout_container/show_layout_tab?layout_container_id=24526874&page_node_id=2623080&tab_element_id=84513", 2016, 'D1'),
    ("https://www.iwlca.org/layout_container/show_layout_tab?layout_container_id=24526875&page_node_id=2623080&tab_element_id=84513", 2016, 'D2'),
    ("https://www.iwlca.org/layout_container/show_layout_tab?layout_container_id=24526876&page_node_id=2623080&tab_element_id=84513", 2016, 'D3')
   ]


# List of user-agents to simulate different browsers
USER_AGENTS_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0"
]

# Function to scrape and save data
def scrape_all_american(url, year, division):
    headers = {"User-Agent": random.choice(USER_AGENTS_LIST)}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Ensure we raise an error for bad responses
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Store the entire HTML as a string
        data = {"year": year, "division": division, "html": str(soup)}
        
        # Format filename properly
        file_name = f"all_american_{year}_{division}.json"
        file_path = os.path.join(RAW_DATA_PATH, file_name)
        
        # Save data to a JSON file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"Data for {year} ({division}) saved to {file_path}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data for {year} ({division}). Error: {e}")

# Iterate through the list and scrape each URL
for url, year, division in all_american_urls:
    print(f"Scraping All-American team data for {year} ({division})...")
    scrape_all_american(url, year, division)

print("Scraping completed!")