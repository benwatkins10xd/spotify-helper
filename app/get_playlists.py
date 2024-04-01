"""Script to get all playlists."""

import requests
import os
from dotenv import load_dotenv
import sys
from auth import handle_authentication


def get_playlists(access_token: str, user_id: str):
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    response = requests.get(url)


def get_playlist(access_token: str, playlist_id: str):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    response = requests.get(url)


if __name__ == "__main__":
    load_dotenv()
    client_id = os.environ.get("CLIENT_ID")
    # client_secret = os.environ.get("CLIENT_SECRET")
    redirect_uri = os.environ.get("REDIRECT_URI")
    access_token = handle_authentication(client_id=client_id, redirect_uri=redirect_uri)
    # TODO: wtf is the user_id
    get_playlists(
        access_token=access_token,
    )
