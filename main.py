"""main file for start application"""
# TODO: repair asynchronous, connect DB
from bot.bot_manager import BotManager

if __name__ == "__main__":
    bot_manager = BotManager()
    bot_manager.start_work()
