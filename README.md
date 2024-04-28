# Useful Tools for Spotify

## Features

- Relatively intuitive UI
- Currently all you can do is list all your playlists
- Custom auth solution for CLI
- More coming soon...

## Prerequisites

- Python >=3.9 (NOTE: if you're using Windows then use >=3.9 and <=3.11)
- Git
- Poetry (`pip install poetry`)
- Spotify account (obviously)

## Setup

1. First, you need to create a Spotify application to get the required credentials. Navigate to [Spotify for Developers](https://developer.spotify.com/dashboard/create).

2. Name the app whatever you like, add a description if you want. Leave the website field blank, and add `http://localhost:8123/callback` to redirect URIs.

3. Check the Web APIs checkbox, read and accept the terms and conditions and click save. You should be able to go to your new app's settings and find the client ID and secret.

## Installation

1. Clone this repo somewhere nice:

```shell
git clone https://github.com/benwatkins10xd/spotify-helper.git
```

2. Change into project directory and run the install script for your operating system. It will prompt you for your client ID and secret you created above.

### macOS and Linux (and Windows Git bash)

```shell
cd spotify-helper && bash scripts/install.sh
```

### Windows command prompt

```shell
cd spotify-helper && scripts\install.bat
```

Activate your virtual environment and run `spotifyhelper` to get started.

## TODO

- Test suite
- Create txt file with all songs in playlist
- Create playlist using this txt file
- CRUD operations on playlists?
- Do same with albums?
- Be nice to have a nice task bar at the top with the time, current menu etc. something like spotify-helper > playlists > playlist_name
