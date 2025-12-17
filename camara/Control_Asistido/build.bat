@echo off
echo ========================================
echo   CONSTRUCTOR ControlPorGestos.exe
echo ========================================
echo.

REM Cambiar a la carpeta correcta
cd /d "C:\Users\2asir3\Desktop\Python\camara\Control_Asistido"

REM Verificar que existe el archivo
if not exist "controltotal.py" (
    echo ❌ ERROR: No se encuentra controltotal.py
    echo Archivos en la carpeta:
    dir *.py
    pause
    exit /b 1
)

if not exist "icono.ico" (
    echo ⚠️  Advertencia: No se encuentra icono.ico
    set ICON_OPTION=
) else (
    set ICON_OPTION=--icon "icono.ico"
)

echo ✅ Archivo principal: controltotal.py
if defined ICON_OPTION echo ✅ Icono: icono.ico
echo.

echo 🔨 Construyendo ejecutable...
echo.

REM Construir con PyInstaller
pyinstaller --onefile --windowed --name "ControlPorGestos" %ICON_OPTION% --clean --noconfirm controltotal.py

echo.
if exist "dist\ControlPorGestos.exe" (
    echo ✅ ¡ÉXITO! Ejecutable creado correctamente
    echo 📍 Ruta: %CD%\dist\ControlPorGestos.exe
    echo 📦 Tamaño: 
    for %%F in ("dist\ControlPorGestos.exe") do echo        %%~zF bytes (~%%~zF:1024/1024/1024^) MB
    echo.
    
    REM Preguntar si copiar al Escritorio
    set /p COPIAR="¿Copiar al Escritorio? (s/n): "
    if /i "%COPIAR%"=="s" (
        copy "dist\ControlPorGestos.exe" "%USERPROFILE%\Desktop\ControlPorGestos.exe"
        echo 📋 Copiado al Escritorio
    )
) else (
    echo ❌ ERROR: No se pudo crear el ejecutable
    echo Posibles causas:
    echo 1. PyInstaller no instalado: pip install pyinstaller
    echo 2. Permisos insuficientes (ejecuta como Administrador)
    echo 3. Errores en el código Python
)

echo.
pause