from typing import Annotated

import typer
from dotenv import find_dotenv
from dotenv import load_dotenv

from .agent import OpenAIAgent
from .bot import TelegramBot
from .config import Config


def run(config_file: Annotated[str, typer.Option("-c", "--config")] = "config.json") -> None:
    config = Config.from_json(config_file)
    agent = OpenAIAgent.from_config(config)
    bot = TelegramBot(agent=agent)
    bot.run()


def main() -> None:
    load_dotenv(find_dotenv())
    typer.run(run)
