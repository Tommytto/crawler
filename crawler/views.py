from django.shortcuts import render
from .crawler import crawl


def index(request):
    return render(request, "crawler/index.html")


def search(request):
    url = request.POST['url']
    crawl_result = crawl(url)
    return render(request, "crawler/index.html", {
        "links": crawl_result["links"],
        "url": url
    })
