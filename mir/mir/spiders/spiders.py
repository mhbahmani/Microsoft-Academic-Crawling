from scrapy_splash import SplashRequest 
from bs4 import BeautifulSoup
import scrapy
import json
import re

class ArticlesSpider(scrapy.Spider):
    name = "articlespider"
    start_urls = ['https://academic.microsoft.com/paper/2981549002',
        'https://academic.microsoft.com/paper/3105081694',
        'https://academic.microsoft.com/paper/2950893734',
        'https://academic.microsoft.com/paper/3119786062',
        'https://academic.microsoft.com/paper/2145339207',
        'https://academic.microsoft.com/paper/2153579005']

    queue = []
    crawled = set()

    def start_requests(self): 
        
        lua_script = """
            function main(splash)   
                assert(splash:go(splash.args.url))
                splash:wait(0.5)  
                splash:evaljs("document.getElementsByClassName('tag-cloud')[0].getElementsByClassName('au-target icon-expand')[0].click();")   
            end
        """

        for url in self.start_urls: 
            yield SplashRequest(url, self.parse, 
                endpoint='render.html', 
                args={'lua_source': lua_script, 'wait': 20}, 
           )


    def parse(self, response):
    
        references = []
        for ref in response.css('div.results').css('ma-card').css('div.primary_paper').css('a.title.au-target').css('a[href*=paper]::attr(href)').getall():
            ref_id = ref.split('/')[1]
            self.queue.append(ref_id)
            references.append(ref_id)

        article_id = response.url.split('/')[-1]

        self.crawled.add(article_id)
        yield {
            'id': article_id,
            'title': BeautifulSoup(
                        response.css('h1.name').get(),
                        'html.parser'
                    ).text.strip(),
            # 'title': re.sub('<.*>', '', str(response.css('h1.name').get())).strip(),
            'abstract': response.css('p:not(p.help-control-title.au-target)::text').get(),
            'date': response.css('span.year::text').get().strip(),
            'authors': response.css('div.authors')[0].css('a::text').getall(),
            'related_topics': [related.split('/')[-1] for related in response.css('div.topics').css('div.tag-cloud').css('a.ma-tag.au-target').css('a[href*=topic]::attr(href)').getall()],
            'citation_count' : \
                response.css('div.stats'
                ).css('ma-statistics-item'
                )[1].css('div.count::text'
                ).get().strip(),
            'reference_count': \
                response.css('div.stats'
                ).css('ma-statistics-item'
                )[0].css('div.count::text'
                ).get().strip(),
            'references': list(set(references))[:10]
        }


        for page_id in self.queue:
            if page_id in self.crawled:
                continue

            yield SplashRequest('https://academic.microsoft.com/paper/%s' % page_id,
                self.parse, 
                endpoint='render.html', 
                args={'wait': 20}, 
           )
