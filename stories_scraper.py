import sqlite3
import os
from data_extractor import extract_elements  # Importing the extraction function
import init_db
from dotenv import load_dotenv
load_dotenv()

# Insert data into the database
def insert_into_db(data):
    conn = sqlite3.connect('comic_data.db')
    cursor = conn.cursor()

    try:
        # Insert the extracted data
        cursor.execute('''
        INSERT INTO comic_data (url, post_title, english_title, author, date, likes, dislikes, story_content)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data['url'], data['post_title'], data['english_title'], data['author'], data['date'], data['likes'], data['dislikes'], data['story_content']))

        conn.commit()
        print(f"Successfully inserted: {data['post_title']}")

    except sqlite3.Error as e:
        print(f"Failed to insert data: {e}")

    finally:
        conn.close()

# Check if URL is already processed (exists in the database)
def is_url_in_db(url):
    conn = sqlite3.connect('comic_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT 1 FROM comic_data WHERE url = ?', (url,))
    result = cursor.fetchone()

    conn.close()

    return result is not None

# Process each URL and insert the extracted data into the database
def process_url(url):
    if is_url_in_db(url):
        print(f"{url} already in the database, skipping...")
        return

    try:
        extracted_data = extract_elements(url)

        if extracted_data:
            insert_into_db(extracted_data)
        else:
            print(f"No data extracted for {url}")

    except Exception as e:
        print(f"Error processing {url}: {e}")

# Load URLs from collected_urls.txt
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

    for url in urls:
        print(f"Processing {url}...")
        process_url(url)

if __name__ == "__main__":
    main()
