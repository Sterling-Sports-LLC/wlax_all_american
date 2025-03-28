import os
import json

# Folder containing the JSON files
FOLDER = "final"
OUTPUT_FILE = "unique_values.txt"

# Sets to store unique values
unique_schools = set()
unique_classes = set()
unique_positions = set()

# Process each JSON file
for filename in os.listdir(FOLDER):
    if filename.endswith(".json"):
        file_path = os.path.join(FOLDER, filename)
        
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        for division in data.get("divisions", {}).values():
            for team, players in division.get("teams", {}).items():
                for player in players:
                    unique_schools.add(player["school"].strip())
                    unique_classes.add(player["class"].strip())
                    unique_positions.add(player["position"].strip())

# Write the unique values to a file
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("Unique Schools:\n")
    f.write("\n".join(sorted(unique_schools)) + "\n\n")
    
    f.write("Unique Classes:\n")
    f.write("\n".join(sorted(unique_classes)) + "\n\n")
    
    f.write("Unique Positions:\n")
    f.write("\n".join(sorted(unique_positions)) + "\n\n")

print(f"Unique values saved to {OUTPUT_FILE}")