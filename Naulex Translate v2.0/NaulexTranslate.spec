# -*- mode: python ; coding: utf-8 -*-
# ============================================================
#  Naulex Translate — PyInstaller Spec
#  Path src mengikuti struktur folder project yang sebenarnya:
#    ui\index.html, ui\script.js, ui\style.css
#    ui\assets\icon.png, ui\assets\Naulex.ico
# ============================================================

import os

block_cipher = None

ui_datas = [
    # (path_sumber_relatif_dari_root_project, folder_tujuan_di_dalam_exe)
    (os.path.join("ui", "index.html"),              "ui"),
    (os.path.join("ui", "script.js"),               "ui"),
    (os.path.join("ui", "style.css"),               "ui"),
    (os.path.join("ui", "assets", "icon.png"),      os.path.join("ui", "assets")),
    (os.path.join("ui", "assets", "Naulex.ico"),    os.path.join("ui", "assets")),
]

a = Analysis(
    ["main.py"],
    pathex=["."],
    binaries=[],
    datas=ui_datas,
    hiddenimports=[
        "webview",
        "webview.platforms.winforms",
        "clr",
        "deep_translator",
        "deep_translator.google",
        "keyboard",
        "pyperclip",
        "tkinter",
        "tkinter.ttk",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="Naulex Translate",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join("ui", "assets", "Naulex.ico"),
    uac_admin=True,
)
