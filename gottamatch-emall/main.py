import json
from utils import extract_files, load_data, find_best_matches, save_to_json, save_to_geojson

# Define ZIP archive and files to extract
zip_file = "geojson_data.zip"
geojson_files = ["nolli_points_open.geojson", "osm_node_way_relation.geojson"]

# Extract the required files
extracted_files = extract_files(zip_file, geojson_files)

# Define file paths
nolli_file, osm_file = extracted_files

# Load the extracted GeoJSON files
nolli_data = load_data(nolli_file)
osm_data = load_data(osm_file)

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
        nolli_relevant_data[nolli_id] = {
            "nolli_names": possible_names,
            "nolli_coords": feature["geometry"]
        }

# Perform fuzzy matching for each Nolli point
counter = 0
print(f"Searching best match for Nolli names:")

for nolli_id, values in nolli_relevant_data.items():
    names = values["nolli_names"]
    print(f"\t{nolli_id}\t{names[0]}")

    features = osm_data.get("features", [])
    
    match, j = find_best_matches(names, features, key_field="name", threshold=85)#, scorer="partial_ratio")
    counter += j
    nolli_relevant_data[nolli_id]["match"] = match
        
print(f"MATCHED {counter} NOLLY ENTRIES")

# Save results
save_to_json(nolli_relevant_data, "matched_nolli_features.json")
save_to_geojson(nolli_relevant_data, "matched_nolli_features.geojson")

print(f"Matching complete. Results saved.")