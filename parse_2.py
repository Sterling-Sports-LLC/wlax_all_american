import os
import json
from bs4 import BeautifulSoup

# Directories
RAW_FOLDER = 'raw_2'
PARSED_FOLDER = 'parsed'

# Ensure the parsed folder exists
os.makedirs(PARSED_FOLDER, exist_ok=True)

def parse_html(html):
    """Extracts player data for First Team, Second Team, and Third Team."""
    soup = BeautifulSoup(html, 'html.parser')
    teams = {}
    current_team = None

    for row in soup.find_all('tr'):
        cols = row.find_all('td')

        # If there's a colspan, it's a team name (e.g., "First Team")
        if len(cols) == 1 or (len(cols) > 0 and 'colspan' in cols[0].attrs):
            team_name = cols[0].get_text(strip=True)
            if team_name:  # Ensure it's not an empty row
                current_team = team_name
                teams[current_team] = []  # Initialize team list
            continue  # Skip processing this row as a player

        # Skip empty rows (those that only contain &nbsp;)
        if all(col.get_text(strip=True) == "" for col in cols):
            continue

        # Process player data only if we have a current team and enough columns
        if current_team and len(cols) >= 4:
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
