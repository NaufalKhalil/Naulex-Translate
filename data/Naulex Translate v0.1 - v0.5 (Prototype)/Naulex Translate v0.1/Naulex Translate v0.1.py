"""
Naulex Translate Prototype v0.1

=> Added :
- Auto translate selected text using Google Translate.
- Translation triggered with F2 hotkey.
- Dark-themed CustomTkinter interface.
- Language selection panel.
- Search language feature.
- Favorite language system.
- Terminal log panel.
- Responsive language grid layout.
- Persistent favorite language storage (favorites.json).
- Automatic dependency installer.

=> Notes :
- Basic proof-of-concept release.
- Fixed shortcut and language settings were not yet configurable.
"""


import subprocess
import sys

REQUIRED_PACKAGES = [
    "customtkinter",
    "deep-translator",
    "keyboard",
    "pyperclip",
    "Pillow",
]

def install_missing():
    for pkg in REQUIRED_PACKAGES:
        try:
            __import__(pkg.replace("-", "_").split("[")[0])
        except ImportError:
            print(f"[INSTALL] Installing {pkg}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])

install_missing()

# =========================
# IMPORTS
# =========================
import time
import json
import os
import threading
import time
import tkinter as tk

import customtkinter as ctk
import keyboard
import pyperclip
from PIL import Image


# =========================
# KONSTANTA UKURAN & WARNA
# =========================

# -- Window --
WIN_WIDTH       = 1200
WIN_HEIGHT      = 700
WIN_MIN_W       = 640
WIN_MIN_H       = 480
SASH_RATIO      = 0.72          # porsi lebar panel kiri (0.0 – 1.0)

# -- Header --
HEADER_HEIGHT   = 45
HEADER_FONT     = ("Consolas", 15, "bold")
HEADER_ICON_SZ  = (18, 18)

# -- Topbar (tab + search) --
TOPBAR_PAD_X    = 12
TOPBAR_PAD_Y_T  = 10
TOPBAR_PAD_Y_B  = 6
TAB_BTN_W       = 55
TAB_BTN_H       = 32
FAV_BTN_W       = 78
FAV_BTN_H       = 32
TAB_FONT        = ("Consolas", 12, "bold")
FAV_FONT        = ("Consolas", 12)
SEARCH_H        = 32
SEARCH_FONT     = ("Consolas", 12)
SEARCH_ICON_SZ  = (16, 16)

# -- Language Buttons --
LANG_BTN_H      = 45
LANG_BTN_FONT   = ("Consolas", 12)
LANG_BTN_RADIUS = 8
LANG_PAD_X      = 4
LANG_PAD_Y      = 4
LANG_FRAME_PX   = 12
LANG_FRAME_PY_B = 10

# -- Terminal --
TERM_FONT       = ("Consolas", 12)
TERM_HEADER_PX  = 12
TERM_HEADER_PY  = (10, 4)
TERM_ICON_SZ    = (18, 18)
TERM_HEADER_FONT= ("Consolas", 14, "bold")
TERM_PX         = 12
TERM_PY         = (0, 6)
STATUS_FONT     = ("Consolas", 11)
STATUS_PX       = 14
STATUS_PY       = (2, 10)

# -- Grid breakpoints (lebar left_frame → jumlah kolom) --
GRID_COLS       = [(300, 2), (500, 2), (700, 3)]   # (max_width, cols)
GRID_COLS_DEF   = 4                                 # kolom default jika > semua threshold
RESIZE_DEBOUNCE = 100                               # ms debounce untuk resize

# -- Warna --
C_BG            = "#0d0d0d"
C_PANEL         = "#111111"
C_BTN           = "#1a1a1a"
C_BTN_HOVER     = "#2a2a2a"
C_BTN_BORDER    = "#333333"
C_BTN_SEL_FG    = "white"
C_BTN_SEL_TXT   = "black"
C_SASH          = "#2a2a2a"
C_TERM_BG       = "#0a0a0a"
C_TERM_TXT      = "#e0e0e0"
C_TERM_BORDER   = "#222222"
C_SCROLL_BTN    = "#444444"
C_SCROLL_HOVER  = "#666666"
C_STATUS_TXT    = "white"
C_WHITE         = "white"
C_TEXT          = "white"

# -- File paths --
FAVORITES_FILE  = "favorites.json"
ICON_APP        = "icons/Naulex.ico"
ICON_TRANSLATE  = "icons/translate_icon.png"
ICON_SEARCH     = "icons/search_icon.png"
ICON_TERMINAL   = "icons/terminal_icon.png"


# =========================
# DAFTAR BAHASA
# =========================

LANGUAGES = {
    "English": "en", "Indonesia": "id", "Mandarin Chinese": "zh-CN",
    "Arabic": "ar", "Japanese": "ja", "Spanish": "es", "Portuguese": "pt",
    "French": "fr", "German": "de", "Italian": "it", "Russian": "ru",
    "Korean": "ko", "Thai": "th", "Vietnamese": "vi", "Hindi": "hi",
    "Dutch": "nl", "Turkish": "tr", "Polish": "pl", "Persian": "fa",
    "Malay": "ms", "Bengali": "bn", "Filipino": "tl", "Czech": "cs",
    "Urdu": "ur", "Swahili": "sw", "Romanian": "ro", "Punjabi": "pa",
    "Hausa": "ha", "Hungarian": "hu", "Tamil": "ta", "Amharic": "am",
    "Greek": "el", "Telugu": "te", "Hebrew": "iw", "Swedish": "sv",
    "Marathi": "mr", "Serbian": "sr", "Norwegian": "no", "Ukrainian": "uk",
    "Bulgarian": "bg", "Danish": "da", "Slovak": "sk", "Finnish": "fi",
    "Croatian": "hr",
}


# =========================
# HELPERS
# =========================

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def load_icon(path, size=(20, 20)):
    try:
        image = Image.open(resource_path(path)).convert("RGBA")
        return ctk.CTkImage(light_image=image, size=size)
    except Exception:
        return None


# =========================
# FAVORITES PERSISTENCE
# =========================

def load_favorites():
    try:
        with open(FAVORITES_FILE, "r") as f:
            return set(json.load(f))
    except Exception:
        return set()


def save_favorites(fav_set):
    try:
        with open(FAVORITES_FILE, "w") as f:
            json.dump(list(fav_set), f)
    except Exception:
        pass


# =========================
# STATE
# =========================

selected_lang   = "en"
favorites       = load_favorites()
current_filter  = "all"
current_menu    = None
buttons         = {}
_resize_after   = [None]


# =========================
# UI SETUP
# =========================

ctk.set_appearance_mode("dark")

root = ctk.CTk()
root.title("Naulex Translate")
root.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")
root.minsize(WIN_MIN_W, WIN_MIN_H)
root.configure(fg_color=C_BG)

# App icon
try:
    root.iconbitmap(resource_path(ICON_APP))
except Exception:
    pass


# =========================
# TERMINAL LOG
# =========================

def log(msg):
    terminal.configure(state="normal")
    terminal.insert("end", msg + "\n")
    terminal.see("end")
    terminal.configure(state="disabled")


# =========================
# PILIH BAHASA
# =========================

def select_language(name):
    global selected_lang
    selected_lang = LANGUAGES[name]
    for btn_name, btn in buttons.items():
        if btn_name == name:
            btn.configure(fg_color=C_BTN_SEL_FG, text_color=C_BTN_SEL_TXT, border_width=0)
        else:
            btn.configure(fg_color=C_BTN, text_color=C_TEXT,
                          border_color=C_BTN_BORDER, border_width=1)
    status_label.configure(text=f"Target Language : {name}")
    log(f"[INFO] Language selected: {name}")


# =========================
# FAVORITE
# =========================

def toggle_favorite(name):
    if name in favorites:
        favorites.remove(name)
        log(f"[INFO] Removed from favorites: {name}")
    else:
        favorites.add(name)
        log(f"[INFO] Added to favorites: {name}")
    save_favorites(favorites)
    refresh_grid()


def show_context_menu(event, lang_name):
    global current_menu
    if current_menu and current_menu.winfo_exists():
        current_menu.destroy()

    menu = ctk.CTkToplevel(root)
    current_menu = menu
    menu.overrideredirect(True)
    menu.attributes("-topmost", True)
    menu.geometry(f"120x35+{event.x_root}+{event.y_root}")

    text = "Unfavorite" if lang_name in favorites else "Favorite"

    def on_click():
        global current_menu
        toggle_favorite(lang_name)
        if menu.winfo_exists():
            menu.destroy()
        current_menu = None

    ctk.CTkButton(
        menu, text=text,
        fg_color=C_BTN, hover_color=C_BTN_HOVER,
        text_color=C_TEXT, border_color=C_BTN_BORDER,
        border_width=1, corner_radius=6, command=on_click
    ).pack(fill="both", expand=True)


def close_current_menu(event=None):
    global current_menu
    if current_menu and current_menu.winfo_exists():
        current_menu.destroy()
    current_menu = None


root.bind_all("<Button-1>", lambda e: root.after(10, close_current_menu))


# =========================
# TRANSLATE
# =========================

def do_translate():
    try:
        from deep_translator import GoogleTranslator
        keyboard.press_and_release('ctrl+a')
        time.sleep(0.1)
        keyboard.press_and_release('ctrl+c')
        time.sleep(0.15)

        text = pyperclip.paste()
        if not text.strip():
            return

        translated = GoogleTranslator(source='auto', target=selected_lang).translate(text)
        pyperclip.copy(translated)
        time.sleep(0.1)
        keyboard.press_and_release('ctrl+v')

        code = selected_lang.upper().split("-")[0]
        log(f"Asli: {text}")
        log(f"{code}   : {translated}")
        log("─" * 30)
        log("")
    except Exception as e:
        log(f"[ERROR] {e}")


# =========================
# HOTKEY THREAD
# =========================

def hotkey_loop():
    log("[INFO] Naulex version 1.0")
    time.sleep(0.5) 
    log("[INFO] Naulex is running...")
    time.sleep(0.5) 
    log("[INFO] Welcome to Naulex Auto Translate 🌍")
    time.sleep(0.5)
    log("[INFO] Created by Naufal Khalil")
    time.sleep(0.5)
    log("[INFO] Select your target language on the left panel")
    time.sleep(0.5)
    log("[INFO] Press F2 to auto translate & replace")
    log("")

    while True:
        try:
            if keyboard.is_pressed("F2"):
                do_translate()
                while keyboard.is_pressed("F2"):
                    time.sleep(0.05)
            time.sleep(0.05)
        except Exception:
            pass


# =========================
# RESPONSIVE GRID
# =========================

def get_column_count():
    try:
        w = left_frame.winfo_width()
    except Exception:
        w = 600
    for max_w, cols in GRID_COLS:
        if w < max_w:
            return cols
    return GRID_COLS_DEF


def refresh_grid():
    search_text = search_var.get().lower()
    cols = get_column_count()

    for c in range(10):
        lang_frame.grid_columnconfigure(c, weight=0, minsize=0)
    for c in range(cols):
        lang_frame.grid_columnconfigure(c, weight=1)

    row = col = 0
    for name, btn in buttons.items():
        label = f"★ {name}" if name in favorites else name
        btn.configure(text=label)

        show = True
        if search_text and search_text not in name.lower():
            show = False
        if current_filter == "favorite" and name not in favorites:
            show = False

        if show:
            btn.grid(row=row, column=col,
                     padx=LANG_PAD_X, pady=LANG_PAD_Y, sticky="ew")
            col += 1
            if col >= cols:
                col = 0
                row += 1
        else:
            btn.grid_remove()


def set_filter(mode):
    global current_filter
    current_filter = mode
    if mode == "all":
        btn_all.configure(fg_color=C_WHITE, text_color="black")
        btn_fav.configure(fg_color="transparent", text_color=C_TEXT)
    else:
        btn_fav.configure(fg_color=C_WHITE, text_color="black")
        btn_all.configure(fg_color="transparent", text_color=C_TEXT)
    refresh_grid()


# =========================
# RESIZE (debounced)
# =========================

def on_resize(event):
    if _resize_after[0]:
        root.after_cancel(_resize_after[0])
    _resize_after[0] = root.after(RESIZE_DEBOUNCE, refresh_grid)


# =========================
# LAYOUT
# =========================

# ── Header ─────────────────────────────────────────

header_frame = ctk.CTkFrame(root, fg_color=C_BG, height=HEADER_HEIGHT)
header_frame.pack(fill="x")
header_frame.pack_propagate(False)

icon_img   = load_icon(ICON_TRANSLATE, HEADER_ICON_SZ)
icon_label = ctk.CTkLabel(
    header_frame,
    image=icon_img,
    text="  Select Language",
    compound="left",
    font=HEADER_FONT,
    text_color=C_WHITE,
    anchor="w",
)
icon_label.image = icon_img
icon_label.pack(side="left", padx=20, pady=0, fill="y")

# ── Paned container ────────────────────────────────

paned = ctk.CTkFrame(root, fg_color=C_BG)
paned.pack(fill="both", expand=True)

sash_pane = tk.PanedWindow(
    paned,
    orient=tk.HORIZONTAL,
    bg=C_SASH,
    sashwidth=5,
    sashpad=0,
    sashrelief="flat",
    handlesize=0,
    showhandle=False,
    opaqueresize=False,   # non-opaque → lebih ringan saat drag
    bd=0,
)
sash_pane.pack(fill="both", expand=True)

# ── Left panel ─────────────────────────────────────

left_outer = tk.Frame(sash_pane, bg=C_PANEL, bd=0)
sash_pane.add(left_outer, minsize=220, stretch="always")

left_frame = ctk.CTkFrame(left_outer, fg_color=C_PANEL, corner_radius=0)
left_frame.pack(fill="both", expand=True)

topbar_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
topbar_frame.pack(fill="x", padx=TOPBAR_PAD_X,
                  pady=(TOPBAR_PAD_Y_T, TOPBAR_PAD_Y_B))

btn_all = ctk.CTkButton(
    topbar_frame, text="All",
    width=TAB_BTN_W, height=TAB_BTN_H,
    fg_color=C_WHITE, text_color="black",
    hover_color="#dddddd", corner_radius=20,
    font=TAB_FONT, command=lambda: set_filter("all")
)
btn_all.pack(side="left", padx=(0, 5))

btn_fav = ctk.CTkButton(
    topbar_frame, text="Favorite",
    width=FAV_BTN_W, height=FAV_BTN_H,
    fg_color="transparent", text_color=C_TEXT,
    hover_color=C_BTN_HOVER, border_color="#444444",
    border_width=1, corner_radius=20,
    font=FAV_FONT, command=lambda: set_filter("favorite")
)
btn_fav.pack(side="left", padx=(0, 8))

search_frame = ctk.CTkFrame(topbar_frame, fg_color=C_BTN,
                             corner_radius=20, height=SEARCH_H)
search_frame.pack(side="left", fill="x", expand=True)
search_frame.pack_propagate(False)

search_img  = load_icon(ICON_SEARCH, SEARCH_ICON_SZ)
search_icon = ctk.CTkLabel(
    search_frame,
    image=search_img if search_img else None,
    text="" if search_img else "🔍"
)
if search_img:
    search_icon.image = search_img
search_icon.pack(side="left", padx=(8, 0))

search_var   = ctk.StringVar()
search_entry = ctk.CTkEntry(
    search_frame,
    placeholder_text="Search",
    textvariable=search_var,
    border_width=0,
    fg_color="transparent",
    text_color=C_WHITE,
    placeholder_text_color="#555555",
    font=SEARCH_FONT,
    height=30,
)
search_entry.pack(fill="x", padx=(2, 8), pady=1)
search_var.trace_add("write", lambda *_: refresh_grid())

# Language grid — scrollbar selalu terlihat (tidak di-hide)
lang_frame = ctk.CTkScrollableFrame(
    left_frame,
    fg_color="transparent",
    scrollbar_button_color=C_SCROLL_BTN,
    scrollbar_button_hover_color=C_SCROLL_HOVER,
)
lang_frame.pack(fill="both", expand=True,
                padx=LANG_FRAME_PX, pady=(0, LANG_FRAME_PY_B))

# Buat tombol bahasa
for name in LANGUAGES:
    btn = ctk.CTkButton(
        lang_frame,
        text=name,
        height=LANG_BTN_H,
        fg_color=C_BTN,
        text_color=C_TEXT,
        hover_color=C_BTN_HOVER,
        border_color=C_BTN_BORDER,
        border_width=1,
        corner_radius=LANG_BTN_RADIUS,
        font=LANG_BTN_FONT,
        command=lambda n=name: select_language(n),
    )
    buttons[name] = btn
    btn.bind("<ButtonRelease-3>", lambda e, lang=name: show_context_menu(e, lang))

# ── Right panel ────────────────────────────────────

right_outer = tk.Frame(sash_pane, bg=C_PANEL, bd=0)
sash_pane.add(right_outer, minsize=200, stretch="never")

right_frame = ctk.CTkFrame(right_outer, fg_color=C_PANEL, corner_radius=0)
right_frame.pack(fill="both", expand=True)

terminal_header = ctk.CTkFrame(right_frame, fg_color="transparent",
                                height=HEADER_HEIGHT)
terminal_header.pack(fill="x", padx=TERM_HEADER_PX, pady=TERM_HEADER_PY)
terminal_header.pack_propagate(False)

terminal_img  = load_icon(ICON_TERMINAL, TERM_ICON_SZ)
terminal_icon = ctk.CTkLabel(
    terminal_header,
    image=terminal_img if terminal_img else None,
    text="  Terminal",
    compound="left",
    font=TERM_HEADER_FONT,
    text_color=C_WHITE,
    anchor="w",
)
if terminal_img:
    terminal_icon.image = terminal_img
terminal_icon.pack(side="left", fill="y")

terminal = ctk.CTkTextbox(
    right_frame,
    font=TERM_FONT,
    fg_color=C_TERM_BG,
    text_color=C_TERM_TXT,
    corner_radius=6,
    border_width=1,
    border_color=C_TERM_BORDER,
    wrap="word",
    scrollbar_button_color=C_SCROLL_BTN,
    scrollbar_button_hover_color=C_SCROLL_HOVER,
)
terminal.pack(fill="both", expand=True, padx=TERM_PX, pady=TERM_PY)
terminal.configure(state="disabled")

status_label = ctk.CTkLabel(
    right_frame,
    text="Target Language : English",
    font=STATUS_FONT,
    text_color=C_STATUS_TXT,
    anchor="w",
)
status_label.pack(anchor="w", padx=STATUS_PX, pady=STATUS_PY)


# =========================
# INIT SETELAH WINDOW SIAP
# =========================

def _after_map():
    root.bind("<Configure>", on_resize)
    refresh_grid()
    root.after(100, lambda: sash_pane.sash_place(
        0, int(root.winfo_width() * SASH_RATIO), 0))

root.after(150, _after_map)

select_language("English")
threading.Thread(target=hotkey_loop, daemon=True).start()
root.mainloop()
