import sqlite3

# Connect to the SQLite3 database
conn = sqlite3.connect('pokemon_etl_project.db')
cursor = conn.cursor()

# Query to select all data from the pokemon_data table
query = "SELECT * FROM pokemon_data"

# Execute the query
cursor.execute(query)

# Fetch all rows from the executed query
rows = cursor.fetchall()

# Print the column headers
column_names = [description[0] for description in cursor.description]
print(column_names)

# Print each row
for row in rows:
    print(row)

# Close the connection
conn.close()
