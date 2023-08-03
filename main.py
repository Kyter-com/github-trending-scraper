"""Scrapy library import."""
import json
import datetime
import scrapy
import requests
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


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
    """Spider for daily trending Python repositories."""

    name = "GitHubTrendingSpider"
    start_urls = ["https://github.com/trending/python?since=daily"]

    def parse(self, response):
        for repo in response.css(SHARED_CSS_SELECTOR).extract():
            res = requests.put(
                "url",
                files={
                    "value": f"https://github.com{repo}",
                    "metadata": json.dumps(
                        {"updatedAt": datetime.datetime.now().isoformat()}
                    ),
                },
                headers={"Authorization": "Bearer token"},
                timeout=10,
            )
            res.raise_for_status()
            print("📡 [Python] Successfully synced with Cloudflare KV")


class GitHubTrendingGolangSpider(scrapy.Spider):
    """Spider for daily trending Golang repositories."""

    name = "GitHubTrendingSpider"
    start_urls = ["https://github.com/trending/go?since=daily"]

    def parse(self, response):
        for repo in response.css(SHARED_CSS_SELECTOR).extract():
            yield {"repo": "https://github.com" + repo, "language": "go"}


custom_settings = get_project_settings()
custom_settings["LOG_LEVEL"] = "ERROR"
process = CrawlerProcess(settings=custom_settings)
process.crawl(GitHubTrendingPythonSpider)
process.crawl(GitHubTrendingGolangSpider)
process.start()
