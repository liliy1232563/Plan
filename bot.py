# Don't Remove Credit @CodeFlix_Bots, @rohit_1888
# Ask Doubt on telegram @CodeflixSupport
#
# Copyright (C) 2025 by Codeflix-Bots@Github
# https://github.com/Codeflix-Bots
#
# This file is part of Codeflix-Bots/FileStore
# Released under the MIT License.

from aiohttp import web
from plugins import web_server
import asyncio
import pyromod.listen
from pyrogram import Client
from pyrogram.enums import ParseMode
import sys
import pytz
from datetime import datetime
from config import *
from database.db_premium import *
from database.database import *
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging

logging.getLogger("apscheduler").setLevel(logging.WARNING)

scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
scheduler.add_job(remove_expired_users, "interval", seconds=10)


async def daily_reset_task():
    try:
        await db.reset_all_verify_counts()
    except Exception:
        pass


scheduler.add_job(daily_reset_task, "cron", hour=0, minute=0)


def get_indian_time():
    """Returns the current time in IST."""
    ist = pytz.timezone("Asia/Kolkata")
    return datetime.now(ist)


name = """
BY CODEFLIX BOTS
"""


class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={"root": "plugins"},
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        scheduler.start()

        usr_bot_me = await self.get_me()
        self.uptime = get_indian_time()

        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel

            test = await self.send_message(
                chat_id=db_channel.id,
                text="Test Message"
            )
            await test.delete()

        except Exception as e:
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(
                f"Make Sure bot is Admin in DB Channel, "
                f"and double-check CHANNEL_ID. Current Value: {CHANNEL_ID}"
            )
            self.LOGGER(__name__).info(
                "\nBot Stopped. Join https://t.me/Mature_Nation for support"
            )
            sys.exit()

        self.set_parse_mode(ParseMode.HTML)

        self.LOGGER(__name__).info(
            "Bot Running..!\n\nCreated by\nhttps://t.me/weebs_support"
        )

        self.LOGGER(__name__).info(
            r"""
  ___ ___  ___  ___ ___ _    _____  _____  ___ _____ ___
 / __/ _ \|   \| __| __| |  |_ _\ \/ / _ )/ _ \_   _/ __|
| (_| (_) | |) | _|| _|| |__ | | >  <| _ \ (_) || | \__ \
 \___\___/|___/|___|_| |____|___/_/\_\___/\___/ |_| |___/
"""
        )

        self.username = usr_bot_me.username

        self.LOGGER(__name__).info(
            "Bot Running..! Made by @Ecchi_Culture"
        )

        # Start Web Server
        app = web.AppRunner(await web_server())
        await app.setup()
        await web.TCPSite(app, "0.0.0.0", PORT).start()

        # Notify owner that the bot has restarted
        try:
            await self.send_message(
                OWNER_ID,
                text=(
                    "<b><blockquote>"
                    "Bᴏᴛ Rᴇsᴛᴀʀᴛᴇᴅ by @Ecchi_Culture"
                    "</blockquote></b>"
                )
            )
        except Exception as e:
            self.LOGGER(__name__).warning(
                f"Could not notify OWNER_ID: {e}"
            )

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")

    def run(self):
        """Run the bot."""
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.start())

        self.LOGGER(__name__).info(
            "Bot is now running. Thanks to @Ecchi_Culture"
        )

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            self.LOGGER(__name__).info("Shutting down...")
        finally:
            loop.run_until_complete(self.stop())


# Copyright (C) 2025 by Codeflix-Bots@Github
# Released under the MIT License.