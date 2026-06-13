
import subprocess, sys, os, json

# ── Path helpers ───────────────────────────────────────────
def _get_internal_dir():
    """Folder berisi asset bundled (di dalam EXE = _MEIPASS)."""
    if getattr(sys, "frozen", False):
        return sys._MEIPASS          # type: ignore[attr-defined]
    return os.path.dirname(os.path.abspath(__file__))

def _get_appdata_dir():
    """C:\\Program Files\\Naulex Translate — writable data folder."""
    path = os.path.join("C:\\Program Files", "Naulex Translate")
    for sub in ["config", "data", "assets"]:
        os.makedirs(os.path.join(path, sub), exist_ok=True)
    return path

INTERNAL_DIR = _get_internal_dir()
APP_DIR      = _get_appdata_dir()

IS_FROZEN = getattr(sys, "frozen", False)

REQUIRED  = ["pywebview", "deep-translator", "keyboard", "pyperclip"]
FLAG_FILE = os.path.join(APP_DIR, ".deps_installed")

def _install_missing():
    # EXE mode → tidak perlu install apapun
    if IS_FROZEN:
        return

    # Dev mode → cek flag dulu
    if os.path.exists(FLAG_FILE):
        return

    needs = []
    for pkg in REQUIRED:
        mod = pkg.replace("-", "_").split("[")[0]
        try:
            __import__(mod)
        except ImportError:
            needs.append(pkg)

    if not needs:
        open(FLAG_FILE, "w").close()
        return

    # Progress window (dev mode only)
    try:
        import tkinter as tk
        from tkinter import ttk
        import threading

        root = tk.Tk()
        root.title("Naulex Translate — Installing...")
        root.geometry("400x130")
        root.resizable(False, False)
        root.configure(bg="#0d0d0d")

        tk.Label(root, text="Installing required libraries…",
                 bg="#0d0d0d", fg="#ffffff",
                 font=("Consolas", 10)).pack(pady=(18, 6))
        lbl = tk.Label(root, text="", bg="#0d0d0d", fg="#FF6600",
                       font=("Consolas", 9))
        lbl.pack()
        bar = ttk.Progressbar(root, length=340, mode="determinate",
                              maximum=len(needs))
        bar.pack(pady=10)
        ttk.Style().configure("TProgressbar", troughcolor="#1a1a1a",
                              background="#FF6600", thickness=14)

        def do_install():
            ok = True
            for i, pkg in enumerate(needs):
                lbl.config(text=f"pip install {pkg}")
                bar["value"] = i
                root.update_idletasks()
                try:
                    subprocess.check_call(
                        [sys.executable, "-m", "pip", "install", pkg, "-q"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                except Exception:
                    ok = False
            bar["value"] = len(needs)
            root.update_idletasks()
            if ok:
                open(FLAG_FILE, "w").close()
            root.after(800, root.destroy)

        threading.Thread(target=do_install, daemon=True).start()
        root.mainloop()

    except Exception:
        for pkg in needs:
            subprocess.call(
                [sys.executable, "-m", "pip", "install", pkg, "-q"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        open(FLAG_FILE, "w").close()

_install_missing()

# ── Imports utama ─────────────────────────────────────────
import threading, time
from collections import deque
import webview
import keyboard
import pyperclip
from deep_translator import GoogleTranslator

# ── Paths ─────────────────────────────────────────────────
UI_DIR      = os.path.join(INTERNAL_DIR, "ui")
CONFIG_FILE = os.path.join(APP_DIR, "config", "settings.json")
FAV_FILE    = os.path.join(APP_DIR, "data",   "favorites.json")

# ── Seed default JSON + salin assets ──────────────────────
def _seed_defaults():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump({"shortcut": "F2", "language": "English"}, f, indent=2)
    if not os.path.exists(FAV_FILE):
        with open(FAV_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2)

    import shutil
    src_assets = os.path.join(INTERNAL_DIR, "ui", "assets")
    dst_assets = os.path.join(APP_DIR, "assets")
    if os.path.isdir(src_assets):
        for fn in os.listdir(src_assets):
            dst = os.path.join(dst_assets, fn)
            if not os.path.exists(dst):
                try:
                    shutil.copy2(os.path.join(src_assets, fn), dst)
                except Exception:
                    pass

_seed_defaults()

# ── Language table ─────────────────────────────────────────
LANGUAGES = {
    "English":"en",
    "Indonesian":"id",
    "Chinese (Simplified)":"zh-CN",
    "Spanish":"es",
    "Hindi":"hi",
    "Arabic":"ar",
    "French":"fr",
    "Portuguese":"pt",
    "Russian":"ru",
    "German":"de",
    "Japanese":"ja",
    "Korean":"ko",
    "Turkish":"tr",
    "Italian":"it",
    "Vietnamese":"vi",
    "Thai":"th",
    "Polish":"pl",
    "Dutch":"nl",
    "Ukrainian":"uk",
    "Persian":"fa",
    "Urdu":"ur",
    "Malay":"ms",
    "Bengali":"bn",
    "Tamil":"ta",
    "Telugu":"te",
    "Punjabi":"pa",
    "Greek":"el",
    "Hebrew":"iw",
    "Swedish":"sv",
    "Czech":"cs",
    "Romanian":"ro",
    "Hungarian":"hu",
    "Danish":"da",
    "Finnish":"fi",
    "Norwegian":"no",
    "Slovak":"sk",
    "Croatian":"hr",
    "Bulgarian":"bg",
    "Serbian":"sr",
    "Lithuanian":"lt",
    "Latvian":"lv",
    "Estonian":"et",
    "Slovenian":"sl",
    "Macedonian":"mk",
    "Albanian":"sq",
    "Georgian":"ka",
    "Armenian":"hy",
    "Kazakh":"kk",
    "Uzbek":"uz",
    "Azerbaijani":"az",
    "Mongolian":"mn",
    "Nepali":"ne",
    "Khmer":"km",
    "Lao":"lo",
    "Myanmar (Burmese)":"my",
    "Sinhala":"si",
    "Swahili":"sw",
    "Hausa":"ha",
    "Yoruba":"yo",
    "Igbo":"ig",
    "Zulu":"zu",
    "Xhosa":"xh",
    "Amharic":"am",
    "Somali":"so",
    "Malagasy":"mg",
    "Filipino":"tl",
    "Javanese":"jw",
    "Sundanese":"su",
    "Welsh":"cy",
    "Irish":"ga",
    "Scots Gaelic":"gd",
    "Basque":"eu",
    "Catalan":"ca",
    "Galician":"gl",
    "Esperanto":"eo",
    "Latin":"la",
    "Yiddish":"yi",
    "Luxembourgish":"lb",
    "Corsican":"co",
    "Frisian":"fy",
    "Maori":"mi",
    "Samoan":"sm",
    "Hawaiian":"haw",
    "Nyanja":"ny",
    "Sesotho":"st",
    "Shona":"sn",
    "Sindhi":"sd",
    "Pashto":"ps",
    "Kyrgyz":"ky",
    "Kurdish":"ku",
    "Gujarati":"gu",
    "Kannada":"kn",
    "Malayalam":"ml",
    "Maltese":"mt",
    "Belarusian":"be",
    "Bosnian":"bs",
    "Tajik":"tg",
    "Cebuano":"ceb",
    "Afrikaans":"af"
}

SHORTCUT_OPTIONS = [
    "F1","F2","F3","F4","F5","F6","F7","F8","F9","F10",
    "ctrl+q","ctrl+shift+t","ctrl+shift+x","ctrl+alt+t",
    "alt+x","alt+z","alt+t","alt+q",
]

# ── Persistence helpers ────────────────────────────────────
def _load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

def _save_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

# ── App state ──────────────────────────────────────────────
_config             = _load_json(CONFIG_FILE, {"shortcut": "F2", "language": "English"})
_favorites          = set(_load_json(FAV_FILE, []))
_selected_lang      = LANGUAGES.get(_config.get("language", "English"), "en")
_selected_lang_name = _config.get("language", "English")
_hotkey_registered  = [None]
_window             = None
_log_buffer         = deque(maxlen=500)

# ── Log ───────────────────────────────────────────────────
def _log(msg):
    _log_buffer.append(msg)
    if _window:
        try:
            safe = msg.replace("\\","\\\\").replace("`","\\`").replace("$","\\$")
            _window.evaluate_js(f"window._appendLog(`{safe}`)")
        except Exception:
            pass

# ── JS bridge API ──────────────────────────────────────────
class NaulexAPI:

    def get_init_data(self):
        return {
            "languages":        list(LANGUAGES.keys()),
            "shortcuts":        SHORTCUT_OPTIONS,
            "selected_lang":    _selected_lang_name,
            "current_shortcut": _config.get("shortcut", "F2"),
            "favorites":        list(_favorites),
        }

    def select_language(self, name):
        global _selected_lang, _selected_lang_name
        if name not in LANGUAGES:
            return {"ok": False, "error": "Unknown language"}
        _selected_lang      = LANGUAGES[name]
        _selected_lang_name = name
        _config["language"] = name
        _save_json(CONFIG_FILE, _config)
        _log(f"[INFO] Language selected: {name}")
        return {"ok": True, "lang": name}

    def toggle_favorite(self, name):
        if name in _favorites:
            _favorites.discard(name)
            msg = f"Removed from favorites: {name}"
        else:
            _favorites.add(name)
            msg = f"Added to favorites: {name}"
        _save_json(FAV_FILE, list(_favorites))
        _log(f"[INFO] {msg}")
        return {"ok": True, "favorites": list(_favorites), "message": msg}

    def get_favorites(self):
        return list(_favorites)

    def set_shortcut(self, shortcut):
        old = _config.get("shortcut", "F2")
        _config["shortcut"] = shortcut
        _save_json(CONFIG_FILE, _config)
        _log(f"[INFO] Shortcut changed: {old} → {shortcut}")
        threading.Thread(target=lambda: _register_hotkey(shortcut), daemon=True).start()
        return {"ok": True, "shortcut": shortcut}

    def translate_text(self, text, target_lang=None):
        lang = target_lang or _selected_lang
        if not text.strip():
            return {"ok": False, "error": "Empty text"}
        try:
            result = GoogleTranslator(source="auto", target=lang).translate(text)
            _log(f"Asli  : {text[:120]}{'…' if len(text)>120 else ''}")
            _log(f"{lang.upper()[:6]:6s}: {result[:120]}{'…' if len(result)>120 else ''}")
            _log("─" * 30)
            return {"ok": True, "result": result}
        except Exception as e:
            _log(f"[ERROR] {e}")
            return {"ok": False, "error": str(e)}

    def do_clipboard_translate(self):
        threading.Thread(target=_do_translate, daemon=True).start()
        return {"ok": True}

    def get_log_lines(self):
        return list(_log_buffer)

# ── Translation (clipboard flow) ──────────────────────────
def _do_translate():
    try:
        keyboard.press_and_release("ctrl+a")
        time.sleep(0.05)
        keyboard.press_and_release("ctrl+c")
        time.sleep(0.08)

        text = pyperclip.paste()
        if not text.strip():
            return

        translated = GoogleTranslator(source="auto", target=_selected_lang).translate(text)
        pyperclip.copy(translated)
        keyboard.press_and_release("ctrl+v")

        code = _selected_lang.upper().split("-")[0]
        _log(f"Asli  : {text[:120]}{'…' if len(text)>120 else ''}")
        _log(f"{code:6s}: {translated[:120]}{'…' if len(translated)>120 else ''}")
        _log("─" * 30)
        _log("")

        if _window:
            try:
                _window.evaluate_js("window._onTranslateSuccess()")
            except Exception:
                pass

    except Exception as e:
        _log(f"[ERROR] {e}")
        if _window:
            try:
                _window.evaluate_js(f"window._onTranslateError(`{e}`)")
            except Exception:
                pass

# ── Hotkey management ─────────────────────────────────────
def _register_hotkey(shortcut):
    if _hotkey_registered[0]:
        try:
            keyboard.remove_hotkey(_hotkey_registered[0])
        except Exception:
            pass
    try:
        keyboard.add_hotkey(
            shortcut,
            lambda: threading.Thread(target=_do_translate, daemon=True).start(),
            suppress=False
        )
        _hotkey_registered[0] = shortcut
    except Exception as e:
        _log(f"[WARN] Hotkey register failed: {e}")

def _hotkey_init():
    time.sleep(0.4)
    _log("[INFO] Naulex Translate v1.0")
    time.sleep(0.1)
    _log("[INFO] Created by Naufal Khalil 🇮🇩")
    time.sleep(0.1)
    _log(f"[INFO] Shortcut active: {_config.get('shortcut','F2')}")
    time.sleep(0.1)
    _log("[INFO] Right-click a language to toggle favorite")
    time.sleep(0.1)
    _log(f"[INFO] Data dir: {APP_DIR}")
    time.sleep(0.1)
    _log("")
    _register_hotkey(_config.get("shortcut", "F2"))
    keyboard.wait()

# ── Entry point ───────────────────────────────────────────
def main():
    global _window

    api     = NaulexAPI()
    _window = webview.create_window(
        title            = "Naulex Translate",
        url              = os.path.join(UI_DIR, "index.html"),
        js_api           = api,
        width            = 1200,
        height           = 700,
        min_size         = (640, 480),
        background_color = "#0d0d0d",
        resizable        = True,
    )

    threading.Thread(target=_hotkey_init, daemon=True).start()
    webview.start(debug=False)

if __name__ == "__main__":
    main()
