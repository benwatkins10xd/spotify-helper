#!/usr/bin/bash

prompt_input() {
    read -p "$1" input
    while [[ -z "$input" ]]; do
        echo "Input cannot be empty. Please try again."
        read -p "$1" input
    done
    echo "$input"
}

echo "Welcome to spotify-helper. Let's get set up:"

client_id=$(prompt_input "Enter your client_id: ")
client_secret=$(prompt_input "Enter your client_secret: ")

# create .env
echo "CLIENT_ID=$client_id" >.env
echo "CLIENT_SECRET=$client_secret" >>.env
# this shouldn't change otherwise stuff will break
echo "REDIRECT_URI=http://localhost:8123/callback" >>.env

echo "Credentials stored in .env file successfully."

echo "Creating virtual environment and installing dependencies..."

# check if we're using windows
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    echo "using windows"
    py -m venv venv
    source venv/scripts/Activate
    py -m pip install poetry
    py -m poetry install
    if [ $? -ne 0 ]; then
        echo "Error: something bad happened when creating the venv"
        echo "Check you have Python and Poetry installed and try again"
        echo "Also check that you've added python to your PATH environment variable"
        exit 1
    fi
    echo "Installation complete - now activate your venv and run 'spotifyhelper'."
    echo "source venv/Scripts/activate && spotifyhelper"
    exit 0
fi

# otherwise create venv and install deps as normal
python3 -m venv venv
source venv/bin/activate
pip install poetry
poetry install

if [ $? -ne 0 ]; then
    echo "Error: something bad happened when creating the venv"
    echo "Check you have Python and Poetry installed and try again"
    exit 1
fi

echo "Installation complete - now activate your venv and run 'spotifyhelper'."
echo "source venv/bin/activate && spotifyhelper"
exit 0
