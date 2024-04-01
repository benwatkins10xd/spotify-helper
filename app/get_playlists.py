import requests
from requests.models import PreparedRequest
import os
import webbrowser
from dotenv import load_dotenv


def get_access_token(client_id: str, redirect_uri: str):
    base_url = "https://accounts.spotify.com/authorize"
    scope = "user-read-private user-read-email"

    params = {
        "response_type": "code",
        "client_id": client_id,
        "scope": scope,
        "redirect_uri": redirect_uri,
    }

    # put the url params in the url
    req = PreparedRequest()
    req.prepare_url(base_url, params)
    webbrowser.open_new(req.url)


def get_current_user(access_token: str):
    url = "https://api.spotify.com/v1/me"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    print(response.json())


def get_playlists(access_token: str, user_id: str):
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    response = requests.get(url)


def get_playlist(access_token: str, playlist_id: str):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    response = requests.get(url)


if __name__ == "__main__":
    load_dotenv()
    client_id = os.environ.get("CLIENT_ID")
    client_secret = os.environ.get("CLIENT_SECRET")
    redirect_uri = os.environ.get("REDIRECT_URI")

    access_token = get_access_token(client_id=client_id, redirect_uri=redirect_uri)
