#!/usr/bin/bash

echo "Welcome to spotify-helper. Let's get set up:"

# read in credentials
read -p "Enter your client_id: " client_id
read -p "Enter your client_secret: " client_secret

echo "CLIENT_ID=$client_id" > .env
echo "CLIENT_SECRET=$client_secret" >> .env
# this shouldn't change otherwise stuff will break
echo "REDIRECT_URI=http://localhost:8123/callback" >> .env

# create venv and install deps
python3 -m venv venv
source venv/bin/activate
poetry install

echo "All installed. Run 'spotifyhelper' to get started."