# import os
# import requests

# # === CONFIGURATION ===
# RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "50543b5350msh6045016fe73417cp12ee22jsnc05ce7578b40")
# BASE_URL = "https://jsearch.p.rapidapi.com"

# headers = {
#     "X-RapidAPI-Key": RAPIDAPI_KEY,
#     "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
# }

# def search_jobs(query, location=None, remote=False):
#     """
#     Search jobs using the JSearch API (via RapidAPI).
#     """
#     full_query = query
#     if location:
#         full_query += f" in {location}"
#     params = {
#         "query": query,
#         "page": "1",
#         "num_pages": "1"
#     }

#     if location:
#         params["location"] = location
#     if remote:
#         params["remote_jobs_only"] = "true"

#     try:
#         response = requests.get(f"{BASE_URL}/search", headers=headers, params=params)
#     except requests.RequestException as e:
#         print(f"⚠️ Network error: {e}")
#         return []

#     if response.status_code != 200:
#         print(f"❌ HTTP Error {response.status_code}: {response.text}")
#         return []

#     try:
#         data = response.json()
#     except ValueError:
#         print("⚠️ Failed to parse JSON:", response.text)
#         return []

#     if data.get("status") != "OK":
#         print("⚠️ API Error:", data)
#         return []

#     return data.get("data", [])

import os
import requests
import time

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "50543b5350msh6045016fe73417cp12ee22jsnc05ce7578b40")
BASE_URL = "https://jsearch.p.rapidapi.com"

headers = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
}

def search_jobs(query, location=None, remote=False):
    params = {
        "query": query,
        "num_pages": 1
    }
    if location:
        params["location"] = location
    if remote:
        params["remote_jobs_only"] = "true"

    for attempt in range(3):  # retry up to 3 times
        try:
            response = requests.get(f"{BASE_URL}/search", headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "OK":
                    return data.get("data", [])
                else:
                    print("⚠️ API returned error:", data)
                    return []
            else:
                print(f"❌ HTTP {response.status_code}: {response.text}")
        except Exception as e:
            print("⚠️ Exception:", e)
        time.sleep(1)

    print("❌ Failed after 3 retries.")
    return []
