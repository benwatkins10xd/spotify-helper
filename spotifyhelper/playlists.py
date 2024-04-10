"""Methods for getting and handling playlists."""

import curses
import math
from typing import Any
import requests
from spotifyhelper.structs import PlaylistString


def create_playlist_list(
    playlists_dict: dict, paginated: bool = False
) -> list[PlaylistString]:
    """Creates a list of PlaylistString objects."""
    formatted_playlists = []
    if not paginated:
        for playlist in playlists_dict["items"]:
            formatted_playlists.append(
                PlaylistString(
                    name=playlist["name"],
                    description=playlist["description"],
                    tracks=playlist["tracks"]["total"],
                    href=playlist["href"],
                    open_link=playlist["external_urls"]["spotify"],
                )
            )
        return formatted_playlists

    for page in playlists_dict.keys():
        for playlist in playlists_dict[page]["items"]:
            formatted_playlists.append(
                PlaylistString(
                    name=playlist["name"],
                    description=playlist["description"],
                    tracks=playlist["tracks"]["total"],
                    href=playlist["href"],
                    open_link=playlist["external_urls"]["spotify"],
                )
            )

    return formatted_playlists


def get_playlist_strings(access_token: str, user_id: str) -> list[PlaylistString]:
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
        return create_playlist_list(playlists_dict=paginated_playlists, paginated=True)

    return create_playlist_list(playlists_dict=playlists_dict)


def print_all_playlists(
    stdscr: Any, selected_row: int, playlists: list[PlaylistString]
):
    """
    Renders all playlists to screen.
    TODO: need to handle pagination
    """
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    curses.start_color()
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)

    for idx, playlist in enumerate(playlists):
        formatted_string = f"Playlist: {playlist.name} -- {playlist.description} -- "
        tracks_string = f"Tracks: {playlist.tracks}"

        x_pos = width // 2 - len(formatted_string + tracks_string) // 2
        y_pos = height // 2 - len(playlists) // 2 + idx

        if idx == selected_row:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y_pos, x_pos, formatted_string)
            stdscr.addstr(tracks_string, curses.color_pair(2))
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y_pos, x_pos, formatted_string)
            stdscr.addstr(tracks_string, curses.color_pair(2))

    title = "spotify-helper"
    help_text = "Use arrow keys to navigate and escape to return to main."
    x_title = width // 2 - len(title) // 2
    x_help_text = width // 2 - len(help_text) // 2
    stdscr.addstr(0, x_title, title)
    stdscr.addstr(1, x_help_text, help_text)
    stdscr.refresh()


def print_single_playlist(stdscr: Any, playlist_string: PlaylistString):
    """Renders the single playlist menu to screen."""
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    stdscr.addstr(
        height // 2, (width - len(playlist_string.name)) // 2, playlist_string.name
    )
    stdscr.addstr(height - 2, 0, "Press any key to return to main menu")
    stdscr.refresh()
    stdscr.getch()
