import git
import sys

repo_root_dir = git.Repo(__file__, search_parent_directories=True).working_tree_dir
sys.path.append(repo_root_dir)

import asyncio
import telegram
import pandas as pd
from typing import List, Optional

import configs.telegram_config as telegram_config
from configuration import Configuration


async def broadcast_tg_message(msg: str, recipient_subset: List[str]=[], admin_only: bool=False) -> List[str]:

    bot = telegram.Bot(Configuration.BLETCHLEY_BOT_TOKEN)
    async with bot:

        for recipient in telegram_config.BLETCHLEY_BOT_RECEIPIENTS:
            if len(recipient_subset) > 0 and recipient["username"] not in recipient_subset:
                continue

            if admin_only and recipient["role"] != "ADMIN":
                continue

            await bot.send_message(text=msg, chat_id=recipient["chat_id"])

async def get_updates_df(limit: Optional[int]=None) -> List[str]:

    bot = telegram.Bot(Configuration.BLETCHLEY_BOT_TOKEN)
    
    update_cols = ["ts", "chat_id", "chat_username", "msg_text"]
    updates_data = []

    async with bot:
        updates = (await bot.get_updates())
        for update in updates:
            update_datum = [update.message.date, update.message.from_user.id, update.message.from_user.username, update.message.text]
            updates_data.append(update_datum)
    
    df = pd.DataFrame(data=updates_data, columns=update_cols).sort_values(by="ts", ascending=False)
    if limit is not None:
        df = df.head(n=limit)
    return df
