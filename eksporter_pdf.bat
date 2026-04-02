@echo off
REM Eksporterer rapport-kapitler fra Markdown til PDF med Pandoc + XeLaTeX
REM Bruk: dobbeltklikk eller kjor fra kommandolinje

set PANDOC="%LOCALAPPDATA%\Microsoft\WinGet\Packages\JohnMacFarlane.Pandoc_Microsoft.Winget.Source_8wekyb3d8bbwe\pandoc-3.9.0.2\pandoc.exe"
set XELATEX="%LOCALAPPDATA%\Programs\MiKTeX\miktex\bin\x64\xelatex.exe"
set OUTDIR=005 report

if not exist "%OUTDIR%" mkdir "%OUTDIR%"

echo Eksporterer kapitler til PDF...

%PANDOC% "014 fase 4 - report\kap6_modell.md" -o "%OUTDIR%\kap6_modell.pdf" --pdf-engine=%XELATEX% -V geometry:margin=2.5cm -V fontsize=11pt -V mainfont="Segoe UI"
if %ERRORLEVEL% EQU 0 (echo   kap6 OK) else (echo   kap6 FEILET)

%PANDOC% "014 fase 4 - report\kap7_analyse_resultater.md" -o "%OUTDIR%\kap7_analyse_resultater.pdf" --pdf-engine=%XELATEX% -V geometry:margin=2.5cm -V fontsize=11pt -V mainfont="Segoe UI"
if %ERRORLEVEL% EQU 0 (echo   kap7 OK) else (echo   kap7 FEILET)

echo.
echo Ferdige PDF-er i %OUTDIR%\
pause
