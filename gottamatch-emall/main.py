import json
import os
from thefuzz import fuzz, process
from utils import *

# Define file paths
nolli_file = "nolli_points_open.geojson"
osm_file = "osm_node_way_relation.geojson"

# Load Nolli GeoJSON data
with open(nolli_file, "r", encoding="utf-8") as f:
    nolli_data = json.load(f)

# Load OpenStreetMaps (OSM) GeoJSON data
with open(osm_file, "r", encoding="utf-8") as f:
    osm_data = json.load(f)

# Extract relevant names from Nolli points
nolli_features = nolli_data["features"]
nolli_relevant_data = {}

for feature in nolli_features:
    properties = feature.get("properties", {})
    possible_names = [
        properties.get("Nolli Name", ""),
        properties.get("Unravelled Name", ""),
        properties.get("Modern Name", ""),
    ]
    possible_names = [name for name in possible_names if name]  # Remove empty names
    if possible_names:
        nolli_id = feature["properties"]["Nolli Number"]
        # nolli_names[feature["properties"]["Nolli Number"]] = possible_names
        nolli_relevant_data[nolli_id] = {
            "nolli_names": possible_names,
            "nolli_coords": feature["geometry"]
        }


# tot_entries = len(nolli_names.keys())

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
                matches.append((feature_name, best_match, score, 
                                {"osm_coords": feature["geometry"]["coordinates"]}))
                # matches.append((feature, feature_name, best_match, score))
    if len(matches) > 0:
        unique_match = max(matches, key=lambda x: x[2])
        coords2convert = unique_match[-1]["osm_coords"]
        unique_match[-1]["osm_coords"] = extract_coords(coords2convert)
        return  unique_match, 1
    return None, 0

# Perform fuzzy matching for each Nolli point
# matched_results = {}

counter = 0
print(f"Searching best match for Nolli name:")
for nolli_id, values in nolli_relevant_data.items():
    names = values["nolli_names"]
    print(f"\t{nolli_id}\t{names[0]}")
    # matched_results[nolli_id] = []

    features = osm_data.get("features", [])
    
    # Check multiple possible name fields
    for key_field in ["name"]: #, "alt_name", "wikidata", "wikipedia"]:
        match, j = find_best_matches(names, features, key_field, threshold=85)
        counter += j
        nolli_relevant_data[nolli_id]["match"] = match
        
print(f"MATCHED {counter} NOLLY ENTRIES")

# Save results to a JSON file
output_file = "matched_nolli_features.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(nolli_relevant_data, f, indent=2, ensure_ascii=False)

print(f"Matching complete. Results saved to {output_file}.")
