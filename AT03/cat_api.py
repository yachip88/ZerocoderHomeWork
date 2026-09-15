import requests

CAT_API_URL = "https://api.thecatapi.com/v1/images/search"


def get_random_cat_image():
    try:
        response = requests.get(CAT_API_URL, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data[0]["url"]
        return None
    except Exception:
        return None
