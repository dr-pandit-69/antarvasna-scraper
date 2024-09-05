import sqlite3
import os
from data_extractor import extract_elements  # Importing the extraction function
import json
import init_db


# Insert data into the database
def insert_into_db(data):
    conn = sqlite3.connect('comic_data.db')
    cursor = conn.cursor()

    try:
        # Insert the extracted data
        cursor.execute('''
        INSERT INTO comic_data (post_title, english_title, author, date, likes, dislikes, story_content)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (data['post_title'], data['english_title'], data['author'], data['date'], data['likes'], data['dislikes'], data['story_content']))

        conn.commit()
        print(f"Successfully inserted: {data['post_title']}")  # Log successful insertions

    except sqlite3.Error as e:
        print(f"Failed to insert data: {e}")  # Log any database errors
    
    finally:
        conn.close()

# Function to process each URL and insert the extracted data into the database
def process_url(url):
    try:
        # Extract data using the function from data_extractor.py
        extracted_data = extract_elements(url)

        # Insert the extracted data into the database
        if extracted_data:
            insert_into_db(extracted_data)
        else:
            print(f"No data extracted for {url}")

    except Exception as e:
        print(f"Error processing {url}: {e}")  # Log any scraping errors

# Function to load URLs from collected_urls.txt
def load_urls_from_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    else:
        print(f"{file_path} does not exist.")
        return []

def main():
    if not os.path.exists('comic_data.db'):
        init_db.init_db()
 
    urls = load_urls_from_file('collected_urls.txt')

    # Loop through each URL
    for url in urls:
        print(f"Processing {url}...")
        process_url(url)

if __name__ == "__main__":
    main()
