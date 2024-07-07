import git
import sys

repo_root_dir = git.Repo(__file__, search_parent_directories=True).working_tree_dir
sys.path.append(repo_root_dir)

from ytmusicapi import YTMusic
from pathlib import Path
import pandas as pd
import datetime as dt
from typing import Dict


def get_track_details(track: Dict, playlist_name: str = "") -> Dict[str, str]:
    title = track["title"]
    try:
        artist = track["artists"][0]["name"]
    except Exception:
        artist = ""
    try:
        album = track["album"]["name"]
    except Exception:
        album = ""
    duration = track["duration"]
    is_liked = track["likeStatus"] == "LIKE"
    video_id = track["videoId"]
    video_type = track["videoType"]
    return {
        "playlist": playlist_name, "title": title, "artist": artist, 
        "album": album, "duration": duration, "is_liked": is_liked,
        "video_id": video_id, "video_type": video_type
    }


def __main__():

    auth_path = Path(repo_root_dir) / "oauth.json"
    data_dir_path = Path(repo_root_dir) / "data"
    client = YTMusic(auth=str(auth_path))
    today_str = dt.datetime.now().strftime("%Y%m%d")

    playlists = YTMusic.get_library_playlists(client, limit=100)

    rows = []
    playlist_count = 0

    for playlist in playlists:
        playlist_name = playlist["title"]
        if ("[E]" not in playlist_name) and ("[NE]" not in playlist_name):
            continue
        playlist_id = playlist["playlistId"]
        playlist_data = YTMusic.get_playlist(client, playlistId=playlist_id, limit=1000)
        print(f"Getting data for {playlist_name}...")
        for track in playlist_data["tracks"]:
            track_data = get_track_details(track, playlist_name)
            rows.append(track_data)
        playlist_count += 1

    df = pd.DataFrame(rows)

    output_filename = f"{today_str}_YTMusic_tracks.csv"
    output_filepath = data_dir_path / output_filename
    df.to_csv(output_filepath, index=False)
    print(f"Successfully saved down information on {df.shape[0]} tracks in {playlist_count} playlists at {output_filename}")

__main__()