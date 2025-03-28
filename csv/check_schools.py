import csv

# File paths
all_american_file = "csv/all_american_schools.txt"
mapping_file = "csv/school_mapping.csv"
output_file = "csv/comparison_results.txt"

# Read all American schools from text file
with open(all_american_file, "r", encoding="utf-8") as f:
    all_american_schools = {line.strip() for line in f if line.strip()}

# Read only the first column (abbreviations) from CSV
mapped_schools = set()
with open(mapping_file, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader, None)  # Skip header if it exists
    for row in reader:
        if row:  # Ensure row is not empty
            mapped_schools.add(row[0].strip())  # Only consider the first column

# Find schools not in the first column of the mapping CSV
missing_schools = sorted(all_american_schools - mapped_schools)

# Save results to a text file
with open(output_file, "w", encoding="utf-8") as f:
    if missing_schools:
        f.write("Schools in all_american_school.txt missing from school_mapping.csv:\n")
        for school in missing_schools:
            f.write(school + "\n")
    else:
        f.write("All schools in all_american_school.txt are accounted for in school_mapping.csv.")

print(f"Comparison complete. Results saved to {output_file}.")
