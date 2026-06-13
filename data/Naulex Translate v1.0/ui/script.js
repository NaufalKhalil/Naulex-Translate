// ============================================================
//  Naulex Translate — Frontend Script
//  Communicates with Python backend via window.pywebview.api
// ============================================================

'use strict';

// ── State ──────────────────────────────────────────────────
let state = {
  languages:        [],
  shortcuts:        [],
  selectedLang:     'English',
  currentShortcut:  'F2',
  favorites:        new Set(),
  filter:           'all',        // 'all' | 'favorite'
  contextTarget:    null,
  shortcutPopupOpen: false,
  shortcutCloseTimer: null,
};

// ── Init ───────────────────────────────────────────────────
window.addEventListener('pywebviewready', async () => {
  try {
    const data = await window.pywebview.api.get_init_data();
    state.languages       = data.languages;
    state.shortcuts       = data.shortcuts;
    state.selectedLang    = data.selected_lang;
    state.currentShortcut = data.current_shortcut;
    state.favorites       = new Set(data.favorites);

    buildLangButtons();
    buildShortcutList();
    updateShortcutBtn();
    updateStatus();
    refreshGrid();
  } catch (e) {
    console.error('Init failed:', e);
    // Retry once after a short delay (window may not be ready yet)
    setTimeout(async () => {
      try {
        const data = await window.pywebview.api.get_init_data();
        state.languages       = data.languages;
        state.shortcuts       = data.shortcuts;
        state.selectedLang    = data.selected_lang;
        state.currentShortcut = data.current_shortcut;
        state.favorites       = new Set(data.favorites);
        buildLangButtons();
        buildShortcutList();
        updateShortcutBtn();
        updateStatus();
        refreshGrid();
      } catch(e2) { console.error('Init retry failed:', e2); }
    }, 800);
  }
});

// ── Build language buttons ─────────────────────────────────
function buildLangButtons() {
  const grid = document.getElementById('langGrid');
  grid.innerHTML = '';

  for (const name of state.languages) {
    const btn = document.createElement('button');
    btn.className   = 'lang-btn';
    btn.dataset.lang = name;
    btn.textContent  = name;
    btn.title        = name;

    btn.addEventListener('click', () => selectLanguage(name));
    btn.addEventListener('contextmenu', e => showCtxMenu(e, name));

    grid.appendChild(btn);
  }
}

// ── Refresh / filter / sort ─────────────────────────────────
function refreshGrid() {
  const query   = document.getElementById('searchInput').value.toLowerCase();
  const grid    = document.getElementById('langGrid');
  const buttons = grid.querySelectorAll('.lang-btn');

  for (const btn of buttons) {
    const name    = btn.dataset.lang;
    const isFav   = state.favorites.has(name);
    const matches = name.toLowerCase().includes(query);
    const passFilter = state.filter === 'all' || isFav;
    const visible = matches && passFilter;

    btn.style.display = visible ? '' : 'none';

    // Label
    btn.textContent = name;

    // CSS classes
    btn.classList.toggle('selected',  name === state.selectedLang);
    btn.classList.toggle('fav-star',  isFav);
  }

  // Sort: fav used first → fav unused → rest
  const sorted = [...buttons].sort((a, b) => {
    const aFav = state.favorites.has(a.dataset.lang) ? 0 : 1;
    const bFav = state.favorites.has(b.dataset.lang) ? 0 : 1;
    if (aFav !== bFav) return aFav - bFav;
    return a.dataset.lang.localeCompare(b.dataset.lang);
  });
  sorted.forEach(btn => grid.appendChild(btn));
}

// ── Select language ────────────────────────────────────────
async function selectLanguage(name) {
  state.selectedLang = name;
  updateStatus();
  refreshGrid();

  try {
    await window.pywebview.api.select_language(name);
  } catch(e) { console.error(e); }
}

// ── Filter (All / Fav) ─────────────────────────────────────
function setFilter(mode) {
  state.filter = mode;
  document.getElementById('btnAll').classList.toggle('active', mode === 'all');
  document.getElementById('btnFav').classList.toggle('active', mode === 'favorite');
  refreshGrid();
}

// ── Context menu (right-click) ─────────────────────────────
function showCtxMenu(e, name) {
  e.preventDefault();
  state.contextTarget = name;

  const menu   = document.getElementById('ctxMenu');
  const favBtn = document.getElementById('ctxFavBtn');
  favBtn.textContent = state.favorites.has(name)
    ? `★ Unfavorite`
    : `☆ Favorite`;

  menu.classList.remove('hidden');
  menu.style.left = e.clientX + 'px';
  menu.style.top  = e.clientY + 'px';

  // Clamp to viewport
  requestAnimationFrame(() => {
    const r = menu.getBoundingClientRect();
    if (r.right  > window.innerWidth)  menu.style.left = (e.clientX - r.width)  + 'px';
    if (r.bottom > window.innerHeight) menu.style.top  = (e.clientY - r.height) + 'px';
  });
}

function hideCtxMenu() {
  document.getElementById('ctxMenu').classList.add('hidden');
  state.contextTarget = null;
}

async function ctxToggleFav() {
  const name = state.contextTarget;
  if (!name) return;
  hideCtxMenu();

  try {
    const res = await window.pywebview.api.toggle_favorite(name);
    if (res.ok) {
      state.favorites = new Set(res.favorites);
      refreshGrid();
      showToast(res.message, state.favorites.has(name));
    }
  } catch(e) { console.error(e); }
}

