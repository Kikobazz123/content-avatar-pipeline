@echo off
REM make.bat - build one episode end to end.
REM
REM   make.bat day01
REM
REM Expects:  days\day01\me.mp4       (you talking; Me.MOV / .mov / .MOV also work)
REM Optional: days\day01\screen.mp4   (screen recording - strongly recommended)
REM Optional: days\day01\script.txt   (what you actually said - fixes caption wording)
REM Produces: days\day01\out.mp4
REM
REM The scripts live in the avatar-video-engine skill, not in this folder, so
REM every project shares one copy and fixes land everywhere at once.
REM
REM Uses "py -3.10" on purpose: the plain "python" on this machine points at an
REM unrelated project's virtualenv that has no faster-whisper installed.
REM
REM Keep this file pure ASCII. cmd.exe mis-parses non-ASCII characters such as
REM em dashes in its default codepage and reports bogus "not recognized" errors.

setlocal enabledelayedexpansion
if "%~1"=="" (
  echo Usage: make.bat ^<day-folder^>     e.g.  make.bat day01
  exit /b 1
)

set "HERE=%~dp0"
set "DIR=%HERE%days\%~1"
set "SKILL=%USERPROFILE%\.claude\skills\avatar-video-engine\scripts"

if not exist "%SKILL%\captions.py" (
  echo [x] avatar-video-engine skill not found at "%SKILL%"
  exit /b 1
)

REM Cameras name files Me.MOV / IMG_1234.MOV, not me.mp4. Checking real
REM extensions here is why "make.bat day01" failed silently before.
set "ME="
for %%E in (mp4 MP4 mov MOV m4v) do (
  if not defined ME if exist "%DIR%\me.%%E" set "ME=%DIR%\me.%%E"
  if not defined ME if exist "%DIR%\Me.%%E" set "ME=%DIR%\Me.%%E"
)
if not defined ME (
  echo [x] No talking-head clip in "%DIR%"
  echo     Looked for me/Me with extension mp4, mov, m4v.
  exit /b 1
)

set "SCREEN="
for %%E in (mp4 MP4 mov MOV) do (
  if not defined SCREEN if exist "%DIR%\screen.%%E" set "SCREEN=%DIR%\screen.%%E"
  if not defined SCREEN if exist "%DIR%\Screen.%%E" set "SCREEN=%DIR%\Screen.%%E"
)

echo.
echo Talking head: !ME!
if defined SCREEN echo Screen      : !SCREEN!

echo.
echo [1/2] Captions from your audio...
REM --cache keeps the transcript so a re-run that only changes styling is instant.
if exist "%DIR%\script.txt" (
  py -3.10 "%SKILL%\captions.py" "!ME!" -o "%DIR%\captions.ass" --script "%DIR%\script.txt" --model small --cache "%DIR%\transcript.json"
) else (
  py -3.10 "%SKILL%\captions.py" "!ME!" -o "%DIR%\captions.ass" --model small --cache "%DIR%\transcript.json"
)
if errorlevel 1 (
  echo.
  echo     Captions failed. If it reported a low match ratio, script.txt does not
  echo     match what was actually said - fix the script, do not pass --force.
  exit /b 1
)

echo.
echo [2/2] Composing 1080x1920...
if defined SCREEN (
  py -3.10 "%SKILL%\compose.py" --top "!SCREEN!" --bottom "!ME!" --captions "%DIR%\captions.ass" -o "%DIR%\out.mp4"
) else (
  echo     [!] No screen recording found - building talking-head only.
  echo         Both reference videos keep a screen recording up the whole way through.
  py -3.10 "%SKILL%\compose.py" --bottom "!ME!" --captions "%DIR%\captions.ass" -o "%DIR%\out.mp4"
)
if errorlevel 1 exit /b 1

echo.
echo Done. Output: %DIR%\out.mp4
echo Watch it before posting. Check the first 3 seconds especially.
echo Read any WARNING above - upscale and crop warnings are why day01 looked soft.
endlocal
