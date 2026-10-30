import json
import os

from logging_config import logger
from paths import SRV_DIR, SAVES_DIR

_GAME_CONFIG_CACHE = {}

def load_game_config(user_id=None):
    if user_id:
        user_path = os.path.join(SAVES_DIR, str(user_id), 'get_game_config.json')
        path = user_path if os.path.exists(user_path) else os.path.join(SRV_DIR, 'get_game_config.json')
    else:
        path = os.path.join(SRV_DIR, 'get_game_config.json')

    cached = _GAME_CONFIG_CACHE.get(path)
    mtime = os.path.getmtime(path)

    if cached and cached['mtime'] == mtime:
        return cached['data']

    with open(path, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())

    _GAME_CONFIG_CACHE[path] = {'data': data, 'mtime': mtime}
    return data

def get_item_config(config, model_id):
    model_id_str = str(model_id)
    for item in config.get('items', []):
        if str(item.get('id')) == model_id_str:
            return item
    return None