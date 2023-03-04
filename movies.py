import pandas as pd
import scrapy


class MoviesSpider(scrapy.Spider):
    name = 'movies'
    allowed_domains = ['letterboxd.com']
    start_urls = ['https://letterboxd.com/']

    def parse(self, response):
        urls_df = pd.read_csv('/Users/maryam/PycharmProjects/subgenrescrawler/newnewnewremained.csv')
        urls = urls_df['url'].to_list()
        for url in urls:
            yield response.follow('https://letterboxd.com' + url, callback=self.parse_movies)

    def parse_movies(self, response):
        all_genres = ((((response.css('div#tab-genres')).css('div.text-sluglist.capitalize'))
                       .css('p')).css('a::text')).getall()
        country = []
        language = []
        if response.css('div#tab-details').css('h3').css('span::text').getall()[0] == 'Studios' \
                or response.css('div#tab-details').css('h3').css('span::text').getall()[0] == 'Studio':
            country = response.css('div#tab-details').css('div')[2].css('a::text').getall()
            language = response.css('div#tab-details').css('div')[3].css('a::text').getall()
        elif response.css('div#tab-details').css('h3').css('span::text').getall()[0] == 'Country' \
                or response.css('div#tab-details').css('h3').css('span::text').getall()[0] == 'Countries':
            country = response.css('div#tab-details').css('div')[1].css('a::text').getall()
            language = response.css('div#tab-details').css('div')[2].css('a::text').getall()
        elif response.css('div#tab-details').css('h3').css('span::text').getall()[0] == 'Language' \
                or response.css('div#tab-details').css('h3').css('span::text').getall()[0] == 'Languages':
            country = []
            language = response.css('div#tab-details').css('div')[1].css('a::text').getall()

        if len(country) != 0 and country[0] == 'Iran':
            persian_title = response.css('div.col-17').css('section.film-header-lockup em::text').get()[1:-1]
        else:
            persian_title = ''

        other_links = response.css('a.micro-button.track-event::attr(href)').getall()
        tmdb_url = ''
        imdb_url = ''
        for i in range(len(other_links)):
            if 'themoviedb' in other_links[i]:
                tmdb_url = response.css('a.micro-button.track-event::attr(href)').getall()[i]
            if 'imdb' in other_links[i]:
                imdb_url = response.css('a.micro-button.track-event::attr(href)').getall()[i]

        yield {
            'title': response.css('h1.headline-1.js-widont.prettify::text').get(),
            'persian_title': persian_title,
            'story': response.css('div.truncate').css('p::text').get(),
            "genres": ((((response.css('div#tab-genres')).css('div.text-sluglist.capitalize'))
                       .css('p')).css('a::text')).getall(),
            'director': response.css('span.prettify::text').get(),
            'release_year': response.css('small.number a::text').get(),
            'country': country,
            'language': language,
            'duration': response.css('p.text-link.text-footer').css('p::text').get()[12:-34],
            'letterboxd_url': str(response)[5:-1],
            'imdb_url': imdb_url,
            'tmdb_url': tmdb_url,
        }
