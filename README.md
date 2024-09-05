# Antarvasna Scraper

This project is a **web scraper** designed to scrape stories and relevant metadata from the *Antarvasna* website. It uses **Selenium** for web scraping, **Joblib** for parallelization, and stores the scraped data in an **SQLite database**. The scraper is built to be efficient and can handle interruptions & errors by resuming from where it left off.

**Thanks to Shubham Rawat for the idea.**

## Features

- **Parallel Scraping**: The scraper uses Joblib to scrape multiple URLs in parallel, speeding up the process.
- **Resume Mechanism**: If the script is interrupted, it can resume scraping from where it left off.
- **Data Storage**: The scraped data is stored in an SQLite database (`comic_data.db`).
- **URL Tracking**: The script tracks processed URLs using `processed_urls.txt` to ensure the same URL is not scraped multiple times.
- **Error Handling**: Robust error handling for failed scrapes, including retry mechanisms.

## Project Structure

├── data_extractor.py \
**Contains the function to extract data from each webpage**\
├── init_db.py \
**Contains the function to initialize the SQLite database**\
├── stories_scraper_parallel.py \
**Main script for scraping comic stories with parallelization**\
├── stories_scraper.py \
**Main script for scraping comic stories without parallelization**\
├── urlsindex_scraper_parallel.py \
**Main script for scraping URLs stories with parallelization**\
├── urlsindex_scraper.py \
**Main script for scraping comic stories without parallelization**\
├── delete_none.py \
**Deletes the None values in the DB, just in case some random error occurs**\



### Steps to run the Project

1. Clone the repository

```bash
  git clone https://github.com/dr-pandit-69/antarvasna-scraper
  cd antarvasna-scraper
```

2. Create a virtual environment (pipenv is used here)

```bash
pipenv shell
```
4. Install the dependencies

```bash
pip install -r requirements.txt
```
5. Adjust the Environment variables in .env file according to your preference

```bash
PARALLEL_INSTANCES=<Number of cores in your CPU>
PAGES=<Number of Pages you want to scrape from the beginning>
MAX_RETRIES=<maximum Number of retries>
```

5. Run the URLs Scraper first in the virtual environment

If your Computer is fast, run the parallelized script

```bash
python3 urlsindex_scraper_parallel.py
```
If you have a slow computer run this script

```bash
python3 urlsindex_scraper.py
```

After the Scraping is done

6. Now run the Stories scraper file

If your Computer is fast, run the parallelized script

```bash
python3 stories_scraper_parallel.py
```
If you have a slow computer run this script

```bash
python3 stories_scraper.py
```

The final data will be stored in comic_data.db database file


Enjoyyy lol
# Antarvasna Scraper

This project is a **web scraper** designed to scrape stories and relevant metadata from the *Antarvasna* website. It uses **Selenium** for web scraping, **Joblib** for parallelization, and stores the scraped data in an **SQLite database**. The scraper is built to be efficient and can handle interruptions & errors by resuming from where it left off.

**Thanks to Shubham Rawat for the idea.**

## Features

- **Parallel Scraping**: The scraper uses Joblib to scrape multiple URLs in parallel, speeding up the process.
- **Resume Mechanism**: If the script is interrupted, it can resume scraping from where it left off.
- **Data Storage**: The scraped data is stored in an SQLite database (`comic_data.db`).
- **URL Tracking**: The script tracks processed URLs using `processed_urls.txt` to ensure the same URL is not scraped multiple times.
- **Error Handling**: Robust error handling for failed scrapes, including retry mechanisms.

## Project Structure

├── data_extractor.py \
**Contains the function to extract data from each webpage**\
├── init_db.py \
**Contains the function to initialize the SQLite database**\
├── stories_scraper_parallel.py \
**Main script for scraping comic stories with parallelization**\
├── stories_scraper.py \
**Main script for scraping comic stories without parallelization**\
├── urlsindex_scraper_parallel.py \
**Main script for scraping URLs stories with parallelization**\
├── urlsindex_scraper.py \
**Main script for scraping comic stories without parallelization**\
├── delete_none.py \
**Used delete the None values in the DB, just in case something fails in the script**\


### Steps to run the Project

1. Clone the repository

```bash
  git clone https://github.com/dr-pandit-69/antarvasna-scraper
  cd antarvasna-scraper
```

2. Create a virtual environment (pipenv is used here)

```bash
pipenv shell
```
4. Install the dependencies

```bash
pip install -r requirements.txt
```
5. Adjust the Environment variables in .env file according to your preference

```bash
PARALLEL_INSTANCES=<Number of cores in your CPU>
PAGES=<Number of Pages you want to scrape from the beginning>
MAX_RETRIES=<maximum Number of retries>
```

5. Run the URLs Scraper first in the virtual environment

If your Computer is fast, run the parallelized script

```bash
python3 urlsindex_scraper_parallel.py
```
If you have a slow computer run this script

```bash
python3 urlsindex_scraper.py
```

After the Scraping is done

6. Now run the Stories scraper file

If your Computer is fast, run the parallelized script

```bash
python3 stories_scraper_parallel.py
```
If you have a slow computer run this script

```bash
python3 stories_scraper.py
```

The final data will be stored in comic_data.db database file


Enjoyyy lol
