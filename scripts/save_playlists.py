# Generates and saves down a csv containing all information about current playlists in my library

import git
import sys

repo_root_dir = git.Repo(__file__, search_parent_directories=True).working_tree_dir
sys.path.append(repo_root_dir)

from ytmusicapi import YTMusic
from pathlib import Path
import pandas as pd
import datetime as dt
from typing import Dict
import json


def __main__():

    auth_path = Path(repo_root_dir) / "oauth.json"
    data_dir_path = Path(repo_root_dir) / "data"
    client = YTMusic(auth=str(auth_path))
    today_str = dt.datetime.now().strftime("%Y%m%d")

    playlists = YTMusic.get_library_playlists(client, limit=100)

    rows = []

    for playlist in playlists:
        print(playlist)
        playlist_name = playlist["title"]
        if ("[E]" not in playlist_name) and ("[NE]" not in playlist_name):
            continue
        playlist_id = playlist["playlistId"]
        playlist_data = YTMusic.get_playlist(client, playlistId=playlist_id, limit=1000)
        print(f"Getting data for {playlist_name}...")
        row = {"name": playlist_name, "description": playlist["description"]}
        rows.append(row)

    df = pd.DataFrame(rows)

    output_filename = f"{today_str}_YTMusic_playlists.csv"
    latest_playlists_filename = f"latest_YTMusic_playlists.csv"
    latest_playlists_metadata = {"date": today_str}

    df.to_csv(data_dir_path / output_filename, index=False)
    df.to_csv(data_dir_path / latest_playlists_filename, index=False)

    with open(data_dir_path / "latest_YTMusic_playlists_metadata.json", "w") as file:
        json.dump(latest_playlists_metadata, file)

    print(f"Successfully saved down information on {df.shape[0]} playlists")

__main__()