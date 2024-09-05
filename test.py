import os



MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
PARALLEL_INSTANCES=int(os.getenv('PARALLEL_INSTANCES', 4))
PROCESSED_URLS_FILE = os.getenv('PROCESSED_URLS_FILE', 'processed_urls.txt')
COLLECTED_URLS_FILE = os.getenv('COLLECTED_URLS_FILE', 'collected_urls.txt')

print(type(MAX_RETRIES))