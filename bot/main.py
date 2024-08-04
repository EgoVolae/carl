import git
import sys

repo_root_dir = git.Repo(__file__, search_parent_directories=True).working_tree_dir
sys.path.append(repo_root_dir)

from telegram_utils import CarlTheConductor
from utils.yt_music_utils import YTMusicHandler

handler = YTMusicHandler()

all_playlists = handler.get_raw_playlists()
names_to_ids = {p["title"]: p["playlistId"] for p in all_playlists}

carl = CarlTheConductor()
carl.playlist_dict = names_to_ids

carl.run()