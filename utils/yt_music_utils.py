import git
import sys

repo_root_dir = git.Repo(__file__, search_parent_directories=True).working_tree_dir
sys.path.append(repo_root_dir)

from typing import List
from ytmusicapi import YTMusic
from pathlib import Path

YT_MUSIC_PLAYLIST_BASE_URL = "https://music.youtube.com/playlist?list="

class YTMusicHandler:

    def __init__(self) -> None:

        auth_path = Path(repo_root_dir) / "oauth.json"
        self.client = YTMusic(auth=str(auth_path))
    
    def get_raw_playlists(self) -> List:
        return YTMusic.get_library_playlists(self.client, limit=100)
