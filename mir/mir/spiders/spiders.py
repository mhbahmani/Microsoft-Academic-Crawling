import scrapy

class ArticlesSpider(scrapy.Spider):
    name = "articlespider"
    # start_urls = ['https://academic.microsoft.com/paper/2981549002']
        #https://academic.microsoft.com/paper/3105081694
        #https://academic.microsoft.com/paper/2950893734
        #https://academic.microsoft.com/paper/3119786062
        #https://academic.microsoft.com/paper/2145339207
        #https://academic.microsoft.com/paper/2153579005']
    start_urls = ['https://www.zyte.com/blog/page/2']

    def parse(self, response):
        page = response.url
        print(page)
        filename = 'article-%s.html' % page.split('/')[-2]
        with open(filename, 'wb') as f:
            f.write(response.body)

