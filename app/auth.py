import os
import re
import time
import webbrowser
from fastapi import HTTPException
from requests import PreparedRequest
import requests


def watch_directory_for_files(regex_pattern: re.Pattern) -> str:
    """
    Watch the project directory for files
    matching a regular expression pattern.
    """

    initial_files = os.listdir()

    while True:
        current_files = os.listdir()

        new_files = [
            file
            for file in current_files
            if re.match(regex_pattern, file) and file not in initial_files
        ]

        if new_files:
            return new_files[0]

        # update files list and wait a bit
        initial_files = current_files
        time.sleep(1)


def send_auth_request(client_id: str, redirect_uri: str) -> None:
    """
    Sends initial request to Spotify API for an access
    token, and prompts user to authorize using their
    browser.

    Does not return anything, the authorization logic is
    handled by the FastAPI app running, which creates a file
    containing the access token.
    """
    base_url = "https://accounts.spotify.com/authorize"
    scope = "user-read-private user-read-email"

    params = {
        "response_type": "code",
        "client_id": client_id,
        "scope": scope,
        "redirect_uri": redirect_uri,
    }

    # TODO: check if fastapi is running and only send request if it is?
    # put the url params in the url
    req = PreparedRequest()
    req.prepare_url(base_url, params)
    webbrowser.open_new(req.url)


def create_access_token(
    client_id: str, redirect_uri: str, file_regex: re.Pattern
) -> str:
    """
    Sends the initial auth request and waits until we
    find an access token file. Returns the contents of
    the access token file, which is our token.
    """
    send_auth_request(client_id=client_id, redirect_uri=redirect_uri)
    # we wait here until we get a new access_token file
    file_path = watch_directory_for_files(file_regex)
    with open(file_path, "r") as fh:
        return fh.read()


def get_current_user(access_token: str) -> requests.Response:
    """
    Gets current user.

    Useful to check if we're logged in correctly
    """
    url = "https://api.spotify.com/v1/me"
    headers = {"Authorization": f"Bearer {access_token}"}
    return requests.get(url, headers=headers)


def handle_authentication(client_id: str, redirect_uri: str) -> str:
    """
    Handles the entire e2e auth flow. Just give it the
    client id and redirect uri and it'll return the access token.
    """

    file_regex = re.compile(r"access-token-\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}")

    # first check if we have an access_token file
    is_access_token_found = False

    for file in os.listdir():
        if not file_regex.match(file):
            continue
        is_access_token_found = True
        access_token_file = file

    # if we don't, we create one
    if not is_access_token_found:
        return create_access_token(
            client_id=client_id, redirect_uri=redirect_uri, file_regex=file_regex
        )

    # if we do, check if it's valid and return access_token
    with open(access_token_file, "r") as fh:
        access_token = fh.read()
    response = get_current_user(access_token=access_token)
    if response.status_code == 200:
        return access_token

    # if it's not valid we delete it and request a new one
    os.remove(access_token_file)
    return create_access_token(
        client_id=client_id, redirect_uri=redirect_uri, file_regex=file_regex
    )
