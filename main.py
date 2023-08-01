import scrapy


class GitHubTrendingSpider(scrapy.Spider):
    name = "GitHubTrendingSpider"
    start_urls = ["https://github.com/trending/python?since=daily"]

    def parse(self, response):
        for repo in response.css(
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
        ).extract():
            yield {"repo": "https://github.com" + repo, "language": "python"}


# Run with scrapy runspider main.py -o output.json
