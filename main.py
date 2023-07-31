import scrapy


class GitHubTrendingSpider(scrapy.Spider):
    name = "githubtrendingspider"
    start_urls = ["https://github.com/trending/python?since=daily"]

    def parse(self, response):
        print("📡 " + response.url)
