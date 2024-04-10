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

- Return some HTML in the fastapi app to instruct user to close the browser window or if possible automatically close it when authenticated? idk man
- Separate installation instructions for windows and mac/unix
- Test suite
- More functionality it's useless at the moment lmao
