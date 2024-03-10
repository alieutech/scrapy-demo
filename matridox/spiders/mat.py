import scrapy


class MatSpider(scrapy.Spider):
    name = "mat"
    allowed_domains = ["matridox.com"]
    start_urls = ["https://matridox.com/category/reviews/"]

    def parse(self, response):
        next_page = response.xpath("//div[@class='inf-load-more-wrap pagination clearfix inf-spacer']/a/@href").get()
        print(next_page)
        links = response.xpath("//h3[@class='title']/a/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.parse_product)
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response):
        titles = response.xpath("//h1/text()").get()
        image_url = response.xpath("//img/@src").get()
        datetime = response.xpath("//time/@datetime").get().split('T')
        date = datetime[0]
        yield {
            'titles': titles,
            'image_url': image_url,
            'date': date,
            'page_url': response.url
        }

