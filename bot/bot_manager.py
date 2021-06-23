"""file for control bot manager and his specification"""
import asyncio

from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType

from .bot_settings import vk_token
from .bot import VkBot


class BotManager:
    """Class for bot manager. Bot manager - control all bots."""

    # Old users(with started bots)
    AUTH_USERS = []
    # Bots tasks for asyncio loop
    TASKS = []

    def __init__(self):
        vk_session = VkApi(token=vk_token)
        self.__vk_api = vk_session.get_api()
        self.__vk_longpoll = VkLongPoll(vk_session)

    def start_work(self):
        """start bot manager work"""
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.__start_bots(loop))

    async def __start_bots(self, loop):
        """listen vk server, if get message from new user - start new bot for him"""
        for event in self.__vk_longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                if event.__user_id not in self.AUTH_USERS:
                    self.AUTH_USERS.append(event.__user_id)

                    bot = VkBot(event.__user_id)
                    task = loop.create_task(bot.start_bot(event.__user_id))
                    self.TASKS.append(task)
                    await asyncio.gather(*self.TASKS)
            else:
                continue
