
REM As per https://deric.github.io/DaVinciResolve-API-Docs/#using-a-script
SET RESOLVE_SCRIPT_API="%PROGRAMDATA%\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\"
echo %RESOLVE_SCRIPT_API%

SET RESOLVE_SCRIPT_LIB="C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
echo %RESOLVE_SCRIPT_LIB%

SET PYTHONPATH="%PYTHONPATH%;%RESOLVE_SCRIPT_API%\Modules\"
echo %PYTHONPATH%

REM Must use Python 3.6
py -3.6 main.py 