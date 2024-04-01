"""Script to get all playlists."""

from pprint import pprint
import requests
import html
import os
from dotenv import load_dotenv
from auth import get_current_user, handle_authentication


def get_playlists(access_token: str, user_id: str):
    """
    Print all playlists that a user has.
    TODO: need to handle multiple pages
    """
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url=url, headers=headers)

    print(f"Total of {response.json()['total']} playlists.")

    for index, playlist in enumerate(response.json()["items"]):
        description = playlist["description"]
        print(f"{index + 1}: {playlist['name']}")
        if description is not None:
            print(f"{html.unescape(description)}\n")


# def get_playlist(access_token: str, playlist_id: str):
#     url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
#     response = requests.get(url)


if __name__ == "__main__":
    load_dotenv()
    client_id = os.environ.get("CLIENT_ID")
    redirect_uri = os.environ.get("REDIRECT_URI")

    access_token = handle_authentication(client_id=client_id, redirect_uri=redirect_uri)
    user_response = get_current_user(access_token=access_token)

    user_id = user_response.json()["id"]
    get_playlists(access_token=access_token, user_id=user_id)
