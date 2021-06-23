"""file for control social media scraper and his specification"""
import requests
from .scraper_settings import (
    soc_scraper_link,
    soc_scraper_search_fragment,
    soc_scraper_4,
    soc_scraper_5,
    soc_scraper_6,
    soc_scraper_7,
    soc_scraper_8,
    soc_scraper_9,
)


class SocScraper:
    """Class for social media scraper"""

    LINK_TO_SITE = None

    def __init__(self, scraper_number):
        self.__scraper_number = scraper_number

    def start_parse(self, search_query):
        """start scraping process"""
        self.__set_link_to_site(search_query)
        posts = self.__get_posts()
        books_info = self.__get_books_info(posts)

        return books_info

    def __set_link_to_site(self, search_query):
        """set link to page for scraping chosen source"""
        if self.__scraper_number == 4:
            self.LINK_TO_SITE = str(
                soc_scraper_link
                + soc_scraper_4
                + soc_scraper_search_fragment
                + search_query
            )
        elif self.__scraper_number == 5:
            self.LINK_TO_SITE = str(
                soc_scraper_link
                + soc_scraper_5
                + soc_scraper_search_fragment
                + search_query
            )
        elif self.__scraper_number == 6:
            self.LINK_TO_SITE = str(
                soc_scraper_link
                + soc_scraper_6
                + soc_scraper_search_fragment
                + search_query
            )
        elif self.__scraper_number == 7:
            self.LINK_TO_SITE = str(
                soc_scraper_link
                + soc_scraper_7
                + soc_scraper_search_fragment
                + search_query
            )
        elif self.__scraper_number == 8:
            self.LINK_TO_SITE = str(
                soc_scraper_link
                + soc_scraper_8
                + soc_scraper_search_fragment
                + search_query
            )
        elif self.__scraper_number == 9:
            self.LINK_TO_SITE = str(
                soc_scraper_link
                + soc_scraper_9
                + soc_scraper_search_fragment
                + search_query
            )

    def __get_posts(self):
        """return posts which contains search query"""
        posts = requests.get(self.LINK_TO_SITE).json()

        return posts

    @staticmethod
    def __get_books_info(posts):
        """return all books info from posts"""
        books_info = []

        for post_number in range(1000):
            try:
                try:
                    if (
                        posts["response"]["items"][post_number]["attachments"][1][
                            "type"
                        ]
                        == "doc"
                    ):
                        book_info = {
                            "title": posts["response"]["items"][post_number][
                                "attachments"
                            ][1]["doc"]["title"],
                            "author": "No author",
                            "description": "No description",
                            "download_link": posts["response"]["items"][post_number][
                                "attachments"
                            ][1]["doc"]["url"],
                        }
                        books_info.append(book_info)
                except KeyError:
                    continue
            except IndexError:
                continue

        books_info = books_info[:5]
        return books_info
