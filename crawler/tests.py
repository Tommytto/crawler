from django.test import TestCase

from html_downloader.downloader import download_html

from .crawler import Crawler, crawl
from links_extractor.links_extractor import extract_links_from_html


# Create your tests here.
class CrawlerTestCase(TestCase):
    def test_crawl(self):
        links_info = [
            ["https://example.com", ["https://example.com/2"]],
            ["https://example.com/2", ["https://example.com/3", "test"]],
            ["https://example.com/3", ["https://example.com", "https://google.com"]],
        ]

        expected_result = [
            "https://example.com",
            "https://example.com/2",
            "https://example.com/3",
            "https://example.com/test",
            "https://google.com"
        ]

        crawler = Crawler({
            "html_downloader": get_download_html_mock(links_info),
            "links_extractor": extract_links_from_html,
            "seed_url": 'https://example.com',
            "delay": 0,
        })
        result = crawler.crawl()
        self.assertListEqual(result["links"], expected_result)

    def test_bad_url(self):
        try:
            crawl("bad url")
        except Exception:
            pass


def get_download_html_mock(pages):
    response_map = {}
    for page in pages:
        html = ""
        page_url = page[0]
        page_child_links = page[1]
        for link in page_child_links:
            html += "<a href=\"{}\"></a>".format(link)
        response_map[page_url] = html

    def download_html_mock(url):
        return response_map.get(url, "")

    return download_html_mock
