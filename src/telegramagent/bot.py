from __future__ import annotations

import asyncio
import os

from telegram import Update
from telegram.ext import Application
from telegram.ext import ContextTypes
from telegram.ext import MessageHandler
from telegram.ext import filters

from .agent import OpenAIAgent


class TelegramBot:
    def __init__(self, agent: OpenAIAgent, cache_key_prefix: str = "telegram_agent") -> None:
        self.agent = agent
        self.cache_key_prefix = cache_key_prefix

        token = os.getenv("BOT_TOKEN")
        if token is None:
            raise ValueError("BOT_TOKEN is not set")

        self.app = Application.builder().token(token).build()
        self.app.add_handler(
            MessageHandler(
                filters=filters.TEXT,
                callback=self.callback,
                block=False,
            )
        )

    async def callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        message = update.message
        if message is None:
            return

        text = message.text
        if text is None:
            return

        output = await self.agent.run(
            text=text,
            cache_key=f"{self.cache_key_prefix}:{message.chat.id}",
        )
        await message.reply_text(output)

    async def initialize(self) -> None:
        await self.agent.connect()

        await self.app.initialize()
        await self.app.start()

        if self.app.updater:
            await self.app.updater.start_polling(allowed_updates=Update.ALL_TYPES)

    async def close(self) -> None:
        if self.app.updater:
            await self.app.updater.stop()

        await self.app.stop()
        await self.app.shutdown()

        await self.agent.cleanup()

    async def arun(self) -> None:
        try:
            await self.initialize()
            while True:
                await asyncio.sleep(1)
        finally:
            await self.close()

    def run(self) -> None:
        asyncio.run(self.arun())
