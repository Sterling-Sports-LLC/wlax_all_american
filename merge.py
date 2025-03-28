import os
import json
from collections import defaultdict

# Paths
INPUT_FOLDER = './cleaned'
FINAL_FOLDER = './merged'

# Ensure output folder exists
os.makedirs(FINAL_FOLDER, exist_ok=True)

# Dictionary to store merged data by year
merged_data = defaultdict(lambda: {"year": None, "divisions": {}})

# Process each file in the cleaned folder
for filename in os.listdir(INPUT_FOLDER):
    if filename.endswith(".json"):
        file_path = os.path.join(INPUT_FOLDER, filename)

        # Load JSON data
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        year = data.get("year")
        division = data.get("division")
        teams = data.get("teams")

        if not year or not division or not teams:
            print(f"Skipping {filename} due to missing year, division, or teams")
            continue

        # Initialize year entry if not exists
        merged_data[year]["year"] = year

        # Merge divisions
        if division not in merged_data[year]["divisions"]:
            merged_data[year]["divisions"][division] = {"division": division, "teams": {}}

        # Merge teams within the division
        for team_name, players in teams.items():
            if team_name not in merged_data[year]["divisions"][division]["teams"]:
                merged_data[year]["divisions"][division]["teams"][team_name] = []
            
            merged_data[year]["divisions"][division]["teams"][team_name].extend(players)

# Save merged files
for year, data in merged_data.items():
    output_filename = f"all_american_{year}.json"
    output_path = os.path.join(FINAL_FOLDER, output_filename)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

print("Merging complete. Files saved in the 'merged' folder.")
