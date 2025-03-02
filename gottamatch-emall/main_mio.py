import json
import os
from thefuzz import fuzz, process

# Define file paths
nolli_file = "nolli_points_open.geojson"
geojson_files = "osm_node_way_relation.geojson"

# Load Nolli data
with open(nolli_file, "r", encoding="utf-8") as f:
    nolli_data = json.load(f)

# Load other GeoJSON data
with open(geojson_files, "r", encoding="utf-8") as f:
    geojson_data = json.load(f)

# Extract relevant names from Nolli points
nolli_features = nolli_data["features"]
nolli_names = {}

for feature in nolli_features:
    properties = feature.get("properties", {})
    possible_names = [
        properties.get("Nolli Name", ""),
        properties.get("Unravelled Name", ""),
        properties.get("Modern Name", ""),
    ]
    possible_names = [name for name in possible_names if name]  # Remove empty names
    if possible_names:
        nolli_names[feature["properties"]["Nolli Number"]] = possible_names

tot_entries = len(nolli_names.keys())

# Function to perform fuzzy search
def find_best_matches(search_names, features, key_field="name", threshold=80):
    if 'n/a' in search_names:
        search_names.remove('n/a')
    matches = []
    for feature in features:
        properties = feature.get("properties", {})
        if key_field in properties:
            feature_name = properties[key_field]
            best_match, score = process.extractOne(feature_name, search_names, scorer=fuzz.ratio)
            if score >= threshold:
                matches.append((feature_name, best_match, score))
                # matches.append((feature, feature_name, best_match, score))
    if len(matches) > 0:
        return  [max(matches, key=lambda x: x[-1])], 1
    return matches, 0

# Perform fuzzy matching for each Nolli point
matched_results = {}

counter = 0
print(f"Searching best match for Nolli name:")
for nolli_id, names in nolli_names.items():
    print(f"\t{nolli_id}\t{names[0]}")
    matched_results[nolli_id] = []

    features = geojson_data.get("features", [])

    # Check multiple possible name fields
    #for key_field in ["name"]: #, "alt_name", "wikidata", "wikipedia"]:
    key_field = "name"
    matches, j = find_best_matches(names, features, key_field, threshold=85)
    counter += j
    if matches:
        matched_results[nolli_id].extend([(key_field, match) for match in matches])

print(f"MATCHED {counter} NOLLY ENTRY OUT OF {tot_entries} EXISTENT ENTRIES")

# Save results to a JSON file
output_file = "matched_nolli_features.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(matched_results, f, indent=2, ensure_ascii=False)

print(f"Matching complete. Results saved to {output_file}.")
