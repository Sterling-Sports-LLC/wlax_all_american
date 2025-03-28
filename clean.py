import os
import json

# Paths
INPUT_FOLDER = './parsed'
CLEANED_FOLDER = './cleaned'
REPORT_FILE = './cleaning_report.txt'

# Ensure output folder exists
os.makedirs(CLEANED_FOLDER, exist_ok=True)


POSITION_MAPPING = {
    "A": "Attack",
    "Attack": "Attack",
    "Midfield": "Midfield",
    "Draw Specialist": "Midfield",
    "M": "Midfield",
    "Midfield/DS": "Midfield",
    "Goalkeeper": "Goalkeeper",
    "GK": "Goalkeeper",
    "Attack/DS": "Attack",  # Also represented by A
    "Defender": "Defender",
    "D": "Defender",
    "Attacker": "Attack",
    "Defense": "Defender"
}


CLASS_MAPPING = {
    "Senior": "Senior",
    "Junior": "Junior",
    "Sophomore": "Sophomore",
    "Freshman": "Freshman",
    "Grad": "Graduate Student",
    "Graduate": "Graduate Student",
    "GS": "Graduate Student",
    "Graduate Student":"Graduate Student",
    "Redshirt Senior": "Redshirt Senior",
    "RS-Senior": "Redshirt Senior",
    "RS Senior": "Redshirt Senior",
    "Redshirt Junior": "Redshirt Junior",
    "RS-Junior": "Redshirt Junior",
    "RS Junior": "Redshirt Junior",
    "Junior Redshirt": "Redshirt Junior",
    "Redshirt Sophomore": "Redshirt Sophomore",
    "RS-Sophomore": "Redshirt Sophomore",
    "RS Sophomore": "Redshirt Sophomore",
    "Redshirt Freshman": "Redshirt Freshman",
    "RS Freshman": "Redshirt Freshman",
    "RS-Freshman": "Redshirt Freshman",
    "First-Year": "Redshirt Freshman",
}



# Cleaning report
cleaning_log = []

def clean_data(data, filename):
    """ Cleans player data by standardizing positions and class values. """
    changes = []

    if "teams" not in data or not isinstance(data["teams"], dict):
        print(f"Skipping {filename}: 'teams' key missing or invalid format")
        return data, changes

    for award_name, players in data["teams"].items():
        if not isinstance(players, list):  # Ensure it's a list
            print(f"Skipping {filename} -> {award_name}: Expected a list, got {type(players).__name__}")
            continue

        year = str(data.get("year", "Unknown"))

        for player in players:
            if not isinstance(player, dict):
                print(f"Skipping {filename} -> {award_name}: Expected a dict, got {type(player).__name__}")
                continue

            original_player = player.copy()

            # Standardize string values
            player["name"] = str(player.get("name", "")).strip()
            player["team"] = str(player.get("team", "")).strip() if "team" in player else "Unknown"
            player["class"] = str(player.get("class", "")).strip()
            position = str(player.get("position", "")).strip()

            # Standardize position
            if position in POSITION_MAPPING:
                player["position"] = POSITION_MAPPING[position]
            else:
                player["position"] = "Unknown"
                warning_message = f"Warning: Unexpected position '{position}' in {filename}"
                print(warning_message)
                cleaning_log.append(warning_message)

            # Standardize class values
            if player["class"] in CLASS_MAPPING:
                player["class"] = CLASS_MAPPING[player["class"]]
            else:
                player["class"] = "Unknown"
                warning_message = f"Warning: Unexpected class '{player['class']}' in {filename}"
                print(warning_message)
                cleaning_log.append(warning_message)

            # Add award field based on year and team
            if award_name:
                player["award"] = f"{year} All-American Women's Lacrosse {award_name}"

            # Log changes
            if player != original_player:
                changes.append({
                    "filename": filename,
                    "name": player["name"],
                    "original": original_player,
                    "corrected": player
                })

    return data, changes

# Process files
for filename in os.listdir(INPUT_FOLDER):
    if filename.endswith(".json"):
        input_path = os.path.join(INPUT_FOLDER, filename)
        output_path = os.path.join(CLEANED_FOLDER, filename)

        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        cleaned_data, changes = clean_data(data, filename)

        # Save cleaned data
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(cleaned_data, f, indent=4)

        # Append changes to log
        if changes:
            for change in changes:
                cleaning_log.append(f"File: {change['filename']}, Name: {change['name']}, Changes: {change['original']} -> {change['corrected']}")

# Write cleaning report
if cleaning_log:
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(cleaning_log))

print("Cleaning process completed. Cleaned files are saved in the 'cleaned' folder.")
