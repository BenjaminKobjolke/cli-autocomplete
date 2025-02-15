@echo off
setlocal enabledelayedexpansion

set "counter=1"

:checkFile
if exist %1\dummy_!counter!.jpg (
    set /a counter+=1
    goto checkFile
)

curl -L -o %1\dummy_!counter!.jpg https://picsum.photos/1920/1080
