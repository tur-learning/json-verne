# HINT: You'll likely need to import the same utility functions we used before.
# from utils import extract_files, load_data, find_best_matches, save_to_json, save_to_geojson

###############################
# 1) Define the input files
###############################
# HINT: You have a ZIP file containing GeoJSON files to process.
# zip_file = "geojson_data.zip"
# geojson_files = ["nolli_points_open.geojson", "osm_node_way_relation.geojson"]

###############################
# 2) Extract GeoJSON files
###############################
# HINT: Use the utils function `extract_files(zip_file, geojson_files)` to extract 
#       the required GeoJSON files from the ZIP archive.
#       This function returns a list of extracted file paths.

# extracted_files = ...

# HINT: You can destructure them like this (if they always come in a certain order):
# nolli_file, osm_file = extracted_files

###############################
# 3) Load the GeoJSON data
###############################
# HINT: Use the utils function `load_data(filename)` to read the JSON content of each file.

# nolli_data = ...
# osm_data = ...

###############################
# 4) Extract relevant info from Nolli data
###############################
# HINT: The top-level structure of the loaded GeoJSON looks like:
# {
#   "type": "FeatureCollection",
#   "features": [
#       {
#           "type": "Feature",
#           "geometry": {...},
#           "properties": {...}
#       },
#       ...
#   ]
# }
# 
# For each feature, you can gather necessary attributes:
#  - Unique Nolli ID (e.g., "properties"]["Nolli Number"])
#  - Potential names from different fields (e.g., "Nolli Name", "Unravelled Name", "Modern Name")
#  - Geometry object (to store or compare coordinates)
#
# HINT: Store the extracted information in a dictionary, e.g.:
# nolli_relevant_data = {
#   nolli_id: {
#       "nolli_names": [...],   # list of possible names
#       "nolli_coords": {...},  # the geometry from the nolli feature
#       # "match": None         # place to store matched OSM info (later)
#   },
#   ...
# }

# nolli_relevant_data = {}
# nolli_features = nolli_data["features"]
# for feature in nolli_features:
#     properties = feature.get("properties", {})
#     # 1) Extract the unique nolli_id
#     # 2) Extract possible names (list)
#     # 3) Extract geometry
#     # 4) Store them in nolli_relevant_data

###############################
# 5) Fuzzy match with OSM data
###############################
# HINT: The OSM data is also a FeatureCollection. 
#       Each feature might have "properties" with a "name" field.
#       We'll attempt to fuzzy match each Nolli name to the OSM "name".
#
# HINT: Use the utils function `find_best_matches(search_names, features, key_field="name", threshold=85, ...)`
#       to find the best OSM feature match for each set of Nolli names.
#       - search_names: the list of Nolli potential names
#       - features: the "features" from OSM data
#       - key_field: "name" (default), or another property
#       - threshold: 85 (for example)
#
# This function returns:
#   (best_match, count)
# where best_match might look like:
#   ("OSM name found", "Nolli name used for match", similarity_score, {"osm_coords": [lng, lat]})
# 
# HINT: Store this match in the nolli_relevant_data dictionary under "match".

# for nolli_id, values in nolli_relevant_data.items():
#     possible_names = values["nolli_names"]
#     match_result, match_count = find_best_matches(possible_names, osm_data["features"], ...)
#     values["match"] = match_result
#     # Keep track of how many matches you found if you want.

###############################
# 6) Save to JSON and GeoJSON
###############################
# HINT: Use `save_to_json(data, "matched_nolli_features.json")` 
#       to store your final dictionary structure in a JSON file.
#
# HINT: The structure of nolli_relevant_data might look like:
# {
#   "123": {
#       "nolli_names": ["San Giovanni", "Chiesa di S. Giovanni", ...],
#       "nolli_coords": {
#           "type": "Point",
#           "coordinates": [12.500, 41.900]
#       },
#       "match": ("Chiesa di San Giovanni", "Chiesa di S. Giovanni", 90, {"osm_coords": [12.501, 41.901]})
#   },
#   ...
# }
#
# HINT: Then use `save_to_geojson(data, "matched_nolli_features.geojson")`
#       to convert each matched item to a valid GeoJSON FeatureCollection.
#
# The `save_to_geojson` function will look for:
#   item["match"] -> best match tuple
#   item["nolli_names"] (first name used for "Nolli_Name")
#   item["nolli_coords"]
#   etc.

# save_to_json(nolli_relevant_data, "matched_nolli_features.json")
# save_to_geojson(nolli_relevant_data, "matched_nolli_features.geojson")

###############################
# 7) Visualization
###############################
# HINT: Finally, you can upload the generated "matched_nolli_features.geojson" 
#       to [geojson.io](http://geojson.io/) to visualize your matched points.
#
# TIP: Evaluate how well they match and if the coordinates line up on the map!
