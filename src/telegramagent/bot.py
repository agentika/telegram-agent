from __future__ import annotations

import asyncio
import os

# from contextlib import asynccontextmanager
from telegram import Update
from telegram.ext import Application
from telegram.ext import ContextTypes
from telegram.ext import MessageHandler
from telegram.ext import filters

from .agent import OpenAIAgent


class AgentCallback:
    def __init__(self, agent: OpenAIAgent) -> None:
        self.agent = agent

    async def __call__(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        message = update.message
        if message is None:
            return

        text = message.text
        if text is None:
            return

        output = await self.agent.run(text)
        await message.reply_text(output)


# @asynccontextmanager
# async def init_telegram_bot(agent: OpenAIAgent) -> None:
#     token = os.getenv("BOT_TOKEN")
#     if token is None:
#         raise ValueError("BOT_TOKEN is not set")
#     app = Application.builder().token(token).build()
#     try:
#         await app.initialize()
#         await app.start()
#         await app.updater.start_polling(allowed_updates=Update.ALL_TYPES)

#         app.add_handler(MessageHandler(callback=AgentCallback(agent)))
#     finally:
#         await app.stop()
#         await agent.cleanup()


class TelegramBot:
    def __init__(self, agent: OpenAIAgent) -> None:
        self.agent = agent

        token = os.getenv("BOT_TOKEN")
        if token is None:
            raise ValueError("BOT_TOKEN is not set")

        self.app = Application.builder().token(token).build()

        self.app.add_handler(
            MessageHandler(
                filters=filters.TEXT,
                callback=AgentCallback(agent),
                block=False,
            )
        )

    async def __aenter__(self) -> TelegramBot:
        await self.app.initialize()
        await self.app.start()
        await self.app.updater.start_polling(allowed_updates=Update.ALL_TYPES)

        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.app.updater.stop()
        await self.app.stop()
        await self.app.shutdown()

    async def run(self) -> None:
        while True:
            await asyncio.sleep(1)
