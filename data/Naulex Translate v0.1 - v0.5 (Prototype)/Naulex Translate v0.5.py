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
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", pkg, "-q"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

install_missing()

# =========================
# IMPORTS
# =========================
import json
import os
import threading
import time
import tkinter as tk
from datetime import date

import customtkinter as ctk
import keyboard
import pyperclip
from PIL import Image
# FIX #3: Import di level modul, bukan di dalam fungsi
from deep_translator import GoogleTranslator

# =========================
# KONSTANTA UKURAN & WARNA
# =========================

WIN_WIDTH       = 1200
WIN_HEIGHT      = 700
WIN_MIN_W       = 640
WIN_MIN_H       = 480
SASH_RATIO      = 0.72

HEADER_HEIGHT   = 45
HEADER_FONT     = ("Consolas", 15, "bold")
HEADER_ICON_SZ  = (18, 18)

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

LANG_BTN_H      = 45
LANG_BTN_FONT   = ("Consolas", 12)
LANG_BTN_RADIUS = 8
LANG_PAD_X      = 4
LANG_PAD_Y      = 4
LANG_FRAME_PX   = 12
LANG_FRAME_PY_B = 10

TERM_FONT       = ("Consolas", 12)
TERM_HEADER_PX  = 12
TERM_HEADER_PY  = (10, 4)
TERM_ICON_SZ    = (18, 18)
TERM_HEADER_FONT= ("Consolas", 14, "bold")
TERM_PX         = 12
TERM_PY         = (0, 6)
STATUS_FONT     = ("Consolas", 11)
STATUS_PX       = 14
STATUS_PY       = (2, 6)

GRID_COLS       = [(300, 2), (500, 2), (700, 3)]
GRID_COLS_DEF   = 4

# v1.4: Batas maksimum baris log terminal sebelum auto-truncate
LOG_MAX_LINES   = 500
LOG_TRIM_TO     = 350   # Potong ke jumlah ini saat batas tercapai

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
C_ACCENT        = "#FF6600"
C_SUCCESS       = "#22c55e"
C_ERROR         = "#ef4444"

FAVORITES_FILE  = "favorites.json"
CONFIG_FILE     = "naulex_config.json"
STATS_FILE      = "naulex_stats.json"
ICON_APP        = "icons/Naulex.ico"
ICON_TRANSLATE  = "icons/translate_icon.png"
ICON_SEARCH     = "icons/search_icon.png"
ICON_TERMINAL   = "icons/terminal_icon.png"

# v1.4: Set True untuk mengaktifkan profiling execution time di console
PERF_PROFILE    = False

SHORTCUT_OPTIONS = [
    "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10",
    "ctrl+q", "ctrl+shift+t", "ctrl+shift+x", "ctrl+alt+t",
    "alt+x", "alt+z", "alt+t", "alt+q",
]

# =========================
# DAFTAR BAHASA
# =========================

LANGUAGES = {
    "English": "en",       "Indonesia": "id",     "Mandarin Chinese": "zh-CN",
    "Arabic": "ar",        "Japanese": "ja",       "Spanish": "es",
    "Portuguese": "pt",    "French": "fr",         "German": "de",
    "Italian": "it",       "Russian": "ru",        "Korean": "ko",
    "Thai": "th",          "Vietnamese": "vi",     "Hindi": "hi",
    "Dutch": "nl",         "Turkish": "tr",        "Polish": "pl",
    "Persian": "fa",       "Malay": "ms",          "Bengali": "bn",
    "Filipino": "tl",      "Czech": "cs",          "Urdu": "ur",
    "Swahili": "sw",       "Romanian": "ro",       "Punjabi": "pa",
    "Hausa": "ha",         "Hungarian": "hu",      "Tamil": "ta",
    "Amharic": "am",       "Greek": "el",          "Telugu": "te",
    "Hebrew": "iw",        "Swedish": "sv",        "Marathi": "mr",
    "Serbian": "sr",       "Norwegian": "no",      "Ukrainian": "uk",
    "Bulgarian": "bg",     "Danish": "da",         "Slovak": "sk",
    "Finnish": "fi",       "Croatian": "hr",       "Lithuanian": "lt",
    "Latvian": "lv",       "Estonian": "et",       "Slovenian": "sl",
    "Macedonian": "mk",    "Albanian": "sq",       "Azerbaijani": "az",
    "Georgian": "ka",      "Armenian": "hy",       "Kazakh": "kk",
    "Uzbek": "uz",         "Mongolian": "mn",      "Nepali": "ne",
    "Sinhalese": "si",     "Khmer": "km",          "Lao": "lo",
    "Burmese": "my",       "Icelandic": "is",      "Welsh": "cy",
    "Irish": "ga",         "Basque": "eu",         "Catalan": "ca",
    "Galician": "gl",      "Afrikaans": "af",      "Zulu": "zu",
    "Xhosa": "xh",         "Yoruba": "yo",         "Igbo": "ig",
    "Somali": "so",        "Malagasy": "mg",       "Esperanto": "eo",
}

