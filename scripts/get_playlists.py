"""Script to get all playlists."""

import math
from pprint import pprint
import requests
import html
import os
from dotenv import load_dotenv
from spotifyhelper.auth import get_current_user, handle_authentication


def print_playlists(playlists_dict: dict):
    for index, playlist in enumerate(playlists_dict["items"]):
        description = playlist["description"]
        print(f"{index + 1}: {playlist['name']}")
        if description is not None:
            print(f"{html.unescape(description)}\n")


def get_playlists(access_token: str, user_id: str):
    """
    Print all playlists that a user has.

    Spotify API returns max 100 playlists in one page.
    So handle that if there's more than one page.
    """
    max_playlists_per_page = 100
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"limit": max_playlists_per_page}

    # get first page
    response = requests.get(url=url, headers=headers, params=params)
    playlists_dict = response.json()
    total_playlists = playlists_dict["total"]

    print(f"Total of {total_playlists} playlists.")

    if total_playlists > max_playlists_per_page:
        paginated_playlists = {"page_0": playlists_dict}
        num_pages = math.ceil(total_playlists / max_playlists_per_page)
        for page in range(1, num_pages):
            next_page_url = playlists_dict["next"]
            response = requests.get(url=next_page_url, headers=headers, params=params)
            playlists_dict = response.json()
            paginated_playlists[f"page_{page}"] = playlists_dict

    print_playlists(playlists_dict=playlists_dict)


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