echo [BAT] Script bat started.
@echo off
setlocal enabledelayedexpansion
set "UserName=%USERNAME%"

cd /d %~dp0

set "rootFolder=.\temp_scenario_settings\"
set "configsFolder=%rootFolder%configs\"

if not exist "%configsFolder%" (
    echo [.BAT] %configsFolder%
    echo [.BAT] O caminho da pasta não é válido.
    exit /b
)

set "countConfigFile=0"

for /f %%A in ('dir /a-d /b "%configsFolder%" ^| find /c /v ""') do set "countConfigFile=%%A"

for /f %%f in ('dir /A:-D /B "%configsFolder%"') do (
    echo ------------------"%configsFolder%%%f"------------------
    node ..\node_modules\sitespeed.io\bin\sitespeed.js --config %configsFolder%%%f %rootFolder%urls.txt    
    )
echo [BAT] Script bat ended.
endlocal