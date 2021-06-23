"""file for control SiteScraper1 and his specification"""
import requests
from bs4 import BeautifulSoup

from .base_site_scraper import BaseSiteScraper
from .scraper_settings import (
    link_to_site_temporary1,
    temporary_site_element,
    temporary_site_selector,
    scraper1_search_fragment,
    scraper1_language_ru,
    scraper1_language_en,
)


class SiteScraper1(BaseSiteScraper):
    """Class for 1 site scraper"""

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
        super(SiteScraper1, self).__init__()
        self._scraper_number = 1

    def _set_link_to_site(self, search_query, language):
        """set link to scraping site"""
        response = requests.get(link_to_site_temporary1)

        scraper_result = BeautifulSoup(response.text, "lxml")
        self.LINK_TO_SITE = str(
            "https://"
            + scraper_result.find(
                temporary_site_element, class_=temporary_site_selector
            ).text
        )

        if language == "ru":
            self.LINK_TO_SEARCH_PAGE = (
                self.LINK_TO_SITE
                + scraper1_search_fragment
                + str(search_query)
                + scraper1_language_ru
            )
        elif language == "en":
            self.LINK_TO_SEARCH_PAGE = (
                self.LINK_TO_SITE
                + scraper1_search_fragment
                + str(search_query)
                + scraper1_language_en
            )

    def _get_books_elements(self, search_page):
        """return books elements from scraping page"""
        books_elements = search_page.find_all(
            self.BOOK_POST_ELEMENT, style=self.BOOK_POST_SELECTOR
        )

        return books_elements
