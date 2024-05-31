import sqlite3
import csv

# Path to the CSV file
file_path = "../output/output_2024-05-24_13-05-50.csv"

# Open the CSV file
with open(file_path, mode='r', encoding='utf-8-sig') as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader)  # Skip the header row

    # Connect to SQLite3 database (or create it if it doesn't exist)
    conn = sqlite3.connect('pokemon_etl_project.db')
    cursor = conn.cursor()

    # Create a table based on the CSV header
    create_table_query = """
    CREATE TABLE IF NOT EXISTS pokemon_data (
        name TEXT,
        id INTEGER PRIMARY KEY,
        height INTEGER,
        weight INTEGER,
        base_experience INTEGER,
        types TEXT
    )
    """
    cursor.execute(create_table_query)

    # Insert data into the table
    for row in csv_reader:
        try:
            # Clean the data
            row = [x.strip() for x in row]
            cursor.execute("""
            INSERT INTO pokemon_data (name, id, height, weight, base_experience, types)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (row[0], int(row[1]), int(row[2]), int(row[3]), int(row[4]), row[5]))
        except ValueError as e:
            print(f"Skipping row due to error: {e}")
            continue
        
    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

print("Database created and data inserted successfully.")
