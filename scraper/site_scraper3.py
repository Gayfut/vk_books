from .base_site_scraper import BaseSiteScraper
from .scraper_settings import scraper3_search_fragment


class SiteScraper3(BaseSiteScraper):

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
        super(SiteScraper3, self).__init__()
        self._scraper_number = 3

    def _set_link_to_site(self, search_query, language):
        search_query = SiteScraper3._get_correct_search_query(search_query)

        self.LINK_TO_SEARCH_PAGE = str(
            self.LINK_TO_SITE + scraper3_search_fragment + search_query
        )

    def _get_books_elements(self, search_page):
        books_elements = search_page.find_all(
            self.BOOK_POST_ELEMENT, class_=self.BOOK_POST_SELECTOR
        )

        return books_elements

    def _get_links_to_books(self, books_elements):
        links_of_books = []

        for book_element in books_elements:
            link_of_book = book_element["href"]
            links_of_books.append(link_of_book)

        links_of_books = links_of_books[:5]
        return links_of_books

    async def _get_book_info(self, page_with_book_info):
        try:
            author = page_with_book_info.find(
                self.AUTHOR_ELEMENT, class_=self.AUTHOR_SELECTOR
            ).text
        except AttributeError:
            author = "No author"

        try:
            description = (
                page_with_book_info.find(
                    self.DESCRIPTION_ELEMENT, class_=self.DESCRIPTION_SELECTOR
                )
                .find("p", recursive=False)
                .text
            )
        except AttributeError:
            description = "No description"

        try:
            download_link = page_with_book_info.find(
                self.DOWNLOAD_LINK_ELEMENT, {"id": self.DOWNLOAD_LINK_SELECTOR}
            )["href"]
        except TypeError:
            download_link = "No link to download"

        book_info = {
            "title": page_with_book_info.find(
                self.TITLE_ELEMENT, class_=self.TITLE_SELECTOR
            ).text,
            "author": author,
            "description": description,
            "download_link": download_link,
        }

        return book_info
