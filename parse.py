import os
import json
from bs4 import BeautifulSoup

# Directories
RAW_FOLDER = 'raw'
PARSED_FOLDER = 'parsed'

# Ensure the parsed folder exists
os.makedirs(PARSED_FOLDER, exist_ok=True)

def parse_html(html):
    """Extracts player data for First Team, Second Team, and Third Team."""
    soup = BeautifulSoup(html, 'html.parser')
    teams = {"First Team": [], "Second Team": [], "Third Team": []}
    
    current_team = None
    skip_empty_rows = True  # Flag to skip the initial empty rows
    
    for tag in soup.find_all(['p', 'table']):
        text = tag.get_text(strip=True)
        
        if "First Team" in text:
            current_team = "First Team"
        elif "Second Team" in text:
            current_team = "Second Team"
        elif "Third Team" in text:
            current_team = "Third Team"
        
        # Process only the table rows once the header section is done
        if tag.name == 'table' and current_team:
            for row in tag.find_all('tr'):
                cols = row.find_all('td')
                
                # Skip rows that are likely the table header or empty rows
                if skip_empty_rows and len(cols) < 4:
                    continue  # Skip these rows
                
                # Once we have valid data, stop skipping
                skip_empty_rows = False
                
                # Check if there are enough columns to process
                if len(cols) >= 4:
                    player = {
                        "name": f"{cols[0].get_text(strip=True)} {cols[1].get_text(strip=True)}",
                        "team": cols[2].get_text(strip=True),
                        "class": cols[3].get_text(strip=True),
                        "position": cols[4].get_text(strip=True) if len(cols) > 4 else "",
                    }
                    teams[current_team].append(player)
    
    return teams

# Process each JSON file in the raw folder
for filename in os.listdir(RAW_FOLDER):
    if filename.endswith('.json'):
        file_path = os.path.join(RAW_FOLDER, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        year = data.get("year")
        division = data.get("division")
        html = data.get("html", "")
        
        parsed_data = {
            "year": year,
            "division": division,
            "teams": parse_html(html)
        }
        
        output_file = os.path.join(PARSED_FOLDER, f"all_american_{year}_{division}.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(parsed_data, f, indent=4)

print("Parsing complete. JSON files saved in the 'parsed' folder.")