# =========================
# PERSISTENCE
# =========================

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {"shortcut": "F2", "language": "English"}

def save_config(cfg):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(cfg, f, indent=2)
    except Exception:
        pass

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

def load_stats():
    try:
        with open(STATS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {"total": 0, "today": 0, "today_date": "", "lang_counts": {}}

def save_stats(stats):
    try:
        with open(STATS_FILE, "w") as f:
            json.dump(stats, f, indent=2)
    except Exception:
        pass

# =========================
# HELPERS
# =========================

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# v1.4: Profiling helper — aktif hanya jika PERF_PROFILE = True
import contextlib

@contextlib.contextmanager
def perf_timer(label):
    """Context manager untuk mengukur execution time suatu blok kode."""
    if not PERF_PROFILE:
        yield
        return
    t0 = time.perf_counter()
    yield
    elapsed = (time.perf_counter() - t0) * 1000
    print(f"[PERF] {label}: {elapsed:.2f}ms")

def load_icon(path, size=(20, 20)):
    try:
        image = Image.open(resource_path(path)).convert("RGBA")
        return ctk.CTkImage(light_image=image, size=size)
    except Exception:
        return None

# =========================
# STATE
# =========================

config          = load_config()
favorites       = load_favorites()
stats           = load_stats()
selected_lang   = LANGUAGES.get(config.get("language", "English"), "en")
selected_lang_name = config.get("language", "English")
current_filter  = "all"
current_menu    = None
current_shortcut_popup = None   # FIX #4: state untuk popup shortcut
buttons         = {}            # name -> CTkButton
_resize_after   = [None]
_last_col_count = [-1]
current_shortcut = config.get("shortcut", "F2")
_notif_after    = [None]
_shortcut_popup_close_after = [None]  # FIX #6: timer auto-close popup
_log_line_count = [0]                 # v1.4: counter baris log terminal

# FIX #1: Cache state tombol terakhir untuk skip configure() yang tidak perlu
_btn_state_cache = {}  # name -> (text, fg_color, text_color, border_width, is_visible)
_btn_grid_cache  = {}  # name -> (row, col) | None — skip grid() jika posisi tidak berubah

def _fix_today_stats():
    today = str(date.today())
    if stats.get("today_date") != today:
        stats["today"] = 0
        stats["today_date"] = today

_fix_today_stats()

# =========================
# SORTED LANGUAGE ORDER
# =========================

def get_sorted_language_names():
    lc = stats.get("lang_counts", {})
    fav_used     = sorted([n for n in LANGUAGES if n in favorites and n in lc],
                          key=lambda n: lc[n], reverse=True)
    fav_unused   = sorted([n for n in LANGUAGES if n in favorites and n not in lc])
    nonfav_used  = sorted([n for n in LANGUAGES if n not in favorites and n in lc],
                          key=lambda n: lc[n], reverse=True)
    nonfav_rest  = [n for n in LANGUAGES if n not in favorites and n not in lc]
    return fav_used + fav_unused + nonfav_used + nonfav_rest

# =========================
# UI SETUP
# =========================

ctk.set_appearance_mode("dark")

root = ctk.CTk()
root.title("Naulex Translate")
root.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")
root.minsize(WIN_MIN_W, WIN_MIN_H)
root.configure(fg_color=C_BG)

try:
    root.iconbitmap(resource_path(ICON_APP))
except Exception:
    pass

# =========================
# TERMINAL LOG
# v1.4: Auto-truncate log saat melebihi LOG_MAX_LINES
#        → cegah memory leak & perlambatan insert seiring waktu
# =========================

def log(msg):
    terminal.configure(state="normal")
    terminal.insert("end", msg + "\n")
    _log_line_count[0] += 1

    # Truncate jika sudah melebihi batas
    if _log_line_count[0] >= LOG_MAX_LINES:
        # Hitung jumlah baris yang harus dihapus
        lines_to_delete = _log_line_count[0] - LOG_TRIM_TO
        terminal.delete("1.0", f"{lines_to_delete + 1}.0")
        _log_line_count[0] = LOG_TRIM_TO

    terminal.see("end")
    terminal.configure(state="disabled")

# =========================
# NOTIFICATION
# =========================

def show_notif(msg, color=C_SUCCESS):
    notif_label.configure(text=msg, text_color=color)
    rw = root.winfo_width()
    rh = root.winfo_height()
    w, h = 230, 36
    notif_frame.place(x=rw - w - 16, y=rh - h - 14, width=w, height=h)
    notif_frame.lift()
    if _notif_after[0]:
        root.after_cancel(_notif_after[0])
    _notif_after[0] = root.after(2500, lambda: notif_frame.place_forget())

# =========================
# PILIH BAHASA
# =========================

def select_language(name):
    global selected_lang, selected_lang_name
    prev_name = selected_lang_name
    selected_lang = LANGUAGES[name]
    selected_lang_name = name
    config["language"] = name

    # PERF: Hanya configure 2 tombol (lama & baru), bukan semua 80+ tombol
    if prev_name and prev_name != name and prev_name in buttons:
        buttons[prev_name].configure(
            fg_color=C_BTN, text_color=C_TEXT,
            border_color=C_BTN_BORDER, border_width=1,
        )
        # Reset cache supaya refresh_grid tidak skip tombol lama
        _btn_state_cache.pop(prev_name, None)

    if name in buttons:
        buttons[name].configure(
            fg_color=C_BTN_SEL_FG, text_color=C_BTN_SEL_TXT, border_width=0
        )
        _btn_state_cache.pop(name, None)

    status_label.configure(text=f"Target Language : {name}")
    log(f"[INFO] Language selected: {name}")

# =========================
# FAVORITE
# =========================

def toggle_favorite(name):
    if name in favorites:
        favorites.remove(name)
        log(f"[INFO] Removed from favorites: {name}")
        root.after(0, lambda: show_notif(f"Removed: {name}", C_ERROR))
    else:
        favorites.add(name)
        log(f"[INFO] Added to favorites: {name}")
        root.after(0, lambda: show_notif(f"Favorited: {name}", C_SUCCESS))
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
    menu.geometry(f"130x35+{event.x_root}+{event.y_root}")

    text = "★ Unfavorite" if lang_name in favorites else "☆ Favorite"

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
        border_width=1, corner_radius=6,
        font=("Consolas", 11),
        command=on_click
    ).pack(fill="both", expand=True)

