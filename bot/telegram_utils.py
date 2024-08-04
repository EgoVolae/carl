import git
import sys

repo_root_dir = git.Repo(__file__, search_parent_directories=True).working_tree_dir
sys.path.append(repo_root_dir)

import asyncio
import random
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ParseMode

import pandas as pd
from typing import Dict, List, Optional

from utils.yt_music_utils import YT_MUSIC_PLAYLIST_BASE_URL

from configuration import Configuration


RECIPIENTS = [
    {
        "username": "tones574",
        "chat_id":7026656480,
        "role": "ADMIN"
    }
]


class CarlTheConductor:

    def __init__(self):
        self.token = Configuration.CARL_BOT_TOKEN
        self.bot = Bot(self.token)
        self.playlist_dict = dict()

    async def get_updates_df(self, limit: Optional[int]=None) -> List[str]:

        update_cols = ["ts", "chat_id", "chat_username", "msg_text"]
        updates_data = []

        async with self.bot:
            updates = (await self.bot.get_updates())
            for update in updates:
                update_datum = [update.message.date, update.message.from_user.id, update.message.from_user.username, update.message.text]
                updates_data.append(update_datum)
        
        df = pd.DataFrame(data=updates_data, columns=update_cols).sort_values(by="ts", ascending=False)
        if limit is not None:
            df = df.head(n=limit)
        return df    

    def get_random_msg_from_playlist_dict(self, playlist_dict: Dict) -> str:
        random_playlist_name = random.choice(list(playlist_dict.keys()))
        random_playlist_id = playlist_dict[random_playlist_name]
        text, url = random_playlist_name, YT_MUSIC_PLAYLIST_BASE_URL + random_playlist_id
        return f"<a href='{url}'>{text}</a>"

    async def random_playlist_link(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        
        msg = self.get_random_msg_from_playlist_dict(self.playlist_dict)
        await update.message.reply_text(msg, parse_mode=ParseMode.HTML)

    async def random_e_link(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        
        e_playlists = {k: v for k, v in self.playlist_dict.items() if "[E]" in k}
        msg = self.get_random_msg_from_playlist_dict(e_playlists)
        await update.message.reply_text(msg, parse_mode=ParseMode.HTML)

    async def random_ne_link(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        
        ne_playlists = {k: v for k, v in self.playlist_dict.items() if "[NE]" in k}
        msg = self.get_random_msg_from_playlist_dict(ne_playlists)
        await update.message.reply_text(msg, parse_mode=ParseMode.HTML)

    @property
    def application(self) -> None:
        
        application = Application.builder().token(self.token).build()
        application.add_handler(CommandHandler("random", self.random_playlist_link))
        application.add_handler(CommandHandler("E", self.random_e_link))
        application.add_handler(CommandHandler("NE", self.random_ne_link))
        return application
    
    def run(self):
        print(f"Running Carl...")
        self.application.run_polling()