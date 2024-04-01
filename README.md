# Useful Tools for Spotify

## Prerequisites

- Python >3
- Poetry (`pip install poetry`)

## Installation

1. Create a virtual environment in project directory: `python3 -m venv venv`
2. Activate the virtual environment: `source venv/bin/activate`
3. Install dependencies: `poetry install`

## Running

1. With the virtual environment activated, run `uvicorn app.webserver.main:app --reload --port 8123`.
2. This will start the uvicorn webserver and search for incoming requests.
3. Then, run one of the scripts in the `app/` directory to use the actual app.