def close_current_menu(event=None):
    global current_menu
    if current_menu and current_menu.winfo_exists():
        current_menu.destroy()
    current_menu = None

root.bind_all("<Button-1>", lambda e: root.after(10, close_current_menu))

# =========================
# TRANSLATE
# FIX #3: Kurangi sleep, pindahkan import ke level modul
# =========================

def do_translate():
    try:
        keyboard.press_and_release("ctrl+a")
        time.sleep(0.05)   # dikurangi dari 0.08
        keyboard.press_and_release("ctrl+c")
        time.sleep(0.08)   # dikurangi dari 0.12

        text = pyperclip.paste()
        if not text.strip():
            return

        # GoogleTranslator sudah diimport di atas — tidak ada overhead import di sini
        translated = GoogleTranslator(source="auto", target=selected_lang).translate(text)

        pyperclip.copy(translated)
        # FIX #3: Hapus sleep sebelum paste — tidak diperlukan
        keyboard.press_and_release("ctrl+v")

        code = selected_lang.upper().split("-")[0]
        log(f"Asli  : {text[:120]}{'…' if len(text) > 120 else ''}")
        log(f"{code:6s}: {translated[:120]}{'…' if len(translated) > 120 else ''}")
        log("─" * 30)
        log("")

        _fix_today_stats()
        stats["total"] = stats.get("total", 0) + 1
        stats["today"] = stats.get("today", 0) + 1
        lc = stats.setdefault("lang_counts", {})
        lc[selected_lang_name] = lc.get(selected_lang_name, 0) + 1
        save_stats(stats)

        root.after(0, lambda: show_notif("✓ Translation complete", C_SUCCESS))
        root.after(0, refresh_grid)

    except Exception as e:
        log(f"[ERROR] {e}")
        root.after(0, lambda: show_notif("✗ Translation failed", C_ERROR))

