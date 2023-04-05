@echo off

echo "BUILD DEDSEC"

auto-py-to-exe -nc -o "%~dp0\build" -c "%~dp0\configs\app.config.json" -bdo

set /p launch_y=Do you want to launch command "y"? (Y/N)
if /i "%launch_y%"=="Y" (
  auto-py-to-exe -nc -o "%~dp0\build" -c "%~dp0\configs\hwid.config.json" -bdo
)

cp "%~dp0\config.toml" "%~dp0\build"
xcopy /e /y "assets" "build/assets/"
