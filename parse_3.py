import os
import json
from bs4 import BeautifulSoup
import re

# Directories
RAW_FOLDER = 'raw_3'
PARSED_FOLDER = 'parsed'

# Ensure the parsed folder exists
os.makedirs(PARSED_FOLDER, exist_ok=True)

def parse_html(html):
    """Parses the given HTML and extracts All-American teams and players."""
    soup = BeautifulSoup(html, "html.parser")
    teams = {}
    current_team = None

    # Regex patterns
    team_name_pattern = re.compile(r'^(FIRST|SECOND|THIRD|HONORABLE MENTION)\s+TEAM:?$', re.IGNORECASE)
    player_pattern = re.compile(r'^([\w\s\-\'\.]+)[,.]\s+([\w\s&\-]+),\s+([\w\s\-]+),\s+([\w\s\-]+)$')

    for p in soup.find_all("p"):
        text = p.get_text(strip=True)

        # Match team names in different formats
        if team_name_pattern.match(text):
            current_team = text.replace(":", "").title()  # Normalize format
            teams[current_team] = []
        elif current_team and text:
            match = player_pattern.match(text)
            if match:
                name, school, player_class, position = match.groups()
                player_data = {
                    "name": name.strip(),
                    "team": school.strip(),
                    "class": player_class.strip(),
                    "position": position.strip()
                }
                teams[current_team].append(player_data)

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
