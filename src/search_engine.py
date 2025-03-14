import requests
from typing import List, Dict

def search_engine(query: str, latitude: float = 41.387917, longitude: float = 2.1699187) -> List[Dict]:
    """
    Queries the Wallapop API with the provided query and returns a list of dictionaries.
    Each dictionary contains the 'title' and 'description' of a search result.
    """
    url = "https://api.wallapop.com/api/v3/search"
    params = {
        "source": "search_box",
        "keywords": query,
        "latitude": latitude,
        "longitude": longitude
    }
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "es,it-IT;q=0.9,it;q=0.8,en-US;q=0.7,en;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "DeviceOS": "0",
        "MPID": "-5589673199823489972",
        "Origin": "https://es.wallapop.com",
        "Pragma": "no-cache",
        "Referer": "https://es.wallapop.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "X-AppVersion": "84230",
        "X-DeviceID": "b80b8c1a-a846-4392-9223-eeb4c77c67bb",
        "X-DeviceOS": "0",
        "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"'
    }
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()

    results = []
    items = data.get("data", {}).get("section", {}).get("payload", {}).get("items", [])
    for item in items:
        title = item.get("title", "")
        description = item.get("description", "")
        results.append({"title": title, "description": description})
    return results
