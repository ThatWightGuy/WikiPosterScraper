from requests import get
from requests.exceptions import RequestException
from bs4 import BeautifulSoup as bs
from contextlib import closing
from wikipedia.exceptions import PageError
import wikipedia as wiki


class Poster:
    def __init__(self, title, year=int()):
        self.title = title
        self.year = year
        self.search = self.__get_search_query()
        self.wiki_page = self.__get_wiki_page()

    def __get_search_query(self):
        return ' '.join([self.title, str(self.year)]) + ' film'

    def __get_wiki_page(self):
        try:
            return wiki.page(self.search, auto_suggest=True)
        except PageError:
            print('No Page Found. Try adding a year to your query or check if information is correct.')
            return wiki.WikipediaPage('Main_Page')

    def __get_url_content(self, url):
        try:
            with closing(get(url, stream=True)) as response:
                if self.__check_response(response):
                    html = response.content
                    return html

        except RequestException as e:
            print(str(e))
            return ''

    def __check_response(self, response):
        good_response = False

        if response.status_code == 200:
            good_response = True

        return good_response

    def get_poster_url(self):
        try:
            page = bs(self.__get_url_content(self.wiki_page.url), 'html.parser')
            return 'https:%s' % page.find('table', class_='infobox vevent').find('img')['src']
        except AttributeError:
            print('No Poster Found On Page. Try adding a year to your query or check if information is correct.')
            return ''

    def save_poster(self, url, destination='', filename=''):
        file_ext = url.split('/')[-1].split('.')

        if filename is '':
            file_dest = '/'.join([destination, '.'.join(file_ext)])
        else:
            file_dest = '/'.join([destination, '.'.join([filename, file_ext[-1]])])

        with open(file_dest, 'wb') as file:
            file.write(self.__get_url_content(url))

if __name__ == '__main__':
    poster = Poster('Who Killed Captain Alex?', year=2010)
    poster.save_poster(poster.get_poster_url(), destination='test')
