"""
Main menu and any main loops go here.

This is the entrypoint into the app
"""

import importlib
import sys
from typing import Any
import os
from dotenv import load_dotenv
import curses

from spotifyhelper.albums import print_albums
from spotifyhelper.auth import get_current_user, handle_authentication
from spotifyhelper.playlists import (
    get_playlist_strings,
    print_all_playlists,
    print_single_playlist,
)
from spotifyhelper.user import print_user

__version__ = importlib.metadata.version("spotifyhelper")


def main_menu(stdscr):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    title = f"Welcome to spotify-helper v{__version__}"
    help_text = "Navigate using the arrow keys, use Enter to select a menu."
    exit_text = "Hit escape or Ctrl+C to exit."
    stdscr.addstr(0, (width - len(title)) // 2, title)
    stdscr.addstr(1, (width - len(help_text)) // 2, help_text)
    stdscr.addstr(2, (width - len(exit_text)) // 2, exit_text)

    options = ["Playlists", "Albums", "User"]
    current_option = 0

    while True:
        stdscr.refresh()
        for index, option in enumerate(options):
            x_pos = (width - len(option)) // 2
            y_pos = height // 2 + index
            if index == current_option:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y_pos, x_pos, option)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y_pos, x_pos, option)

        key = stdscr.getch()
        if key == curses.KEY_UP:
            current_option = (current_option - 1) % len(options)
        elif key == curses.KEY_DOWN:
            current_option = (current_option + 1) % len(options)
        elif key == curses.KEY_ENTER or key in [10, 13]:
            return current_option + 1
        elif key == 27:  # escape
            sys.exit(1)


def playlist_loop(stdscr: Any, user_id: str, access_token: str):
    """Main loop for the playlist menu."""
    playlist_strings = get_playlist_strings(access_token=access_token, user_id=user_id)
    selected_row = 0
    print_all_playlists(
        stdscr=stdscr, selected_row=selected_row, playlists=playlist_strings
    )
    while True:
        key = stdscr.getch()

        if key == curses.KEY_UP and selected_row > 0:
            selected_row -= 1
        elif key == curses.KEY_DOWN and selected_row < len(playlist_strings) - 1:
            selected_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            print_single_playlist(
                stdscr=stdscr, playlist_string=playlist_strings[selected_row]
            )

        print_all_playlists(stdscr, selected_row, playlist_strings)

        if key == 27:  # escape
            main_menu_loop(stdscr, user_id=user_id, access_token=access_token)


def main_menu_loop(stdscr: Any, user_id: str, access_token: str):
    option = -1
    while option != 0:
        option = main_menu(stdscr)
        if option == 1:
            playlist_loop(stdscr=stdscr, user_id=user_id, access_token=access_token)
        elif option == 2:
            print_albums(stdscr=stdscr)
        elif option == 3:
            print_user(stdscr=stdscr)


def print_loading(stdscr: Any, status: str = "Loading..."):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    x_pos = width // 2 - len(status) // 2
    y_pos = height // 2
    curses.start_color()
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    stdscr.attron(2)
    stdscr.addstr(y_pos, x_pos, status)
    stdscr.attroff(2)


def create_app(stdscr: Any):
    load_dotenv()
    client_id = os.environ.get("CLIENT_ID")
    client_secret = os.environ.get("CLIENT_SECRET")
    redirect_uri = os.environ.get("REDIRECT_URI")

    stdscr.clear()
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    access_token = handle_authentication(
        client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri
    )
    user_response = get_current_user(access_token=access_token)

    user_id = user_response.json()["id"]
    main_menu_loop(stdscr=stdscr, user_id=user_id, access_token=access_token)


def main():
    try:
        curses.wrapper(create_app)
    except curses.error as e:
        print("Terminal is too small. Try again with a larger terminal")
        print(e)
        sys.exit(1)