# =========================
# HOTKEY THREAD
# FIX #2: Ganti polling loop dengan keyboard.add_hotkey + keyboard.wait
#         → 0% CPU saat idle
# =========================

_hotkey_registered = [None]  # menyimpan nama shortcut yang sedang terdaftar

def _register_hotkey(shortcut):
    """Daftar ulang hotkey. Dipanggil saat startup dan saat shortcut diganti."""
    # Hapus hotkey lama jika ada
    if _hotkey_registered[0]:
        try:
            keyboard.remove_hotkey(_hotkey_registered[0])
        except Exception:
            pass
    try:
        keyboard.add_hotkey(
            shortcut,
            lambda: threading.Thread(target=do_translate, daemon=True).start(),
            suppress=False,
        )
        _hotkey_registered[0] = shortcut
    except Exception as e:
        log(f"[WARN] Hotkey register failed: {e}")

def hotkey_loop():
    time.sleep(0.4)
    log("[INFO] Naulex Translate v1.4")
    log("[INFO] Created by Naufal Khalil 🌍")
    log(f"[INFO] Shortcut active: {current_shortcut}")
    log("[INFO] Right-click a language to favorite it")
    log("")
    _register_hotkey(current_shortcut)
    # keyboard.wait() memblokir thread ini tanpa polling — CPU idle = 0%
    keyboard.wait()

# =========================
# RESPONSIVE GRID
# FIX #1: Skip configure() dan grid() jika state tombol tidak berubah
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
    with perf_timer("refresh_grid"):
        _refresh_grid_inner()

