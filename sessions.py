import time
import queue

from logging_config import logger
from paths import (
    _active_players, _active_players_lock,
    AUTOSAVE_INTERVAL, AUTOSAVE_ACTIVE_WINDOW,
)

jugadores_sse = {}

def autosave_worker():
    while True:
        try:
            time.sleep(AUTOSAVE_INTERVAL)
            with _active_players_lock:
                now_ts = time.time()
                for uid in list(_active_players.keys()):
                    if now_ts - _active_players[uid] >= AUTOSAVE_ACTIVE_WINDOW:
                        del _active_players[uid]
        except Exception as e:
            logger.error("[X] [ERROR] Monitor de jugadores error: " + str(e))

def sse_register(user_id):
    if user_id not in jugadores_sse:
        jugadores_sse[user_id] = queue.Queue()
    return jugadores_sse[user_id]

def sse_notify(user_id, mensaje):
    if user_id in jugadores_sse:
        jugadores_sse[user_id].put(mensaje)