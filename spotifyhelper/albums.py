"""Methods to get and render album info."""

from typing import Any


def print_albums(stdscr: Any):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    title = "Albums"
    stdscr.addstr(0, (width - len(title)) // 2, title)
    stdscr.addstr(height - 3, 0, "This is not implemented yet")
    stdscr.addstr(height - 2, 0, "Press any key to return to main menu")
    stdscr.refresh()
    stdscr.getch()
