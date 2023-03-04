import re
import csv
import json
import requests
import xmltojson
import pandas as pd
from bs4 import BeautifulSoup

headers = {
    'authority': 'letterboxd.com',
    'accept': '*/*',
    'x-requested-with': 'XMLHttpRequest',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 '
                  'Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://letterboxd.com/films/popular/',
    'accept-language': 'en-GB,en;q=0.9,fa-IR;q=0.8,fa;q=0.7,en-US;q=0.6',
}

params = {
    'esiAllowFilters': 'true',
}


def get_movie_url():
    movie_urls = {'title': [], 'url': []}
    with open('../../../final_files/final_movie_urls.csv', 'w') as f1:
        writer = csv.writer(f1)
        # 9983 pages
        for i in range(0, 2001):
            try:
                if i == 0:
                    html_response = requests.get('https://letterboxd.com/films/ajax/popular/size/small/',
                                                 params=params, headers=headers)
                else:
                    html_response = requests.get(
                        'https://letterboxd.com/films/ajax/popular/size/small/page/{}'.format(i),
                        params=params, headers=headers)
                    if i % 50 == 0:
                        print(i)
                soup = BeautifulSoup('<html lang="en"><head></head><body>' + html_response.text + '</body></html>',
                                     'html.parser')
                with open("../../../sample.html", "w") as html_file:
                    html_file.write(str(soup))

                with open("../../../sample.html", "r") as html_file:
                    html = html_file.read()
                    json_ = xmltojson.parse(html)

                result = json.loads(json_)
                for j in range(len(result['html']['body']['ul']['li'])):
                    writer.writerow([((result['html']['body']['ul']['li'][j]['div']['@data-film-slug'][6:])
                                      .replace('-', ' ')).replace('/', ' '),
                                     result['html']['body']['ul']['li'][j]['div']['@data-film-slug']])
            except:
                continue
    return movie_urls

