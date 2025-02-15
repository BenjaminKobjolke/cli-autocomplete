@echo off
setlocal enabledelayedexpansion

set argCount=0
for %%x in (%*) do (
   set /A argCount+=1
   set "argVec[!argCount!]=%%~x"
   set "argVecDir[!argCount!]=%%~dpnx"
   set "argVecWOExtension[!argCount!]=%%~nx"
)

echo Number of processed arguments: %argCount%

for /L %%i in (1,1,%argCount%) do (
   echo %%i !argVecWOExtension[%%i]!
   ffmpeg -v quiet -stats -i "!argVec[%%i]!" -c:v libx265 -crf 26 -preset fast -c:a aac -b:a 64k -movflags +faststart "!argVecDir[%%i]!"_h265.mp4
   rename "!argVec[%%i]!" "!argVecWOExtension[%%i]!"_h264.mp4
)

PAUSE
