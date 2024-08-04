import git
import sys

repo_root_dir = git.Repo(__file__, search_parent_directories=True).working_tree_dir
sys.path.append(repo_root_dir)

import bot.telegram_utils as telegram_utils
import asyncio

df = asyncio.run(telegram_utils.get_updates_df())
print(df)