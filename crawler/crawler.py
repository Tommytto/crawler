from urllib.parse import urlparse
from time import sleep

from django.utils.datastructures import OrderedSet

from html_downloader.downloader import download_html
from links_extractor.links_extractor import extract_links_from_html


class Crawler:
    def __init__(self, settings):
        self.html_downloader = settings["html_downloader"]
        self.links_extractor = settings["links_extractor"]
        self.seed_url = settings["seed_url"]
        self.seed_url_parsed = self.parse_url(self.seed_url)
        self.delay = settings["delay"]

    def crawl(self):
        found_urls = OrderedSet()
        found_urls.add(self.seed_url)
        request_queue = [self.seed_url]

        while len(request_queue) > 0:
            url = request_queue.pop(0)

            print("starting download url", url)
            html = self.html_downloader(url)

            links = self.links_extractor(html, url)
            for link in links:
                if link not in found_urls:
                    found_urls.add(link)

                    if self.same_domain(link):
                        request_queue.append(link)

            # sleep is necessary to not DDOS domain
            sleep(self.delay)

        return {
            "links": list(found_urls)
        }

    def same_domain(self, link):
        return urlparse(link).netloc == self.seed_url_parsed.netloc

    def parse_url(self, link):
        return urlparse(link)


def crawl(seed_url):
    crawler = Crawler({
        "html_downloader": download_html,
        "links_extractor": extract_links_from_html,
        "seed_url": seed_url,
        "delay": 0.5,
    })
    return crawler.crawl()
