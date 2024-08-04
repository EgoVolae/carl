import git
import sys

repo_root_dir = git.Repo(__file__, search_parent_directories=True).working_tree_dir
sys.path.append(repo_root_dir)

from ytmusicapi import YTMusic
from pathlib import Path

def get_client():
    auth_path = Path(repo_root_dir) / "oauth.json"
    return YTMusic(auth=str(auth_path))