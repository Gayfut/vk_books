import asyncio
import aiohttp
import json
import requests
from bs4 import BeautifulSoup

from .scraper_settings import scraper_options_dir


class BaseSiteScraper:

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
        self._scraper_number = None

    def start_parse(self, search_query, language):
        self._set_options()
        search_page = self._get_search_page(search_query, language)
        books_elements = self._get_books_elements(search_page)
        links_to_books = self._get_links_to_books(books_elements)
        pages_with_book_info = self.__get_pages_with_book_info(links_to_books)
        books_info = self.__get_books_info(pages_with_book_info)

        return books_info

    def _set_options(self):
        with open(
            scraper_options_dir
            + "/scraper"
            + str(self._scraper_number)
            + "_options.json",
            encoding="utf-8",
        ) as file_with_options:
            scraper_options = json.load(file_with_options)

        self.LINK_TO_SITE = scraper_options["link_to_site"]
        self.BOOK_POST_ELEMENT = scraper_options["book_post_element"]
        self.BOOK_POST_SELECTOR = scraper_options["book_post_selector"]
        self.TITLE_ELEMENT = scraper_options["title_element"]
        self.TITLE_SELECTOR = scraper_options["title_selector"]
        self.AUTHOR_ELEMENT = scraper_options["author_element"]
        self.AUTHOR_SELECTOR = scraper_options["author_selector"]
        self.DESCRIPTION_ELEMENT = scraper_options["description_element"]
        self.DESCRIPTION_SELECTOR = scraper_options["description_selector"]
        self.DOWNLOAD_LINK_ELEMENT = scraper_options["download_link_element"]
        self.DOWNLOAD_LINK_SELECTOR = scraper_options["download_link_selector"]

    def _get_search_page(self, search_query, language):
        self._set_link_to_site(search_query, language)

        check_success = False
        while check_success is False:
            try:
                response = requests.get(self.LINK_TO_SEARCH_PAGE, verify=False)
                check_success = True
            except requests.exceptions.ConnectionError:
                check_success = False

        search_page = BeautifulSoup(response.text, "lxml")
        return search_page

    def _set_link_to_site(self, search_query, language):
        pass

    @staticmethod
    def _get_correct_search_query(search_query):
        search_query_list = search_query.split()
        search_query = "+".join(search_query_list)

        return search_query

    def _get_books_elements(self, search_page):
        pass

    def _get_links_to_books(self, books_elements):
        links_of_books = []

        for book_element in books_elements:
            link_of_book = self.LINK_TO_SITE + book_element["href"]
            links_of_books.append(link_of_book)

        links_of_books = links_of_books[:5]
        return links_of_books

    def __get_pages_with_book_info(self, links_to_books):
        async_loop = asyncio.get_event_loop()
        coroutines = [
            self._get_page_with_book_info(link_to_book)
            for link_to_book in links_to_books
        ]

        pages_with_book_info = async_loop.run_until_complete(
            asyncio.gather(*coroutines)
        )

        return pages_with_book_info

    @staticmethod
    async def _get_page_with_book_info(link_to_book):
        check_success = False
        while check_success is False:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(link_to_book) as response:
                        response_text = await response.text()
                check_success = True
            except requests.exceptions.ConnectionError:
                check_success = False

        page_with_book_info = BeautifulSoup(response_text, "lxml")
        return page_with_book_info

    def __get_books_info(self, pages_with_book_info):
        async_loop = asyncio.get_event_loop()
        coroutines = [
            self._get_book_info(page_with_book_info)
            for page_with_book_info in pages_with_book_info
        ]

        books_info = async_loop.run_until_complete(asyncio.gather(*coroutines))

        return books_info

    async def _get_book_info(self, page_with_book_info):
        try:
            author = page_with_book_info.find(
                self.AUTHOR_ELEMENT, itemprop=self.AUTHOR_SELECTOR
            ).text
        except AttributeError:
            author = "No author"

        try:
            description = page_with_book_info.find(
                self.DESCRIPTION_ELEMENT, id=self.DESCRIPTION_SELECTOR
            ).text
        except AttributeError:
            description = "No description"

        try:
            download_link = page_with_book_info.find(
                self.DOWNLOAD_LINK_ELEMENT, class_=self.DOWNLOAD_LINK_SELECTOR
            )["href"]
        except TypeError:
            download_link = "No link to download"

        book_info = {
            "title": page_with_book_info.find(
                self.TITLE_ELEMENT, itemprop=self.TITLE_SELECTOR
            ).text,
            "author": author,
            "description": description,
            "download_link": self.LINK_TO_SITE + download_link,
        }

        return book_info
