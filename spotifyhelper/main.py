"""Script to get all playlists."""

import math
import sys
import requests
import html
import os
from dotenv import load_dotenv
import curses

from spotifyhelper.auth import get_current_user, handle_authentication
from spotifyhelper.colours import bcolours


def create_playlist_string_with_ansi_colours(playlist: dict) -> str:
    name = playlist["name"]
    description = playlist["description"]
    total_tracks = playlist["tracks"]["total"]
    complete_string = f"{bcolours.OKGREEN}Playlist:{bcolours.ENDC} {name} -- {bcolours.OKCYAN}{total_tracks}{bcolours.ENDC} tracks -- "

    if description:
        complete_string += f"{html.unescape(description)}"
    else:
        complete_string += f"{bcolours.OKBLUE}No description found.{bcolours.ENDC}"
    return complete_string


def create_playlist_string(playlist: dict) -> str:
    name = playlist["name"]
    description = playlist["description"]
    total_tracks = playlist["tracks"]["total"]
    complete_string = f"Playlist: {name} -- {total_tracks} tracks -- "

    if description:
        complete_string += f"{html.unescape(description)}"
    else:
        complete_string += f"No description found."
    return complete_string


def print_playlists(playlists_dict: dict, paginated: bool = False) -> None:
    formatted_playlists = []
    if not paginated:
        for playlist in playlists_dict["items"]:
            formatted_playlists.append(create_playlist_string(playlist=playlist))
        return formatted_playlists

    for page in playlists_dict.keys():
        print(f"{bcolours.OKCYAN}{page}{bcolours.ENDC}")
        for playlist in playlists_dict[page]["items"]:
            formatted_playlists.append(create_playlist_string(playlist=playlist))

    return formatted_playlists


def get_playlist_strings(access_token: str, user_id: str):
    """
    Print all playlists that a user has.

    Spotify API returns max 100 playlists in one page.
    So handle that if there's more than one page.
    """
    max_playlists_per_page = 10
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
        return print_playlists(playlists_dict=paginated_playlists, paginated=True)

    return print_playlists(playlists_dict=playlists_dict)


# def get_playlist(access_token: str, playlist_id: str):
#     url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
#     response = requests.get(url)


def print_loading(screen, status: str = "Loading..."):
    screen.clear()
    h, w = screen.getmaxyx()
    x = w // 2 - len(status) // 2
    y = h // 2
    screen.addstr(y, x, status)


def print_menu(screen, selected_row, playlists):
    screen.clear()
    h, w = screen.getmaxyx()

    for idx, playlist in enumerate(playlists):
        x = w // 2 - len(playlist) // 2
        y = h // 2 - len(playlists) // 2 + idx
        if idx == selected_row:
            screen.attron(curses.color_pair(1))
            screen.addstr(y, x, playlist)
            screen.attroff(curses.color_pair(1))
        else:
            screen.addstr(y, x, playlist)

    title = "spotify-helper"
    help_text = "Use arrow keys to navigate and escape to exit."
    x_title = w // 2 - len(title) // 2
    x_help_text = w // 2 - len(help_text) // 2
    screen.addstr(0, x_title, title)
    screen.addstr(1, x_help_text, help_text)
    screen.refresh()


def create_app(screen):
    load_dotenv()
    client_id = os.environ.get("CLIENT_ID")
    client_secret = os.environ.get("CLIENT_SECRET")
    redirect_uri = os.environ.get("REDIRECT_URI")

    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    print_loading(screen)

    access_token = handle_authentication(
        client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri
    )
    user_response = get_current_user(access_token=access_token)

    user_id = user_response.json()["id"]
    playlist_strings = get_playlist_strings(access_token=access_token, user_id=user_id)

    current_row = 0
    print_menu(screen, current_row, playlist_strings)

    while True:
        key = screen.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(playlist_strings) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            # Handle selection (e.g., print selected playlist)
            screen.clear()
            screen.addstr(0, 0, f"Selected playlist: {playlist_strings[current_row]}")
            screen.refresh()

        print_menu(screen, current_row, playlist_strings)

        if key == 27:  # escape
            sys.exit(0)


def main():
    try:
        curses.wrapper(create_app)
    except curses.error as e:
        print("Terminal is too small. Try again with a larger terminal")
        print(e)
        sys.exit(1)
