"""Methods to get and render info about user."""

from typing import Any


def print_user(stdscr: Any):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    title = "User"
    stdscr.addstr(0, (width - len(title)) // 2, title)
    stdscr.addstr(height - 3, 0, "This is not implemented yet")
    stdscr.addstr(height - 2, 0, "Press any key to return to main menu")
    stdscr.refresh()
    stdscr.getch()
