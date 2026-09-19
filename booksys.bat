@echo off
setlocal
set "BOOKSYS_ROOT=%~dp0"
set "PYTHONPATH=%BOOKSYS_ROOT%src;%PYTHONPATH%"
python -m booksys %*
exit /b %ERRORLEVEL%