// ── Shortcut picker ────────────────────────────────────────
function buildShortcutList() {
  const list = document.getElementById('shortcutList');
  list.innerHTML = '';
  for (const sc of state.shortcuts) {
    const btn = document.createElement('button');
    btn.className = 'sc-btn' + (sc === state.currentShortcut ? ' active' : '');
    btn.textContent = sc;
    btn.dataset.sc  = sc;
    btn.addEventListener('click', () => pickShortcut(sc));
    list.appendChild(btn);
  }
}

function toggleShortcutPicker() {
  const popup = document.getElementById('shortcutPopup');
  state.shortcutPopupOpen = !state.shortcutPopupOpen;
  popup.classList.toggle('hidden', !state.shortcutPopupOpen);
}

function closeShortcutPopup() {
  state.shortcutPopupOpen = false;
  document.getElementById('shortcutPopup').classList.add('hidden');
}

async function pickShortcut(sc) {
  state.currentShortcut = sc;
  updateShortcutBtn();

  // Update visual in popup
  document.querySelectorAll('#shortcutList .sc-btn').forEach(b => {
    b.classList.toggle('active', b.dataset.sc === sc);
  });

  // Auto-close popup after 2.5s
  if (state.shortcutCloseTimer) clearTimeout(state.shortcutCloseTimer);
  state.shortcutCloseTimer = setTimeout(closeShortcutPopup, 2500);

  try {
    const res = await window.pywebview.api.set_shortcut(sc);
    if (res.ok) showToast(`Shortcut: ${sc}`, true);
  } catch(e) { console.error(e); }
}

function updateShortcutBtn() {
  document.getElementById('shortcutBtn').textContent = state.currentShortcut;
}

// ── Status bar ─────────────────────────────────────────────
function updateStatus() {
  document.getElementById('statusLang').textContent = state.selectedLang;
}

// ── Terminal log ───────────────────────────────────────────
const MAX_LOG_LINES = 500;
const TRIM_TO       = 350;
let   logLineCount  = 0;

/** Called from Python backend via evaluate_js */
window._appendLog = function(msg) {
  const lines  = document.getElementById('termLines');
  const div    = document.createElement('div');

  // Colour coding
  if (msg.startsWith('[INFO]'))  div.className = 'log-info';
  else if (msg.startsWith('[ERROR]')) div.className = 'log-error';
  else if (msg.startsWith('[WARN]'))  div.className = 'log-warn';
  else if (msg.startsWith('─'))       div.className = 'log-sep';
  else if (msg.startsWith('Asli'))    div.className = 'log-orig';
  else if (/^[A-Z]{2,6}\s+:/.test(msg)) div.className = 'log-trans';

  div.textContent = msg;
  lines.appendChild(div);
  logLineCount++;

  // Trim if too long
  if (logLineCount >= MAX_LOG_LINES) {
    const toRemove = logLineCount - TRIM_TO;
    for (let i = 0; i < toRemove; i++) {
      if (lines.firstChild) lines.removeChild(lines.firstChild);
    }
    logLineCount = TRIM_TO;
  }

  const term = document.getElementById('terminal');
  term.scrollTop = term.scrollHeight;
};

function clearTerminal() {
  document.getElementById('termLines').innerHTML = '';
  logLineCount = 0;
}

/** Called when clipboard-hotkey translate succeeds */
window._onTranslateSuccess = function() {
  showToast('✓ Translation complete', true);
};

/** Called when clipboard-hotkey translate fails */
window._onTranslateError = function(msg) {
  showToast(`✗ ${msg}`, false);
};

// ── Toast notification ─────────────────────────────────────
let _toastTimer = null;
function showToast(msg, success = true) {
  const toast = document.getElementById('toast');
  toast.textContent = msg;
  toast.className   = 'toast' + (success ? '' : ' error');

  if (_toastTimer) clearTimeout(_toastTimer);
  _toastTimer = setTimeout(() => {
    toast.classList.add('hidden');
  }, 2500);
}

// ── Global event: close menus on click outside ─────────────
document.addEventListener('click', e => {
  // Close context menu
  if (!e.target.closest('#ctxMenu')) hideCtxMenu();

  // Close shortcut popup
  if (!e.target.closest('#shortcutPopup') &&
      !e.target.closest('#shortcutBtn')) {
    closeShortcutPopup();
  }
});

document.addEventListener('contextmenu', e => {
  // Prevent default for non-lang areas
  if (!e.target.closest('.lang-btn')) {
    e.preventDefault();
    hideCtxMenu();
  }
});

// ── Resizable splitter ─────────────────────────────────────
(function initResize() {
  const handle     = document.getElementById('resizeHandle');
  const panelLeft  = document.getElementById('panelLeft');
  let   dragging   = false;
  let   startX     = 0;
  let   startWidth = 0;

  handle.addEventListener('mousedown', e => {
    dragging   = true;
    startX     = e.clientX;
    startWidth = panelLeft.getBoundingClientRect().width;
    handle.classList.add('dragging');
    document.body.style.cursor = 'col-resize';
    e.preventDefault();
  });

  document.addEventListener('mousemove', e => {
    if (!dragging) return;
    const delta    = e.clientX - startX;
    const newWidth = Math.min(
      Math.max(startWidth + delta, 280),
      window.innerWidth - 220
    );
    panelLeft.style.width = newWidth + 'px';
  });

  document.addEventListener('mouseup', () => {
    if (!dragging) return;
    dragging = false;
    handle.classList.remove('dragging');
    document.body.style.cursor = '';
  });
})();
