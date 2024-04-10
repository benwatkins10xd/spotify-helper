import html


class PlaylistString:
    def __init__(self, name: str, tracks: int, description: str) -> None:
        self.name = name
        self.tracks = tracks
        if not description:
            self.description = "No description found"
        else:
            self.description = html.unescape(description)


class Colours:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"  # reset colours
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    # add more if needed
