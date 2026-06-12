@echo off
:: ============================================================
::  Naulex Translate — Build Script
::  Jalankan file ini di folder project untuk membuat EXE
::  Butuh: Python 3.8+ terinstall di PATH
:: ============================================================

title Naulex Translate — Build

echo.
echo  ╔══════════════════════════════════════════════╗
echo  ║       Naulex Translate — EXE Builder         ║
echo  ║       Created by Naufal Khalil               ║
echo  ╚══════════════════════════════════════════════╝
echo.

:: ── Cek Python ──────────────────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python tidak ditemukan! Pastikan Python 3.8+ terinstall.
    pause
    exit /b 1
)

:: ── Install PyInstaller ──────────────────────────────────
echo [1/4] Menginstall PyInstaller...
pip install pyinstaller -q
if errorlevel 1 (
    echo [ERROR] Gagal install PyInstaller.
    pause
    exit /b 1
)

:: ── Install semua dependensi ─────────────────────────────
echo [2/4] Menginstall dependensi...
pip install pywebview deep-translator keyboard pyperclip -q
if errorlevel 1 (
    echo [ERROR] Gagal install dependensi.
    pause
    exit /b 1
)

:: ── Pastikan struktur folder benar ──────────────────────
echo [3/4] Memeriksa struktur folder...

if not exist "ui\index.html" (
    echo [ERROR] File ui\index.html tidak ditemukan!
    echo         Pastikan folder ui\ berisi: index.html, script.js, style.css
    pause
    exit /b 1
)
if not exist "ui\assets\Naulex.ico" (
    echo [ERROR] File ui\assets\Naulex.ico tidak ditemukan!
    pause
    exit /b 1
)
if not exist "ui\assets\icon.png" (
    echo [ERROR] File ui\assets\icon.png tidak ditemukan!
    pause
    exit /b 1
)

:: ── Build EXE ────────────────────────────────────────────
echo [4/4] Membangun EXE (ini mungkin butuh 1-3 menit)...
echo.

pyinstaller NaulexTranslate.spec --clean --noconfirm

if errorlevel 1 (
    echo.
    echo [ERROR] Build gagal! Lihat pesan error di atas.
    pause
    exit /b 1
)

echo.
echo  ╔══════════════════════════════════════════════╗
echo  ║   BUILD BERHASIL!                            ║
echo  ║   File EXE: dist\Naulex Translate.exe        ║
echo  ╚══════════════════════════════════════════════╝
echo.
echo  Saat pertama kali dijalankan:
echo  - Akan meminta izin Admin (untuk C:\Program Files)
echo  - Otomatis install library yang dibutuhkan
echo  - Membuat folder: C:\Program Files\Naulex Translate\
echo.

:: Buka folder dist
explorer dist

pause
