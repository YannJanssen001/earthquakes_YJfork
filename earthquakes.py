# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests
import json


def get_data(use_local_file=False, save_to_file=False):
    """
    Get earthquake data from API or local file.
    
    Args:
        use_local_file (bool): If True, load from local earthquake_data.json file
        save_to_file (bool): If True, save the API response to earthquake_data.json
    """
    filename = "earthquake_data.json"
    
    if use_local_file:
        # Load from local file
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            print("Loaded data from local file")
            return data
        except FileNotFoundError:
            print(f"Local file {filename} not found. Fetching from API...")
    
    # Fetch from API
    print("Fetching data from API...")
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc"}
    )

    # Parse the JSON response
    data = json.loads(response.text)
    
    # Optionally save to file
    if save_to_file:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Data saved to {filename}")
    
    return data

def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    return len(data["features"])


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake["properties"]["mag"]


def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    # There are three coordinates, but we don't care about the third (altitude)
    return earthquake["geometry"]["coordinates"][1], earthquake["geometry"]["coordinates"][0]


def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    max_earthquake = max(data["features"], key=get_magnitude)
    return get_magnitude(max_earthquake), get_location(max_earthquake)


# With all the above functions defined, we can now call them and get the result
# Get some data and explore it

# First time: fetch from API and save to file
# After saving: load from local file (much faster!)
data = get_data(use_local_file=True, save_to_file=False)
first_earthquake = data["features"][0]

# Print the structure to see what's available
print("Properties:", list(first_earthquake["properties"].keys()))
print("Geometry:", list(first_earthquake["geometry"].keys()))


print(f"Loaded {count_earthquakes(data)}")
max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")