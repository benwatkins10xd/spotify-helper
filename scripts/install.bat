@echo off

echo Welcome to spotify-helper. Let's get set up:

set /p "client_id=Enter your client_id: "
set /p "client_secret=Enter your client_secret: "

echo CLIENT_ID=%client_id% > .env
echo CLIENT_SECRET=%client_secret% >> .env
REM this shouldn't change otherwise stuff will break
echo REDIRECT_URI=http://localhost:8123/callback >> .env

echo Credentials stored in .env file successfully.

echo Creating virtual environment and installing dependencies...
py -m venv venv
call venv\Scripts\activate
py -m pip install poetry
py -m poetry install

if %errorlevel% neq 0 (
    echo Installation failed. Check you have python installed correctly
    exit /b %errorlevel%
)

echo Installation complete - now activate your venv and run 'spotifyhelper'.
echo "call venv\Scripts\activate && spotifyhelper"
goto :eof
