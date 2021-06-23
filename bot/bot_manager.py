# TODO: repair asynchronous, add comments to all files, connect DB
import asyncio

from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType

from .bot_settings import vk_token
from .bot import VkBot


class BotManager:

    AUTH_USERS = []
    BOTS = []
    TASKS = []

    def __init__(self):
        vk_session = VkApi(token=vk_token)
        self.vk_api = vk_session.get_api()
        self.vk_longpoll = VkLongPoll(vk_session)

    def start_work(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.__start_bots(loop))

    async def __start_bots(self, loop):
        for event in self.vk_longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                if event.user_id not in self.AUTH_USERS:
                    self.AUTH_USERS.append(event.user_id)

                    bot = VkBot(event.user_id)
                    task = loop.create_task(bot.start_bot(event.user_id))
                    self.TASKS.append(task)
                    await asyncio.gather(*self.TASKS)
            else:
                continue
