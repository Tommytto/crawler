from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

url1 = "https://www.sampleurl.tld"
url2 = "/some/path/here"


def extract_links_from_html(html, original_url):
    soup = BeautifulSoup(html, 'html.parser')
    a_tag = soup.find_all('a', href=True)
    result = []

    for link in a_tag:
        link_url = get_url(link.get('href'), original_url)
        result.append(link_url)

    return result


def get_url(href, original_url):
    url = urlparse(href)
    if url.netloc:
        return href

    return urljoin(original_url, href)
