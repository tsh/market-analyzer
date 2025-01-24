from datetime import datetime

import dateutil
from bs4 import BeautifulSoup, SoupStrainer


class Parser:
    TO_EXCLUDE = set()
    
    def __init__(self, page_content: str):
        self.page_content = page_content
        self.soup = BeautifulSoup(self.page_content, 'html.parser')

    def urls(self) -> set:
        to_exclude = {'/login', '/signup', None,  '/', 'javascript:void(0)'}.union(self.TO_EXCLUDE)
        prefix_to_avoid = ['#', 'http', '/help']
        urls = set()
        for a in self.soup.find_all('a'):
            url = a.get('href')
            if url in to_exclude or any(map(url.startswith, prefix_to_avoid)):
                continue
            urls.add(url)
        return urls


class VICParser(Parser):
    TO_EXCLUDE = {'/idea/apply'}


class VICIdeasParser(VICParser):
    def get_ideas_links(self) -> list:
        links = []
        for link in  self.soup.find(id='ideas_body').find_all('a'):
            links.append(link.get('href'))
        return links


class IdeaParser(VICParser):
    def get_author_url(self) -> str:
        return self.soup.find('div', attrs={'class': 'idea_by'}).find('a').get('href')

    def get_publication_date(self) -> datetime:
        raw_text = self.soup.find('div', attrs={'class': 'idea_by'}).find('div').text
        text = raw_text[:-3]  # cut "by " from date
        return dateutil.parser.parse(text)

    def get_idea_description(self) -> str:
        return self.soup.find(attrs={'id':'description'}).text

    def get_ticker(self) -> str:
        raise NotImplementedError

    def get_conclusion(self) -> str:
        # class different at every page
        raw_text = self.soup.find_all('p', attrs={'class': 'MsoNormal'})
        if not raw_text:
            pass
        raise NotImplementedError


class AuthorParser(Parser):
    pass
