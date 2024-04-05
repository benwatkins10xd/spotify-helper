import base64
import os
from time import sleep
from fastapi import FastAPI, HTTPException
from typing import Optional
import requests
from datetime import datetime


# these come from passing --env-file to uvicorn
REDIRECT_URI = os.environ.get("REDIRECT_URI")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
CLIENT_ID = os.environ.get("CLIENT_ID")


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hola mundo"}


@app.get("/callback")
async def callback(code: Optional[str] = None, error: Optional[str] = None):

    if error is not None:
        # something like access denied
        raise HTTPException(status_code=400, detail=error)
    elif code is None:
        raise HTTPException(status_code=404, detail="No access code found.")

    # when we get our code, we need to POST to /api/token
    token_url = "https://accounts.spotify.com/api/token"
    bytes_string = f"{CLIENT_ID}:{CLIENT_SECRET}".encode()
    headers = {
        "Authorization": f"Basic {base64.b64encode(bytes_string).decode()}",
        "content-type": "application/x-www-form-urlencoded",
    }
    body = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }

    resp = requests.post(url=token_url, data=body, headers=headers)

    if not resp.status_code == 200:
        raise HTTPException(status_code=400, detail=resp.json())

    # save the access_token to a file in the project dir
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    sleep(5)
    with open(f"access-token-{timestamp}", "w") as fh:
        fh.write(resp.json()["access_token"])

    return {**resp.json()}