def _refresh_grid_inner():
    search_text = search_var.get().lower()
    cols = get_column_count()

    col_changed = (cols != _last_col_count[0])
    if col_changed:
        for c in range(10):
            lang_frame.grid_columnconfigure(c, weight=0, minsize=0)
        for c in range(cols):
            lang_frame.grid_columnconfigure(c, weight=1)
        _last_col_count[0] = cols
        # Kolom berubah → reset posisi cache agar semua tombol di-reposition
        _btn_grid_cache.clear()

    ordered = get_sorted_language_names()
    row = col = 0

    # v1.4: Kumpulkan operasi grid dalam batch — update sekaligus di akhir
    #        Ini mengurangi jumlah geometry manager calls per refresh.
    grid_updates   = []   # list of (btn, row, col) yang perlu dipindah
    remove_updates = []   # list of btn yang perlu di-hide

    for name in ordered:
        btn = buttons[name]
        label = f"★ {name}" if name in favorites else name

        show = True
        if search_text and search_text not in name.lower():
            show = False
        if current_filter == "favorite" and name not in favorites:
            show = False

        is_selected = (name == selected_lang_name)
        new_fg    = C_BTN_SEL_FG if is_selected else C_BTN
        new_tc    = C_BTN_SEL_TXT if is_selected else C_TEXT
        new_bw    = 0 if is_selected else 1

        # PERF: Hanya panggil configure() jika style benar-benar berubah
        cache_key = (label, new_fg, new_tc, new_bw, show)
        if _btn_state_cache.get(name) != cache_key:
            btn.configure(
                text=label,
                fg_color=new_fg,
                text_color=new_tc,
                border_color=C_BTN_BORDER,
                border_width=new_bw,
            )
            _btn_state_cache[name] = cache_key

        if show:
            new_pos = (row, col)
            # PERF: Hanya panggil grid() jika posisi berubah
            if _btn_grid_cache.get(name) != new_pos:
                grid_updates.append((btn, row, col))
                _btn_grid_cache[name] = new_pos
            col += 1
            if col >= cols:
                col = 0
                row += 1
        else:
            if _btn_grid_cache.get(name) is not None:
                remove_updates.append(btn)
                _btn_grid_cache[name] = None

    # v1.4: Eksekusi semua perubahan grid sekaligus (batch update)
    for btn, r, c in grid_updates:
        btn.grid(row=r, column=c,
                 padx=LANG_PAD_X, pady=LANG_PAD_Y, sticky="ew")
    for btn in remove_updates:
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
# RESIZE — Freeze UI selama drag, update sekali saat drag berhenti
# v1.5: Strategi baru: debounce panjang (400ms) tanpa threshold.
#        Selama user masih mendrag, timer terus di-cancel & di-reset.
#        refresh_grid() HANYA dipanggil sekali, yaitu 400ms setelah drag benar-benar berhenti.
#        Tidak ada layout recalculation sama sekali selama window sedang di-resize.
# =========================

_RESIZE_SETTLE  = 2000   # ms setelah drag berhenti baru UI di-update
_last_root_width  = [-1]
_last_root_height = [-1]

def on_resize(event):
    # PERF: <Configure> terpicu untuk SETIAP widget anak di customtkinter.
    # Filter ketat hanya ke root window.
    if event.widget is not root:
        return

    # Jika ukuran sama persis (mis. window move tanpa resize), abaikan
    if event.width == _last_root_width[0] and event.height == _last_root_height[0]:
        return
    _last_root_width[0]  = event.width
    _last_root_height[0] = event.height

    # Cancel timer sebelumnya — selama drag, ini terus di-reset
    if _resize_after[0]:
        root.after_cancel(_resize_after[0])

    # Jadwalkan update HANYA setelah drag berhenti selama RESIZE_SETTLE ms
    _resize_after[0] = root.after(_RESIZE_SETTLE, _on_resize_settled)

def _on_resize_settled():
    """Dipanggil sekali saja, setelah window selesai di-resize."""
    _resize_after[0] = None
    with perf_timer("on_resize_settled → refresh_grid"):
        # Reset cache posisi supaya tombol di-reflow sesuai ukuran baru
        _last_col_count[0] = -1
        _btn_grid_cache.clear()
        refresh_grid()

# =========================
# SHORTCUT PICKER (POPUP KONTEKSTUAL)
# FIX #4: Ganti CTkToplevel dengan popup overrideredirect di dekat tombol
# FIX #5: Shortcut aktif menggunakan style selected yang sama dengan bahasa
# FIX #6: Popup tetap tampil 3 detik setelah memilih, baru tutup otomatis
# =========================

