"""Scrapy library import"""
import scrapy
from scrapy.crawler import CrawlerProcess


SHARED_CSS_SELECTOR = (
    "body >"
    + "div.logged-out.env-production.page-responsive >"
    + "div.application-main >"
    + "main >"
    + "div.position-relative.container-lg.p-responsive.pt-6 >"
    + "div >"
    + "div:nth-child(2) >"
    + "article:nth-child(1) >"
    + "h2 >"
    + "a::attr(href)"
)


class GitHubTrendingPythonSpider(scrapy.Spider):
    """Spider for daily trending Python repositories"""

    name = "GitHubTrendingSpider"
    start_urls = ["https://github.com/trending/python?since=daily"]

    def parse(self, response):
        for repo in response.css(SHARED_CSS_SELECTOR).extract():
            yield {"repo": "https://github.com" + repo, "language": "python"}


process = CrawlerProcess()
process.crawl(GitHubTrendingPythonSpider)
process.start()
