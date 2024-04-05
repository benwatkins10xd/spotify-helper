# Useful Tools for Spotify

## Prerequisites

- Python >3
- Git
- Poetry (`pip install poetry`)
- Spotify account (obviously)

## Installation and Setup

1. First, you need to create a Spotify application to get the required credentials. Navigate to [Spotify for Developers](https://developer.spotify.com/dashboard/create).

2. Name the app whatever you like, add a description if you want. Leave the website field blank, and add `http://localhost:8123/callback` to redirect URIs.

3. Check the Web APIs checkbox, read and accept the terms and conditions and click save. You should be able to go to your new app's settings and find the client ID and secret.

4. Now, clone this repo somewhere nice: `git clone https://github.com/benwatkins10xd/spotify-helper.git`

5. Change into project directory: `cd spotify-helper`

6. Create a virtual environment in this directory: `python3 -m venv venv`

7. Create a .env file in this directory to store your credentials:

```shell
echo "CLIENT_ID=
CLIENT_SECRET=
REDIRECT_URI=http://localhost:8123/callback" > .env
```

8. Open the .env file and add your client ID and secret from your Spotify app's dashboard, and save it

9. Activate the virtual environment: `source venv/bin/activate` or `./venv/Scripts/Activate` for Windows

10. Install dependencies and spotify-helper: `poetry install`

All installed!

## Running

1. With the virtual environment activated, run `uvicorn spotifyhelper.webserver:app --reload --port 8123 --env-file=.env`.
2. This will start the uvicorn webserver and search for incoming requests.
3. Then, run one of the scripts in the `scripts/` directory to use the actual functions, e.g. `python3 scripts/get_playlists.py`

## TODO

- Use argparse or similar rather than python3 scripts/get...
- Can we start the fastapi & uvicorn server only when we need to make an auth request? Might save a lot of hassle setting everything up.
- Separate installation instructions for windows and mac/unix
