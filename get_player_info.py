import json
import os
import time
import shutil

from logging_config import logger
from paths import SRV_DIR, SAVES_DIR, VILLAGES_DIR, _active_players, _active_players_lock
from version import migrate_loaded_save

def _iter_village_files():
    if not os.path.isdir(VILLAGES_DIR):
        return
    for nombre in os.listdir(VILLAGES_DIR):
        if nombre.endswith('.json'):
            yield os.path.join(VILLAGES_DIR, nombre)

def _load_village_by_pid(user_id):
    target = str(user_id)
    for path in _iter_village_files():
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            logger.error("[X] [ERROR] No se pudo leer village " + path + ": " + str(e))
            continue
        pid = data.get('playerInfo', {}).get('pid')
        if pid is not None and str(pid) == target:
            return data
    return None

def inject_default_neighbors(player_data):
    neighbors = []
    for path in _iter_village_files():
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            logger.error("[X] [ERROR] No se pudo leer village " + path + ": " + str(e))
            continue
        info = data.get('playerInfo', {})
        pid = info.get('pid')
        if pid is None:
            continue
        neighbors.append({
            "pid": pid,
            "fbid": pid,
            "name": info.get('name', ''),
            "pic": info.get('pic', ''),
            "xp": info.get('xp', 0),
            "level": info.get('level', 1),
            "world_id": info.get('world_id', pid),
        })
    player_data['neighbors'] = neighbors
    return player_data

def load_player(user_id):
    user_dir      = os.path.join(SAVES_DIR, str(user_id))
    user_file     = os.path.join(user_dir, f"{user_id}.json")
    template_file = os.path.join(SRV_DIR, 'get_player_info.json')

    if not os.path.exists(user_file):
        village_data = _load_village_by_pid(user_id)
        if village_data is not None:
            village_data['timestamp'] = int(time.time())
            migrate_loaded_save(village_data)
            return village_data

        os.makedirs(user_dir, exist_ok=True)
        for nombre in ['get_game_config.json', 'get_pvp_isle.json', 'pvp_players_info.json']:
            src = os.path.join(SRV_DIR, nombre)
            dst = os.path.join(user_dir, nombre)
            if os.path.exists(src):
                shutil.copy2(src, dst)

        if not os.path.exists(template_file):
            logger.critical("[!!] [CRÍTICO] Plantilla inexistente en " + SRV_DIR)
            return {}
        with open(template_file, 'r', encoding='utf-8') as f:
            player_data = json.load(f)

        migrate_loaded_save(player_data)
        inject_default_neighbors(player_data)
    else:
        with open(user_file, 'r', encoding='utf-8') as f:
            player_data = json.load(f)
        migrate_loaded_save(player_data)

    player_data['timestamp'] = int(time.time())
    return player_data

def save_player(state, user_id):
    user_dir = os.path.join(SAVES_DIR, str(user_id))
    os.makedirs(user_dir, exist_ok=True)
    path = os.path.join(user_dir, f"{user_id}.json")

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

    with _active_players_lock:
        _active_players[str(user_id)] = time.time()