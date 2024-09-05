import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver():
    chrome_options = Options()
    service = Service(executable_path="driver/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def extract_elements(url):
    driver = setup_driver()

    try:
       
        
        driver.set_window_position(2000, 100)
        driver.minimize_window()
        driver.get(url)
        

    
        scraped_data = {}

        scraped_data['url'] = url

        
        post_title = driver.find_element(By.CLASS_NAME, 'post-title').text.strip()
        scraped_data['post_title'] = post_title

     
        english_title = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/article/header/div[1]/div/h2').text.strip()
        scraped_data['english_title'] = english_title

       
        author = driver.find_element(By.CLASS_NAME, 'meta-author').find_element(By.TAG_NAME, 'a').text.strip()
        scraped_data['author'] = author

       
        meta_date = driver.find_element(By.CLASS_NAME, 'meta-date').text.strip()
        scraped_data['date'] = meta_date

       

       
        likes_section = driver.find_element(By.CLASS_NAME, 'meta-likes').find_elements(By.CLASS_NAME, 'tumbsvotes')
        scraped_data['likes'] = likes_section[1].text.strip()
        scraped_data['dislikes'] = likes_section[0].text.strip()

       
        story_content = driver.find_element(By.CLASS_NAME, 'story-content').find_elements(By.TAG_NAME, 'p')
        story_text = "\n".join([p.text for p in story_content])
        scraped_data['story_content'] = story_text

    except NoSuchElementException:
        try:
            driver.quit()
            driver.get(url)
            driver.set_window_position(2000, 100)
            driver.minimize_window()
            element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "post-title"))
                )
            
            scraped_data = {}

            scraped_data['url'] = url

            
            post_title = driver.find_element(By.CLASS_NAME, 'post-title').text.strip()
            scraped_data['post_title'] = post_title

        
            english_title = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/article/header/div[1]/div/h2').text.strip()
            scraped_data['english_title'] = english_title

        
            author = driver.find_element(By.CLASS_NAME, 'meta-author').find_element(By.TAG_NAME, 'a').text.strip()
            scraped_data['author'] = author

        
            meta_date = driver.find_element(By.CLASS_NAME, 'meta-date').text.strip()
            scraped_data['date'] = meta_date

        

        
            likes_section = driver.find_element(By.CLASS_NAME, 'meta-likes').find_elements(By.CLASS_NAME, 'tumbsvotes')
            scraped_data['likes'] = likes_section[1].text.strip()
            scraped_data['dislikes'] = likes_section[0].text.strip()

        
            story_content = driver.find_element(By.CLASS_NAME, 'story-content').find_elements(By.TAG_NAME, 'p')
            story_text = "\n".join([p.text for p in story_content])
            scraped_data['story_content'] = story_text

        except Exception as e:    
            scraped_data['url'] = url
            scraped_data['post_title'] = 'None'
            scraped_data['english_title'] = 'None'
            scraped_data['author'] = 'None'
            scraped_data['date'] = 'None'
            scraped_data['likes'] = 'None'
            scraped_data['dislikes'] = 'None'
            scraped_data['story_content'] = 'None'
            print(f"Error occurred: {e} at the URL: {url} hence Skipped" )
            driver.quit()
            return scraped_data



        


    except Exception as e:
        print(f"Error occurred: {e}")
    
    finally:
        # Close the driver
        
        driver.quit()
        return scraped_data


