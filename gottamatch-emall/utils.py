import json
import math

def load_data(filename):
    """
    Loads data from a json file
    """
    with open(filename) as file:
        data = json.load(file)

    return data

def extract_coords(data):
    """
    Extracts the first coordinates couple
    from a generic list of coordinates
    """
    if not isinstance(data, list):
        return None

    nested_data = data[0]
    depth = 0
    while isinstance(nested_data, list):
        depth += 1
        nested_data = nested_data[0]

    for i in range(depth):
        data = data[0]

    return data
    

def print_dict(data):
    """
    Outputs a dictionary in a better format
    """
    print(json.dumps(data, indent=2))


def link2map(data):
    """
    Outputs the link to google maps showing the 
    exact coordinates on a map
    """
    coords = data["coordinates"]
    print(f"https://www.google.com/maps/@{coords[1]},{coords[0]},21z")


def calculate_distance(point1, point2):
    """
    Calculates the distance between two points
    """
    dist = math.sqrt((point1[0]-point2[0])**2 +
                     (point1[1]-point2[1])**2)
    
    return dist

def get_nearest(iterable, object):
    index = min(enumerate(iterable), key=lambda x: x[1])[0]
    return object[index]