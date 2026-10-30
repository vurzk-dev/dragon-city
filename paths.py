import os
import sys
import threading

from logging_config import logger

def _get_exe_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
EXE_DIR    = _get_exe_dir()

TEMPLATES_DIR  = os.path.join(BASE_DIR, 'templates')
FLASH_DIR      = os.path.join(BASE_DIR, 'flash')
WEB_DIR        = os.path.join(BASE_DIR, 'web')
SRV_DIR        = os.path.join(WEB_DIR, 'srv')
DOMAIN_MAP_DIR = os.path.join(BASE_DIR, 'domains')
ASSETS_DIR     = os.path.join(BASE_DIR, 'assets')
VILLAGES_DIR   = os.path.join(BASE_DIR, 'villages')

SAVES_DIR      = os.path.join(BASE_DIR, 'saves')
if not os.path.exists(SAVES_DIR):
    os.makedirs(SAVES_DIR)

SECRET_KEY = "RGhXbiy4xEeDnSNX1oBG"

HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"

HOSTS_ENTRIES = [
    "127.0.0.1 dynamicdc.socialpointgames.com",
    "127.0.0.1 dc-canvas.socialpointgames.com",
    "127.0.0.1 sr.socialpointgames.com",
    "127.0.0.1 static.socialpointgames.com",
    "127.0.0.1 sp-frontend-s1.socialpointgames.com",
    "127.0.0.1 default01.static.socialpointgames.com",
    "127.0.0.1 dci-static-s1.socialpointgames.com",
    "127.0.0.1 dci-static-s2.socialpointgames.com",
    "127.0.0.1 dci-static-s3.socialpointgames.com",
    "127.0.0.1 ajax.googleapis.com",
    "127.0.0.1 api.omniata.com",
    "127.0.0.1 sp-translations.socialpointgames.com",
    "127.0.0.1 graph.facebook.com",
    "127.0.0.1 www.google-analytics.com",
    "127.0.0.1 ssl.google-analytics.com",
    "127.0.0.1 google-analytics.com",
]

MARKER = "# --- Dragon City Flash ---"

_active_players      = {}
_active_players_lock = threading.Lock()

AUTOSAVE_INTERVAL      = 5
AUTOSAVE_ACTIVE_WINDOW = 30