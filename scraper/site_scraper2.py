from requests_html import AsyncHTMLSession, HTMLSession
from bs4 import BeautifulSoup

from .base_site_scraper import BaseSiteScraper
from .scraper_settings import (
    scraper2_search_fragment,
    scraper2_language_ru,
    scraper2_language_en,
)


class SiteScraper2(BaseSiteScraper):

    LINK_TO_SITE = None
    LINK_TO_SEARCH_PAGE = None
    BOOK_POST_ELEMENT = None
    BOOK_POST_SELECTOR = None
    TITLE_ELEMENT = None
    TITLE_SELECTOR = None
    AUTHOR_ELEMENT = None
    AUTHOR_SELECTOR = None
    DESCRIPTION_ELEMENT = None
    DESCRIPTION_SELECTOR = None
    DOWNLOAD_LINK_ELEMENT = None
    DOWNLOAD_LINK_SELECTOR = None

    def __init__(self):
        super(SiteScraper2, self).__init__()
        self._scraper_number = 2

    def _get_search_page(self, search_query, language):
        self._set_link_to_site(search_query, language)

        scraper = HTMLSession()
        response = scraper.get(self.LINK_TO_SEARCH_PAGE)
        search_page = BeautifulSoup(response.text, "lxml")

        return search_page

    def _set_link_to_site(self, search_query, language):
        search_query = SiteScraper2._get_correct_search_query(search_query)

        if language == "ru":
            self.LINK_TO_SEARCH_PAGE = (
                self.LINK_TO_SITE
                + scraper2_search_fragment
                + search_query
                + scraper2_language_ru
            )
        elif language == "en":
            self.LINK_TO_SEARCH_PAGE = (
                self.LINK_TO_SITE
                + scraper2_search_fragment
                + search_query
                + scraper2_language_en
            )

    def _get_books_elements(self, search_page):
        books_elements = search_page.find_all(
            self.BOOK_POST_ELEMENT, class_=self.BOOK_POST_SELECTOR
        )

        return books_elements

    @staticmethod
    async def _get_page_with_book_info(link_to_book):
        session = AsyncHTMLSession()
        response = await session.get(link_to_book)
        response_text = response.text
        page_with_book_info = BeautifulSoup(response_text, "lxml")

        return page_with_book_info