def show_shortcut_picker():
    global current_shortcut_popup

    # Tutup popup lama jika masih terbuka
    if current_shortcut_popup and current_shortcut_popup.winfo_exists():
        current_shortcut_popup.destroy()
        current_shortcut_popup = None
        return  # toggle: klik lagi = tutup

    # Hitung posisi popup relatif ke shortcut_btn
    btn_x = shortcut_btn.winfo_rootx()
    btn_y = shortcut_btn.winfo_rooty()
    btn_h = shortcut_btn.winfo_height()

    popup_w = 180
    # Hitung tinggi: setiap item ~36px + header ~30px
    popup_h = min(len(SHORTCUT_OPTIONS) * 36 + 30, 420)

    # Posisikan di atas tombol agar tidak keluar layar
    px = btn_x - popup_w + shortcut_btn.winfo_width()
    py = btn_y - popup_h - 4

    # Jangan keluar batas atas layar
    if py < 0:
        py = btn_y + btn_h + 4

    popup = ctk.CTkToplevel(root)
    current_shortcut_popup = popup
    popup.overrideredirect(True)
    popup.attributes("-topmost", True)
    popup.geometry(f"{popup_w}x{popup_h}+{px}+{py}")
    popup.configure(fg_color=C_PANEL)

    # Tambah border tipis via inner frame
    inner = ctk.CTkFrame(popup, fg_color=C_PANEL, corner_radius=8,
                         border_width=1, border_color=C_BTN_BORDER)
    inner.pack(fill="both", expand=True, padx=1, pady=1)

    # Label header kecil
    ctk.CTkLabel(
        inner, text="Shortcut",
        font=("Consolas", 10),
        text_color="#888888",
    ).pack(pady=(6, 2))

    scroll = ctk.CTkScrollableFrame(
        inner,
        fg_color="transparent",
        scrollbar_button_color=C_SCROLL_BTN,
        scrollbar_button_hover_color=C_SCROLL_HOVER,
    )
    scroll.pack(fill="both", expand=True, padx=6, pady=(0, 6))

    # Simpan referensi semua tombol di popup agar bisa diupdate visual
    sc_buttons = {}

    def pick(s):
        global current_shortcut
        old = current_shortcut
        current_shortcut = s
        config["shortcut"] = s
        save_config(config)
        shortcut_btn.configure(text=s)
        log(f"[INFO] Shortcut changed: {old} → {s}")
        show_notif(f"Shortcut: {s}", C_SUCCESS)

        # FIX #2: Daftarkan ulang hotkey baru tanpa restart thread
        threading.Thread(target=lambda: _register_hotkey(s), daemon=True).start()

        # FIX #5: Update visual semua tombol di popup — aktif = style selected
        for sc_key, sc_btn in sc_buttons.items():
            is_now_active = (sc_key == s)
            sc_btn.configure(
                fg_color=C_BTN_SEL_FG if is_now_active else C_BTN,
                text_color=C_BTN_SEL_TXT if is_now_active else C_TEXT,
                hover_color="#dddddd" if is_now_active else C_BTN_HOVER,
                border_width=0 if is_now_active else 1,
            )

        # FIX #6: Batalkan timer close sebelumnya, tutup otomatis setelah 3 detik
        if _shortcut_popup_close_after[0]:
            root.after_cancel(_shortcut_popup_close_after[0])
        _shortcut_popup_close_after[0] = root.after(3000, _close_shortcut_popup)

    for sc in SHORTCUT_OPTIONS:
        is_active = (sc == current_shortcut)
        b = ctk.CTkButton(
            scroll,
            text=sc,
            height=30,
            # FIX #5: Style aktif sama persis dengan bahasa yang dipilih
            fg_color=C_BTN_SEL_FG if is_active else C_BTN,
            text_color=C_BTN_SEL_TXT if is_active else C_TEXT,
            hover_color="#dddddd" if is_active else C_BTN_HOVER,
            border_color=C_BTN_BORDER,
            border_width=0 if is_active else 1,
            corner_radius=20,
            font=TAB_FONT,
            command=lambda s=sc: pick(s),
        )
        b.pack(fill="x", pady=2)
        sc_buttons[sc] = b

def _close_shortcut_popup():
    global current_shortcut_popup
    if current_shortcut_popup and current_shortcut_popup.winfo_exists():
        current_shortcut_popup.destroy()
    current_shortcut_popup = None
    _shortcut_popup_close_after[0] = None

