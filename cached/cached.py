import requests
import time
import functools
from cachetools import cached, TTLCache

@cached(cache=TTLCache(maxsize=1024, ttl=2))
# @functools.cache
def fetch_data_from_api(location):
    # Simulate API request delay
    time.sleep(1)

    # Replace this with actual API call to fetch JSON data
    api_url = f'http://127.0.0.1:8000/weather/{location}'
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# First call
start_time = time.time()
result_1 = fetch_data_from_api("Copenhagen")
end_time = time.time()
print(f"Data processing result (First call): {result_1}, Time taken: {end_time - start_time:.6f} seconds")

# Simulate passing of some time
time.sleep(5)

# Second call - pass the same argument again (cached result)
start_time = time.time()
result_2 = fetch_data_from_api("Copenhagen")
end_time = time.time()
print(f"Data processing result (Second call with caching): {result_2}, Time taken: {end_time - start_time:.6f} seconds")
