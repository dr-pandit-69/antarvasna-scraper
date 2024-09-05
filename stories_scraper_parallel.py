import sqlite3
import os
from data_extractor import extract_elements  # Importing the extraction function
from joblib import Parallel, delayed
import init_db
import chromedriver_handler


chromedriver_handler.setup_chromedriver()

MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
PARALLEL_INSTANCES=int(os.getenv('PARALLEL_INSTANCES', 4))

def insert_into_db(data):
    conn = sqlite3.connect('comic_data.db')
    cursor = conn.cursor()

    try:
       
        cursor.execute('''
        INSERT INTO comic_data (url,post_title, english_title, author, date, likes, dislikes, story_content)
        VALUES (?,?, ?, ?, ?, ?, ?, ?)
        ''', (data['url'],data['post_title'], data['english_title'], data['author'], data['date'], data['likes'], data['dislikes'], data['story_content']))

        conn.commit()
        print(f"Successfully inserted: {data['post_title']}")

    except sqlite3.Error as e:
        print(f"Failed to insert data: {e}") 

    finally:
        conn.close()


def process_url(url):
    try:
     
        extracted_data = extract_elements(url)

       
        if extracted_data:
            return extracted_data
        else:
            print(f"No data extracted for {url}")
            return None

    except Exception as e:
        print(f"Error processing {url}: {e}")  
        return None


def load_urls_from_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    else:
        print(f"{file_path} does not exist.")
        return []

def is_url_in_db(url):
    conn = sqlite3.connect('comic_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT 1 FROM comic_data WHERE url = ?', (url,))
    result = cursor.fetchone()

    conn.close()

    return result is not None




def sub_main(urls):
    num_cores = PARALLEL_INSTANCES  
    scraped_data_list = Parallel(n_jobs=num_cores)(delayed(process_url)(url) for url in urls)

    for data in scraped_data_list:
        if data and not is_url_in_db(data['url']): 
            insert_into_db(data)




def main():
    
    if not os.path.exists('comic_data.db'):
        init_db.init_db()
    
   
    urls = load_urls_from_file('collected_urls.txt')
    

    for i in range(0, len(urls), PARALLEL_INSTANCES):
        urls_to_process = urls[i:i + PARALLEL_INSTANCES]
        for url in urls[i:i + PARALLEL_INSTANCES]:
            if is_url_in_db(url):
                print(f"{url} already in the database")
                urls_to_process.remove(url)

        if(urls_to_process):
          sub_main(urls[i:i + PARALLEL_INSTANCES])
          print(i+PARALLEL_INSTANCES, "urls processed")
        else:
          print("No new urls to process hence skipped", i+PARALLEL_INSTANCES)  
    

  
    

if __name__ == "__main__":
    main()
