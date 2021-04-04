import requests

def download_media(url):
    return requests.get(url, allow_redirects=True).content