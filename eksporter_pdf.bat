@echo off
REM ============================================================
REM Eksporter MD til PDF — LOG650 G20 Rune
REM Bruker verktoy\build_pdf.py som master-pipeline
REM ============================================================

setlocal enabledelayedexpansion

if not "%~1"=="" goto direkte

:meny
echo.
echo ===== PDF-eksport LOG650 =====
echo.
echo   1. Samlet rapport (kap 1-9 med innholdsfortegnelse)
echo   2. Alle kapitler separat
echo   3. DSB-onskeliste
echo   4. Ett spesifikt dokument (angi sti)
echo   5. Ett spesifikt sporreskjema
echo   6. Alle sporreskjemaer (AcroForm-PDF)
echo   7. Avslutt
echo.
set /p valg="Velg [1-7]: "

if "%valg%"=="1" ( python verktoy\build_pdf.py --rapport-full & goto slutt )
if "%valg%"=="2" ( python verktoy\build_pdf.py --alle-kapitler & goto slutt )
if "%valg%"=="3" ( python verktoy\build_pdf.py --dokument "analyse\DSB_onskeliste_BRIS_datauttrekk.md" --toc & goto slutt )
if "%valg%"=="4" (
    set /p fil="Angi MD-fil: "
    python verktoy\build_pdf.py --dokument "!fil!"
    goto slutt
)
if "%valg%"=="5" (
    set /p sentral="Sentralnavn (f.eks. Oslo_110): "
    python verktoy\build_pdf.py --skjema "!sentral!"
    goto slutt
)
if "%valg%"=="6" ( python verktoy\build_pdf.py --alle-skjema & goto slutt )
if "%valg%"=="7" ( goto slutt )
echo Ugyldig valg.
goto slutt

:direkte
python verktoy\build_pdf.py %*

:slutt
endlocal
pause
