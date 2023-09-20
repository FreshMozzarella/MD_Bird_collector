import requests

def fetch_bird_calls_from_xenocanto():
    url = 'https://xeno-canto.org/api/2/recordings?query=cnt:"united+states"+loc:maryland&page=1'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return data['recordings']
    except requests.RequestException as e:
        # Handle any kind of request exception (timeout, connectivity, etc.)
        print(f"Error fetching data from xeno-canto: {e}")
        return []

def fetch_image_from_inaturalist(bird_name, access_token):
    base_url = "https://api.inaturalist.org/v1/observations"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "q": bird_name,
        "photo": True,
        "per_page": 1
    }
    
    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        if data['results'] and data['results'][0]['photos']:
            return data['results'][0]['photos'][0]['url']
    except requests.RequestException as e:
        print(f"Error fetching image from iNaturalist: {e}")

    return None
