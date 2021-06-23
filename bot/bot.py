"""file for control bot and his specification"""
from aiovk import TokenSession, API
from aiovk.longpoll import UserLongPoll
from vk_api.utils import get_random_id

from scraper.site_scraper1 import SiteScraper1
from scraper.site_scraper2 import SiteScraper2
from scraper.site_scraper3 import SiteScraper3
from scraper.soc_scraper import SocScraper
from .bot_settings import vk_token, vk_bot_password


class VkBot:
    """Class for Vk Bot. Control him and his specification"""

    # Users success passed auth
    ACCESS_USERS = []

    def __init__(self, user_id):
        vk_session = TokenSession(access_token=vk_token)
        self.__vk_api = API(vk_session)
        self.__vk_longpoll = UserLongPoll(self.__vk_api, mode=2)

        self.__user_id = user_id

    async def start_bot(self, user_id):
        """start bot work"""
        await self.__send_welcome(user_id)
        await self.__start_messaging()

    async def __start_messaging(self):
        """listen vk server and choose next step"""
        async for event in self.__vk_longpoll.iter():
            if event[0] == 4 and event[2] == (1 or 17):
                print(
                    "Name: "
                    + await self.__get_name(event[3])
                    + "\nEvent: "
                    + event[5]
                )
                if await self.__auth(event) is True:
                    if event[5] == "Поиск":
                        await self.__send_question_about_source(event)
                        source_number = await self.__get_source_number()
                        await self.__send_question_about_title(event)
                        title = await self.__get_title()
                        if source_number == 1 or source_number == 2:
                            await self.__send_question_about_language(event)
                            language = await self.__get_language()
                        else:
                            language = None

                        await self.__send_info_about_request(
                            event, title, source_number, language=language
                        )
                        await self.__send_books_info(
                            event, title, source_number, language=language
                        )
                    else:
                        await self.__send_info_about_functions(event)
                else:
                    continue

    async def __auth(self, event):
        """auth user for access"""
        if event[3] not in self.ACCESS_USERS:
            await self.__vk_api.messages.send(
                user_id=event[3],
                random_id=get_random_id(),
                message="Пожалуйста, введите код доступа.",
            )
            check_status = await self.__check_password()
            return check_status
        else:
            return True

    async def __check_password(self):
        """check correct user password or not"""
        async for event in self.__vk_longpoll.iter():
            if event[0] == 4 and event[2] == (1 or 17):
                if event[5] == vk_bot_password:
                    self.ACCESS_USERS.append(event[3])
                    await self.__vk_api.messages.send(
                        user_id=event[3],
                        random_id=get_random_id(),
                        message="Доступ получен.",
                    )
                    check_status = True
                    break
                else:
                    await self.__vk_api.messages.send(
                        user_id=event[3],
                        random_id=get_random_id(),
                        message="В доступе отказано.",
                    )
                    check_status = False
                    break

        return check_status

    async def __send_welcome(self, user_id):
        """send welcome to user"""
        await self.__vk_api.messages.send(
            user_ids=user_id,
            random_id=get_random_id(),
            message="Здравствуйте, " + await self.__get_name(user_id) + ".",
        )

    async def __send_question_about_source(self, event):
        """send question about source for search"""
        await self.__vk_api.messages.send(
            user_id=event[3],
            random_id=get_random_id(),
            message="Пожалуйста, выберите лишь один источник.\n(напишите цифру от 1 до 9)\n\n1 - Любая сфера; самая большая база (нестабильный).\n2 - Любая сфера; большая база\n3 - Любая сфера; средняя база\n4 - Современное искусство; маленькая база.\n5 - Любая сфера; средняя база; только на английском.\n6 - Сфера IT; средняя база; только на английском.\n7 - Сфера IT; средняя база; только на русском.\n8 - Сфера IT; средняя база.\n9 - Сфера физики, математика, IT; средняя база.",
        )

    async def __get_source_number(self):
        """return user chosen source for search"""
        async for event in self.__vk_longpoll.iter():
            if (
                event[0] == 4
                and event[2] == 1
                and int(event[5]) in range(1, 10)
            ):
                source_number = int(event[5])
                break
            elif event[0] == 4 and event[2] == 1:
                await self.__vk_api.messages.send(
                    user_id=event[3],
                    random_id=get_random_id(),
                    message="Пожалуйста, напишите цифру от 1 до 9.",
                )
                continue

        return source_number

    async def __send_question_about_title(self, event):
        """send question about book title"""
        await self.__vk_api.messages.send(
            user_id=event[3],
            random_id=get_random_id(),
            message="Пожалуйста, введите название книги, которую необходимо найти.",
        )

    async def __get_title(self):
        """return user book title"""
        async for event in self.__vk_longpoll.iter():
            if event[0] == 4 and event[2] == 1:
                title = event[5]
                break

        return title

    async def __send_question_about_language(self, event):
        """send question about language of book"""
        await self.__vk_api.messages.send(
            user_id=event[3],
            random_id=get_random_id(),
            message="Пожалуйста, выберите язык.\n(Только en или ru)",
        )

    async def __get_language(self):
        """return user chosen language for book"""
        async for event in self.__vk_longpoll.iter():
            if event[0] == 4 and event[2] == 1:
                language = event[5]
                break

        return language

    async def __send_info_about_request(self, event, title, source_number, language=None):
        """send all info about user search request"""
        if language is not None:
            await self.__vk_api.messages.send(
                user_id=event[3],
                random_id=get_random_id(),
                message="Источник - "
                + str(source_number)
                + "\nНазвание книги - "
                + title
                + "\nЯзык книги - "
                + language
                + "\nПожалуйста, ожидайте...",
            )
        else:
            await self.__vk_api.messages.send(
                user_id=event[3],
                random_id=get_random_id(),
                message="Источник - "
                + str(source_number)
                + "\nНазвание книги - "
                + title
                + "\nПожалуйста, ожидайте...",
            )

    async def __send_books_info(self, event, title, source_number, language="ru"):
        """scraper and send scrapped info about books"""
        if source_number == 1:
            scraper = SiteScraper1()
            books_info = scraper.start_parse(title, language)
        elif source_number == 2:
            scraper = SiteScraper2()
            books_info = scraper.start_parse(title, language)
        elif source_number == 3:
            scraper = SiteScraper3()
            books_info = scraper.start_parse(title, language)
        else:
            scraper = SocScraper(source_number)
            books_info = scraper.start_parse(title)

        for book_info in books_info:
            await self.__vk_api.messages.send(
                user_id=event[3],
                random_id=get_random_id(),
                message="Название - "
                + book_info["title"]
                + "\nАвтор - "
                + book_info["author"]
                + "\nОписание - "
                + book_info["description"]
                + "\nСкачать - "
                + book_info["download_link"],
            )

    async def __send_info_about_functions(self, event):
        """send info about all bot functions"""
        await self.__vk_api.messages.send(
            user_id=event[3],
            random_id=get_random_id(),
            message='Для поиска книги, пожалуйста, напишите "Поиск"',
        )

    async def __get_name(self, user_id):
        """return user first name"""
        info = await self.__vk_api.users.get(user_ids=user_id)
        user_name = info[0]["first_name"]

        return user_name
