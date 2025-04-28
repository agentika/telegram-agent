import asyncio

from dotenv import find_dotenv
from dotenv import load_dotenv

from .agent import OpenAIAgent
from .bot import TelegramBot
from .config import Config


async def run() -> None:
    config = Config.from_json("config.json")
    agent = OpenAIAgent.from_config(config)
    async with TelegramBot(agent=agent) as bot:
        await bot.run()


def main() -> None:
    load_dotenv(find_dotenv())

    asyncio.run(run())
