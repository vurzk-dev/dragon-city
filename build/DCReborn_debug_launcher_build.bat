@echo off
title Dragon City - Debug Launcher Builder
cd /d "%~dp0"

REM ==========================================================================
REM  DRAGON CITY - BUILD LAUNCHER (ONEFILE)
REM  Version: 1.4.0  (Fix para rutas con parentesis)
REM ==========================================================================

REM ---------------------------- CONFIGURACION --------------------------------
set "NAME=DCReborn"
set "PYTHON=python"
set "HERE=%~dp0"
set "ROOT=%HERE%..\"
set "ICON=%HERE%icons\dc_icon3.ico"
set "SPEC=%HERE%spec"
set "ENTRY=%ROOT%server.py"

REM ---------------------------- TIMESTAMP ------------------------------------
set "DT="
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value 2^>nul') do set "DT=%%I"
if defined DT (
    set "TS=%DT:~0,4%-%DT:~4,2%-%DT:~6,2% %DT:~8,2%:%DT:~10,2%:%DT:~12,2%"
    set "FILE_TS=%DT:~0,4%%DT:~4,2%%DT:~6,2%_%DT:~8,2%%DT:~10,2%%DT:~12,2%"
) else (
    set "TS=0000-00-00 00:00:00"
    set "FILE_TS=00000000_000000"
)

REM ---------------------------- LOG ------------------------------------------
set "LOG_DIR=%ROOT%build\logs"
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
set "LOG_FILE=%LOG_DIR%\build_dcreborn_%FILE_TS%.log"

REM ---------------------------- BANNER ---------------------------------------
echo ==========================================
echo [INFO] [%TS%] [^>] [INICIADO] Inicializando entorno de compilacion.
echo ==========================================
echo   BAT   : %~f0
echo   ENTRY : %ENTRY%
echo   ICON  : %ICON%
echo   PYTHON: %PYTHON%
echo   LOG   : %LOG_FILE%
echo ==========================================
echo.

>  "%LOG_FILE%"  echo [INFO] [%TS%] [^>] [INICIADO] Inicializando entorno de compilacion.
>> "%LOG_FILE%" echo ==========================================
>> "%LOG_FILE%" echo BAT   : %~f0
>> "%LOG_FILE%" echo ENTRY : %ENTRY%
>> "%LOG_FILE%" echo ICON  : %ICON%
>> "%LOG_FILE%" echo PYTHON: %PYTHON%

REM ---------------------------- ENTRY POINT ----------------------------------
if not exist "%ENTRY%" goto :entry_missing
echo [INFO] [%TS%] [=] [ENCONTRADO] Entry point detectado.
>> "%LOG_FILE%" echo [INFO] [%TS%] [=] [ENCONTRADO] Entry point detectado.
goto :icon_check

:entry_missing
echo [ERROR] [%TS%] [X!] [FALLIDO] No se encontro el entry point: %ENTRY%
>> "%LOG_FILE%" echo [ERROR] [%TS%] [X!] [FALLIDO] No se encontro el entry point: %ENTRY%
pause
exit /b 1

REM ---------------------------- ICON -----------------------------------------
:icon_check
set "ICON_FLAG="
if not exist "%ICON%" goto :icon_missing
set ICON_FLAG=--icon "%ICON%"
echo [INFO] [%TS%] [=] [ENCONTRADO] Icono detectado.
>> "%LOG_FILE%" echo [INFO] [%TS%] [=] [ENCONTRADO] Icono detectado.
goto :clean

:icon_missing
echo [WARNING] [%TS%] [!] [ADVERTENCIA] Icono no encontrado, se compilara sin icono.
>> "%LOG_FILE%" echo [WARNING] [%TS%] [!] [ADVERTENCIA] Icono no encontrado.
goto :clean

REM ---------------------------- CLEAN ----------------------------------------
:clean
echo [INFO] [%TS%] [~^>] Limpiando compilaciones anteriores...
>> "%LOG_FILE%" echo [INFO] [%TS%] [~^>] Limpiando compilaciones anteriores...

if not exist "%ROOT%dist" goto :clean_spec
rmdir /S /Q "%ROOT%dist"
echo [INFO] [%TS%] [^^] [ELIMINADO] Carpeta 'dist' eliminada.
>> "%LOG_FILE%" echo [INFO] [%TS%] [^^] [ELIMINADO] Carpeta 'dist' eliminada.

:clean_spec
if not exist "%SPEC%" goto :pyInstaller
rmdir /S /Q "%SPEC%"
echo [INFO] [%TS%] [^^] [ELIMINADO] Carpeta 'spec' eliminada.
>> "%LOG_FILE%" echo [INFO] [%TS%] [^^] [ELIMINADO] Carpeta 'spec' eliminada.

REM ---------------------------- PYINSTALLER ----------------------------------
:pyInstaller
echo [INFO] [%TS%] [^>] [INICIADO] Ejecutando PyInstaller (onefile)...
>> "%LOG_FILE%" echo [INFO] [%TS%] [^>] [INICIADO] Ejecutando PyInstaller (onefile)...

if not exist "%SPEC%" mkdir "%SPEC%"

"%PYTHON%" -m PyInstaller ^
    --onefile ^
    --console ^
    --noupx ^
    --noconfirm ^
    --uac-admin ^
    %ICON_FLAG% ^
    --add-data "%ROOT%assets;assets" ^
    --add-data "%ROOT%templates;templates" ^
    --add-data "%ROOT%flash;flash" ^
    --add-data "%ROOT%web;web" ^
    --add-data "%ROOT%domains;domains" ^
    --add-data "%ROOT%villages;villages" ^
    --distpath "%ROOT%dist" ^
    --workpath "%ROOT%build" ^
    --specpath "%SPEC%" ^
    --name "%NAME%" "%ENTRY%" >> "%LOG_FILE%" 2>&1

if errorlevel 1 goto :build_failed

echo [INFO] [%TS%] [^<] [FINALIZADO] PyInstaller completado.
>> "%LOG_FILE%" echo [INFO] [%TS%] [^<] [FINALIZADO] PyInstaller completado.
goto :build_success

:build_failed
echo [ERROR] [%TS%] [X!] [FALLIDO] PyInstaller fallo.
>> "%LOG_FILE%" echo [ERROR] [%TS%] [X!] [FALLIDO] PyInstaller fallo.
echo ==========================================
type "%LOG_FILE%"
echo ==========================================
pause
exit /b 1

:build_success
echo.
echo ==========================================
echo [INFO] [%TS%] [OK] [EXITO] Compilacion completada.
echo ==========================================
echo [INFO] Log completo: %LOG_FILE%
>> "%LOG_FILE%" echo [INFO] [%TS%] [OK] [EXITO] Compilacion completada.
pause
exit /b 0