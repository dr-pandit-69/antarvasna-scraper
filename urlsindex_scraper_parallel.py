from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from joblib import Parallel, delayed
import chromedriver_handler
import random
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

load_dotenv()

chromedriver_handler.setup_chromedriver()


MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
PARALLEL_INSTANCES=int(os.getenv('PARALLEL_INSTANCES', 4))
PROCESSED_URLS_FILE = os.getenv('PROCESSED_URLS_FILE', 'processed_urls.txt')
COLLECTED_URLS_FILE = os.getenv('COLLECTED_URLS_FILE', 'collected_urls.txt')


def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-minimized")
    
    
    service = Service(executable_path="driver/chromedriver.exe")

    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def scrape_page(url, retries=0):
    driver = None
    links = []
    
    try:
        driver = setup_driver()
        driver.minimize_window()
        driver.get(url)
        content_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div'))
        )

        print(f"Scraping: {url}")

       
        content_div = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div')
        article_links = content_div.find_elements(By.XPATH, './/section/article/div/header/a')

        for link in article_links:
            href = link.get_attribute('href')
            links.append(href)
            print(href)

        time.sleep(random.uniform(2, 5))

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        
       
        if retries < MAX_RETRIES:
            print(f"Retrying {url} (attempt {retries + 1})...")
            time.sleep(random.uniform(4,5)) 
            return scrape_page(url, retries + 1)
        else:
            print(f"Failed to scrape {url} after {MAX_RETRIES} retries. Logging failed page.")
            return None, url 
    
    finally:
        if driver:
            driver.quit()  

    return links, None 


def save_processed_url(url):
    with open(PROCESSED_URLS_FILE, 'a') as f:
        f.write(f"{url}\n")

def save_collected_urls(links):
    with open(COLLECTED_URLS_FILE, 'a') as f:  
        for link in links:
            f.write(f"{link}\n")


def load_processed_urls():
    if os.path.exists(PROCESSED_URLS_FILE):
        with open(PROCESSED_URLS_FILE, 'r') as f:
            processed_urls = f.read().splitlines()
            processed_urls.sort()
    else:
        processed_urls = []
    return processed_urls


def process_url(url):
    links, failed_page = scrape_page(url)
    
    if links:
        
        save_processed_url(url)
        
        save_collected_urls(links)
    
    return links, failed_page


def main():

    base_url = "https://www.antarvasna3.com/page/"
    urls = [f"{base_url}{i}/" for i in range(1, int(os.getenv('PAGES', 10)))]  

    
    processed_urls = load_processed_urls()

  
    urls_to_scrape = [url for url in urls if url not in processed_urls]

    print(f"Resuming scraping from {len(processed_urls)} processed URLs. {len(urls_to_scrape)} URLs remaining.")

 
    failed_pages = []

    
    results = Parallel(n_jobs=PARALLEL_INSTANCES)(delayed(process_url)(url) for url in urls_to_scrape)

    
    all_links = []
    for links, failed_page in results:
        if links:
            all_links.extend(links)
        if failed_page:
            failed_pages.append(failed_page)


    with open('parallel_scraped_story_links.txt', 'a') as file:  
        for link in all_links:
            file.write(f"{link}\n")
    print(f"Links saved to parallel_scraped_story_links.txt")

   
    if failed_pages:
        with open('failed_pages.txt', 'a') as file: 
            for page in failed_pages:
                file.write(f"{page}\n")
        print(f"Failed pages saved to failed_pages.txt")

if __name__ == "__main__":
    main()
