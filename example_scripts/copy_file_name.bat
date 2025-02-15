@echo off
setlocal enabledelayedexpansion


for %%x in (%*) do (
    echo Processing: %%x
	echo %%x | clip
)
