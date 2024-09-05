from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import chromedriver_handler
import os
from dotenv import load_dotenv

load_dotenv()
PROCESSED_URLS_FILE = os.getenv('PROCESSED_URLS_FILE', 'processed_urls.txt')
COLLECTED_URLS_FILE = os.getenv('COLLECTED_URLS_FILE', 'collected_urls.txt')

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-minimized")
    service = Service(executable_path="driver/chromedriver.exe")
    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def scrape_page(url):
    driver = setup_driver()
    driver.get(url)

    print(f"Scraping: {url}")


    links = []

  
    content_div = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div')
    article_links = content_div.find_elements(By.XPATH, './/section/article/div/header/a')

    for link in article_links:
        href = link.get_attribute('href')
        links.append(href)
        print(href)


    driver.quit()

    return links


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
    else:
        processed_urls = []
    return processed_urls


def main():
 
    base_url = "https://www.antarvasna3.com/page/"
    urls = [f"{base_url}{i}/" for i in range(1, int(os.getenv('PAGES', 10)))] 

  
    processed_urls = load_processed_urls()

   
    urls_to_scrape = [url for url in urls if url not in processed_urls]

    print(f"Resuming scraping from {len(processed_urls)} processed URLs. {len(urls_to_scrape)} URLs remaining.")

    
    for url in urls_to_scrape:
        links = scrape_page(url)
        if links:
         
            save_collected_urls(links)
           
            save_processed_url(url)

    print(f"Scraping completed.")

if __name__ == "__main__":
    
    
    chromedriver_handler.setup_chromedriver()

    main()
