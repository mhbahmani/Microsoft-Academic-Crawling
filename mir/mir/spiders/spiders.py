from scrapy_splash import SplashRequest 
from bs4 import BeautifulSoup
import scrapy
import json

class ArticlesSpider(scrapy.Spider):
    name = "articlespider"
    start_urls = ['https://academic.microsoft.com/paper/2981549002']
        #https://academic.microsoft.com/paper/3105081694
        #https://academic.microsoft.com/paper/2950893734
        #https://academic.microsoft.com/paper/3119786062
        #https://academic.microsoft.com/paper/2145339207
        #https://academic.microsoft.com/paper/2153579005']

    def start_requests(self): 
        for url in self.start_urls: 
            yield SplashRequest(url, self.parse, 
                endpoint='render.html', 
                args={'wait': 4}, 
           ) 

    def parse(self, response):
        data = {}

        data['id'] = response.url.split('/')[-1]

        data['title'] = BeautifulSoup(
            response.css('h1.name').get(),
            'html.parser'
        ).text.strip()

        data['abstract'] = response.css('p:not(p.help-control-title.au-target)::text').get()

        data['date'] = response.css('span.year::text').get().strip()

        authors = []
        for author in response.css('div.authors')[0].css('a::text'):
            authors.append(author.get())
        data['authors'] = authors

        data['citation_count'] = \
            response.css('div.stats').css('ma-statistics-item')[1].css('div.count::text').get().strip()

        data['reference_count'] = \
            response.css('div.stats').css('ma-statistics-item')[0].css('div.count::text').get().strip()

        references = []
        for ref in response.css('div.results').css('ma-card'):
            references.append(ref.css('div.primary_paper').css('a.title.au-target').css('a[href*=paper]::attr(href)').extract()[0].split('/')[1])
        data['references'] = references

        ### TODO: related_topics

        filename = 'CrawledPapers-%s.json‬‬' % data['id']
        with open(filename, 'w') as file:
            json.dump(data, file)

