import requests
import os
import base64


def load_dot_env():
    # beautifully custom .env loader
    if not os.path.exists(".env"):
        print("Could not find .env file.")
        return None

    with open(".env", "r") as fh:
        for line in fh.readlines():
            name, value = line.split("=", 1)
            os.environ[name] = value.strip()


def get_access_token(client_id: str, client_secret: str) -> str:
    url = "https://accounts.spotify.com/api/token"
    bytes_string = f"{client_id}:{client_secret}".encode()
    headers = {
        "Authorization": f"Basic {base64.b64encode(bytes_string).decode()}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    body = {"grant_type": "client_credentials"}
    response = requests.post(url=url, data=body, headers=headers)

    if response.status_code != 200:
        response.raise_for_status()

    access_token = response.json().get("access_token")
    print("authenticated")
    return access_token


def get_current_user(access_token: str):
    url = "https://api.spotify.com/v1/me"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    print(response.json())


def get_playlists(access_token: str, user_id: str):
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    response = requests.get(url)


def get_playlist(access_token: str, playlist_id: str):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    response = requests.get(url)


if __name__ == "__main__":
    load_dot_env()
    client_id = os.environ.get("CLIENT_ID")
    client_secret = os.environ.get("CLIENT_SECRET")

    access_token = get_access_token(client_id=client_id, client_secret=client_secret)
    get_current_user(access_token=access_token)
