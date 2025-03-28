import os
import json
import requests
from bs4 import BeautifulSoup
import random

# Define the path for storing raw data
RAW_DATA_PATH = "raw"
os.makedirs(RAW_DATA_PATH, exist_ok=True)

# List of All-American team URLs and their corresponding years and divisions
all_american_urls = [
    ("https://www.iwlca.org/news_article/show/1310756", 2024, 'D1'),
    ("https://www.iwlca.org/news_article/show/1310641", 2024, 'D2'),
    ("https://www.iwlca.org/news_article/show/1310861", 2024, 'D3'),
    ("https://www.iwlca.org/news_article/show/1273961", 2023, 'D1'),
    ("https://www.iwlca.org/news_article/show/1273557", 2023, 'D2'),
    ("https://www.iwlca.org/news_article/show/1273959", 2023, 'D3'),
    ("https://www.iwlca.org/layout_container/show_layout_tab?layout_container_id=103916904&page_node_id=7804888&tab_element_id=309374", 2022, 'D1'),
    ("https://www.iwlca.org/layout_container/show_layout_tab?layout_container_id=103916905&page_node_id=7804888&tab_element_id=309374", 2022, 'D2'),
    ("https://www.iwlca.org/layout_container/show_layout_tab?layout_container_id=103916906&page_node_id=7804888&tab_element_id=309374", 2022, 'D3'),
    ("https://www.iwlca.org/layout_container/show_layout_tab?layout_container_id=80884334&page_node_id=6513867&tab_element_id=256653", 2021, 'D1'),
    ("https://www.iwlca.org/layout_container/show_layout_tab?layout_container_id=80884335&page_node_id=6513867&tab_element_id=256653", 2021, 'D2'),
    ("https://www.iwlca.org/layout_container/show_layout_tab?layout_container_id=80884336&page_node_id=6513867&tab_element_id=256653", 2021, 'D3'),
    ("https://www.iwlca.org/layout_container/show_layout_tab?layout_container_id=58126123&page_node_id=5070357&tab_element_id=197346", 2019, 'D1'),
    ("https://www.iwlca.org/layout_container/show_layout_tab?layout_container_id=58126124&page_node_id=5070357&tab_element_id=197346", 2019, 'D2'),
    ("https://www.iwlca.org/layout_container/show_layout_tab?layout_container_id=58126125&page_node_id=5070357&tab_element_id=197346", 2019, 'D3'),
    ("https://www.iwlca.org/layout_container/show_layout_tab?layout_container_id=45796700&page_node_id=4266591&tab_element_id=157567", 2018, 'D1'),
    ("https://www.iwlca.org/layout_container/show_layout_tab?layout_container_id=45796701&page_node_id=4266591&tab_element_id=157567", 2018, 'D2'),
    ("https://www.iwlca.org/layout_container/show_layout_tab?layout_container_id=45796702&page_node_id=4266591&tab_element_id=157567", 2018, 'D3'),
    ("https://www.iwlca.org/layout_container/show_layout_tab?layout_container_id=33739182&page_node_id=3376261&tab_element_id=113910", 2017, 'D1'),
    ("https://www.iwlca.org/layout_container/show_layout_tab?layout_container_id=33739183&page_node_id=3376261&tab_element_id=113910", 2017, 'D2'),
    ("https://www.iwlca.org/layout_container/show_layout_tab?layout_container_id=33739183&page_node_id=3376261&tab_element_id=113910", 2017, 'D3')
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


   