def _close_shortcut_if_outside(event):
    """Tutup popup shortcut jika klik di luar area popup."""
    global current_shortcut_popup
    if not current_shortcut_popup or not current_shortcut_popup.winfo_exists():
        return
    # Jangan tutup jika klik ada di dalam popup atau di shortcut_btn
    try:
        px = current_shortcut_popup.winfo_rootx()
        py = current_shortcut_popup.winfo_rooty()
        pw = current_shortcut_popup.winfo_width()
        ph = current_shortcut_popup.winfo_height()
        ex, ey = event.x_root, event.y_root
        if px <= ex <= px + pw and py <= ey <= py + ph:
            return
        # Juga jangan tutup kalau klik di shortcut_btn sendiri
        bx = shortcut_btn.winfo_rootx()
        by = shortcut_btn.winfo_rooty()
        bw = shortcut_btn.winfo_width()
        bh = shortcut_btn.winfo_height()
        if bx <= ex <= bx + bw and by <= ey <= by + bh:
            return
    except Exception:
        pass
    _close_shortcut_popup()

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
if icon_img:
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
    opaqueresize=False,
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

# Search
search_frame = ctk.CTkFrame(topbar_frame, fg_color=C_BTN,
                             corner_radius=20, height=SEARCH_H)
search_frame.pack(side="left", fill="x", expand=True)
search_frame.pack_propagate(False)

search_img  = load_icon(ICON_SEARCH, SEARCH_ICON_SZ)
search_icon = ctk.CTkLabel(
    search_frame,
    image=search_img if search_img else None,
    text="" if search_img else "🔍",
    text_color=C_TEXT,
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

# Language grid
lang_frame = ctk.CTkScrollableFrame(
    left_frame,
    fg_color="transparent",
    scrollbar_button_color=C_SCROLL_BTN,
    scrollbar_button_hover_color=C_SCROLL_HOVER,
)
lang_frame.pack(fill="both", expand=True,
                padx=LANG_FRAME_PX, pady=(0, LANG_FRAME_PY_B))

# Build language buttons
# v1.4: corner_radius dikurangi (8→4) untuk kurangi biaya render pada 80+ tombol massal.
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
        corner_radius=4,            # v1.4: dikurangi dari 8 → 4 (lebih ringan)
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

# ── Bottom bar: status (left) + shortcut btn (right) ──

bottom_bar = ctk.CTkFrame(right_frame, fg_color="transparent")
bottom_bar.pack(fill="x", padx=STATUS_PX, pady=STATUS_PY)

status_label = ctk.CTkLabel(
    bottom_bar,
    text="Target Language : English",
    font=STATUS_FONT,
    text_color=C_STATUS_TXT,
    anchor="w",
)
status_label.pack(side="left", fill="x", expand=True)

shortcut_btn = ctk.CTkButton(
    bottom_bar,
    text=current_shortcut,
    width=TAB_BTN_W, height=TAB_BTN_H,
    fg_color=C_BTN,
    text_color=C_TEXT,
    hover_color=C_BTN_HOVER,
    border_color="#444444",
    border_width=1,
    corner_radius=20,
    font=TAB_FONT,
    command=show_shortcut_picker,
)
shortcut_btn.pack(side="right")

# ── Notification overlay ───────────────────────────

notif_frame = ctk.CTkFrame(
    root,
    fg_color="#1e1e1e",
    corner_radius=8,
    border_width=1,
    border_color="#333333",
)
notif_label = ctk.CTkLabel(
    notif_frame,
    text="",
    font=("Consolas", 11),
    text_color=C_WHITE,
)
notif_label.pack(padx=14, pady=6)

# FIX #4: Bind klik di luar untuk menutup popup shortcut
root.bind_all("<Button-1>", lambda e: (
    root.after(10, close_current_menu),
    root.after(10, lambda: _close_shortcut_if_outside(e))
))

# =========================
# INIT SETELAH WINDOW SIAP
# =========================

def _after_map():
    root.bind("<Configure>", on_resize)
    refresh_grid()
    root.after(100, lambda: sash_pane.sash_place(
        0, int(root.winfo_width() * SASH_RATIO), 0))

root.after(150, _after_map)

select_language(config.get("language", "English"))
threading.Thread(target=hotkey_loop, daemon=True).start()
root.mainloop()
