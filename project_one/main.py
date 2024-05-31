import requests
import csv
import os
from datetime import datetime

# Create the output directory if it doesn't exist
output_dir = 'output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# URL of the Pokémon API
url = "https://pokeapi.co/api/v2/pokemon?limit=10"

# Make a GET request to fetch the raw JSON data
response = requests.get(url)
if response.status_code != 200:
    raise Exception("Error fetching data from the API")

# Parse the JSON response
data = response.json()

# Extract the results list which contains the Pokémon data
pokemon_list = data['results']

# Create a list to store the Pokémon data
pokemon_data = []

# Fetch detailed data for each Pokémon
for pokemon in pokemon_list:
    pokemon_details_response = requests.get(pokemon['url'])
    if pokemon_details_response.status_code != 200:
        continue  # Skip this Pokémon if there's an issue with the request

    pokemon_details = pokemon_details_response.json()
    pokemon_data.append({
        "name": pokemon['name'],
        "id": pokemon_details['id'],
        "height": pokemon_details['height'],
        "weight": pokemon_details['weight'],
        "base_experience": pokemon_details['base_experience'],
        "types": ", ".join([t['type']['name'] for t in pokemon_details['types']])
    })

# Get the current date and time
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Specify the CSV file to write the data to
csv_file = os.path.join(output_dir, f'output_{current_time}.csv')

# Specify the header for the CSV file
fieldnames = ["name", "id", "height", "weight", "base_experience", "types"]

# Write data to CSV
with open(csv_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()

    # Write the Pokémon data
    for pokemon in pokemon_data:
        writer.writerow(pokemon)

print(f"Data has been successfully exported to {csv_file}")
