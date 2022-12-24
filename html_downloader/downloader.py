import requests


def download_html(url):
    r = requests.get(url)

    return r.text
