import json
from utils import extract_files, load_data, find_best_matches, save_to_json, save_to_geojson

# Define ZIP archive and files to extract
zip_file = "geojson_data.zip"
geojson_files = ["nolli_points_open.geojson", "osm_node_way_relation.geojson"]

# Extract the required files
nolli_file, osm_file = extract_files(zip_file, geojson_files)

# TODO
# Load the extracted GeoJSON files
#
# nolli_data = # load the data using utils functions
# osm_data = # load the data using utils functions

# TODO
# Extract Nolli features and initialize 
# dictionary to put data in
#
# nolli_features = 
# nolli_relevant_data = {}

# TODO
# create a smaller dictionary with the following
# structure for each Nolli feature
# 
# "1319": {
# "nolli_names": [
#   "Mole Adriana, or Castel S. Angelo",
#   "Mole Adriana, or Castel Sant'Angelo",
#   "Castel Sant'Angelo"
# ],
# "nolli_coords": {
#   "type": "Point",
#   "coordinates": [
#     12.46670095,
#     41.90329709
#   ]
# }
# for feature in nolli_features: # Start from here

# TODO
# Perform fuzzy matching for each Nolli point
# use the appropriate function you find in utils
# print(f"Searching best match for Nolli names:")
#
# for nolli_id, values in nolli_relevant_data.items():
#
#   Do some operation on data
#
#   Call function to obtain best match for each entry
#   in the Nolli map   
#
#   match = 
#   Put data in dictionary
#   nolli_relevant_data[nolli_id]["match"] = match

# Save results
save_to_json(nolli_relevant_data, "matched_nolli_features.json")
save_to_geojson(nolli_relevant_data, "matched_nolli_features.geojson")

print(f"Matching complete. Results saved.")
