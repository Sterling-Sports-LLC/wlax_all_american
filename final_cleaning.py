import os
import json
import pandas as pd

# Paths
input_folder = "merged"
output_folder = "final"
csv_path = "csv/school_mapping.csv"
report_file = "cleaning_report.txt"

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Load school mapping CSV
school_mapping = pd.read_csv(csv_path).fillna('')  # Fill NaN with empty string
mapping_dict = {row["input"].strip(): row["output"].strip() if row["output"] else row["input"].strip()
                for _, row in school_mapping.iterrows()}

# Track unmatched schools for reporting
unmatched_schools = []

# Process JSON files
for filename in os.listdir(input_folder):
    if filename.endswith(".json"):
        file_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            updated = False

            # Iterate through divisions, teams, and players
            for division_data in data.get("divisions", {}).values():
                for team_roster in division_data.get("teams", {}).values():
                    for player in team_roster:
                        school = player.get("team")  # "team" is the school field in input JSON

                        if isinstance(school, str):  # Ensure it's a valid string
                            school = school.strip()

                            if school in mapping_dict:
                                player["team"] = mapping_dict[school]
                            else:
                                unmatched_schools.append(
                                    f"File: {filename} | Player: {player.get('name', 'Unknown')} | Unmatched school: {school}"
                                )

                            updated = True

            # Save cleaned JSON if updated
            if updated:
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4)

        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            print(f"Error reading {filename}: {e}")

# Write cleaning report
if unmatched_schools:
    with open(report_file, "w", encoding="utf-8") as f:
        f.write("Cleaning Report: Unmatched Schools\n\n")
        for log in unmatched_schools:
            f.write(log + "\n")

# Rename 'school' field to 'team' in all output files
for filename in os.listdir(output_folder):
    if filename.endswith(".json"):
        file_path = os.path.join(output_folder, filename)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            updated = False
            for division_data in data.get("divisions", {}).values():
                for team_roster in division_data.get("teams", {}).values():
                    for player in team_roster:
                        if "school" in player:
                            player["team"] = player.pop("school")
                            updated = True
            
            if updated:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            print(f"Error processing {filename}: {e}")

print("Cleaning process completed. Check 'final' folder and 'cleaning_report.txt'.")
