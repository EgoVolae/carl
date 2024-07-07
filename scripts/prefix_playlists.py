# Prefxies playlists wiht [E] if they don't already have the [E] or [NE] prefix

import git
import sys

repo_root_dir = git.Repo(__file__, search_parent_directories=True).working_tree_dir
sys.path.append(repo_root_dir)

from ytmusicapi import YTMusic
from pathlib import Path

auth_path = Path(repo_root_dir) / "oauth.json"
client = YTMusic(auth=str(auth_path))

playlists = YTMusic.get_library_playlists(client, limit=100)
for playlist in playlists:
    title = playlist["title"]
    if not str.upper(title) == title:
        continue
    if ("[E]" in title) or ("[NE]" in title):
        continue
    playlist_id = playlist["playlistId"]
    YTMusic.edit_playlist(self=client, playlistId=playlist_id, title=f"[E] {title}")
    print(f"Renamed playlist: {title} -> [E] {title}")