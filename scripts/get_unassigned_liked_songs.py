# Generates and saves down a csv containing all information about current tracks in my library

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

    liked_tracks_data = YTMusic.get_liked_songs(client, limit=1000)

    rows = []
    for track in liked_tracks_data["tracks"]:
        track_data = get_track_details(track)
        rows.append(track_data)

    liked_tracks_df = pd.DataFrame(rows)
    library_tracks_df = pd.read_csv(data_dir_path / f"latest_YTMusic_tracks.csv")
    library_tracks_video_ids = library_tracks_df["video_id"].tolist()
    unassigned_liked_tracks_df = liked_tracks_df[~liked_tracks_df["video_id"].isin(library_tracks_video_ids)]

    print(f"We have {liked_tracks_df.shape[0]} liked tracks; {unassigned_liked_tracks_df.shape[0]} are unassigned")

    output_filename = f"{today_str}_unassignedlikedtracks.csv"
    unassigned_liked_tracks_df.to_csv(data_dir_path / output_filename, index=False)

__main__()