import os
import time
import json
import base64
import queue
import shutil
import socket
import threading
import atexit

from flask import Flask, request, jsonify, send_from_directory, send_file

from logging_config import logger
from paths import (
    TEMPLATES_DIR, FLASH_DIR, ASSETS_DIR, DOMAIN_MAP_DIR,
    SRV_DIR, SAVES_DIR, HOSTS_PATH, HOSTS_ENTRIES, MARKER,
    _active_players, _active_players_lock,
)
from engine import sign_packet
from get_game_config import load_game_config
from get_player_info import load_player, save_player
from sessions import autosave_worker, sse_register
from version import version_n, version_c
from assetsbundlecache import asset_cache
import command

WEB_ASSETS_DIR    = TEMPLATES_DIR
WEB_ASSET_FOLDERS = ('css', 'js', 'javascript', 'img', 'img_v2', 'xmls', 'avatars', 'icons', 'legacy')

app = Flask(__name__)
app.register_blueprint(command.bp)

def add_hosts():
    with open(HOSTS_PATH, 'r', encoding='utf-8') as f: contenido = f.read()
    if MARKER in contenido: return
    with open(HOSTS_PATH, 'a', encoding='utf-8') as f:
        f.write(f"\n{MARKER}\n")
        for entry in HOSTS_ENTRIES: f.write(f"{entry}\n")
        f.write(f"{MARKER}\n")

def remove_hosts():
    with open(HOSTS_PATH, 'r', encoding='utf-8') as f: lineas = f.readlines()
    nuevas_lineas, dentro_del_bloque = [], False
    for linea in lineas:
        if MARKER in linea:
            dentro_del_bloque = not dentro_del_bloque
            continue
        if not dentro_del_bloque: nuevas_lineas.append(linea)
    with open(HOSTS_PATH, 'w', encoding='utf-8') as f: f.writelines(nuevas_lineas)

atexit.register(remove_hosts)

def socket_policy_server(port=5840):
    policy_xml = (
        '<?xml version="1.0"?><!DOCTYPE cross-domain-policy SYSTEM "http://www.adobe.com/xml/dtds/cross-domain-policy.dtd">'
        '<cross-domain-policy><site-control permitted-cross-domain-policies="all"/><allow-access-from domain="*" to-ports="*" />'
        '<allow-http-request-headers-from domain="*" headers="*" /></cross-domain-policy>\0'
    ).encode('utf-8')
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(('127.0.0.1', port))
    srv.listen(20)
    while True:
        conn, addr = srv.accept()
        try:
            conn.recv(1024)
            conn.sendall(policy_xml)
        except Exception: pass
        finally: conn.close()

@app.route('/')
@app.route('/login.html')
def serve_login(): return send_from_directory(TEMPLATES_DIR, 'login.html')

@app.route('/index.html')
def serve_game():
    user_id, player_name = request.args.get('fb_sig_user'), request.args.get('player_name')
    if user_id and player_name:
        player_data = load_player(user_id)
        if 'playerInfo' in player_data and not player_data['playerInfo'].get('name', ''):
            player_data['playerInfo']['name'], player_data['playerInfo']['pid'] = player_name, user_id
            save_player(player_data, user_id)
    return send_from_directory(TEMPLATES_DIR, 'index.html')

def _register_web_asset_folder(folder):
    root = os.path.join(WEB_ASSETS_DIR, folder)
    def _serve(path):
        cached = asset_cache.get(f"{folder}/{path}")
        if cached and os.path.exists(cached): return send_file(cached)
        return send_from_directory(root, path)
    app.add_url_rule('/' + folder + '/<path:path>', endpoint='web_asset_' + folder, view_func=_serve)

for _folder in WEB_ASSET_FOLDERS: _register_web_asset_folder(_folder)

@app.route('/version')
def get_version(): return jsonify({"version_n": version_n, "version_c": version_c})

@app.route('/flash/<path:path>')
def serve_flash(path):
    cached = asset_cache.get(f"flash/{path}")
    if cached and os.path.exists(cached): return send_file(cached)
    return send_from_directory(FLASH_DIR, path)

@app.route('/assets/<path:path>')
def serve_assets(path):
    cached = asset_cache.get(f"assets/{path}")
    if cached and os.path.exists(cached): return send_file(cached)
    return send_from_directory(ASSETS_DIR, path)

@app.route('/ajax/libs/swfobject/2.2/swfobject.js')
def serve_swfobject():
    file_path = os.path.join(DOMAIN_MAP_DIR, 'ajax.googleapis.com', 'ajax', 'libs', 'swfobject', '2.2', 'swfobject.js')
    if os.path.exists(file_path): return send_from_directory(os.path.dirname(file_path), 'swfobject.js')
    return "No encontrado", 404

@app.route('/sp-translations.socialpointgames.com/crossdomain.xml')
@app.route('/crossdomain.xml')
def serve_crossdomain():
    path = os.path.join(DOMAIN_MAP_DIR, 'api.omniata.com', 'crossdomain.xml')
    if os.path.exists(path): return send_from_directory(os.path.dirname(path), 'crossdomain.xml')
    return '<?xml version="1.0"?><cross-domain-policy><allow-access-from domain="*"/></cross-domain-policy>', 200, {'Content-Type': 'application/xml'}

@app.route('/deploy/dc/canvas/prod/<filename>')
def serve_translations(filename):
    translations_dir = os.path.join(DOMAIN_MAP_DIR, 'sp-translations.socialpointgames.com', 'deploy', 'dc', 'canvas', 'prod')
    if os.path.exists(os.path.join(translations_dir, filename)): return send_from_directory(translations_dir, filename)
    return jsonify({"error": "Translation file not found"}), 404

_GIF_B64 = "R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
_GIF_RAW = b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
try: PIXEL_GIF = base64.b64decode(_GIF_B64)
except Exception: PIXEL_GIF = _GIF_RAW

@app.route('/__utm.gif')
@app.route('/ga.js')
def serve_ga_stub(): return PIXEL_GIF, 200, {'Content-Type': 'image/gif'}

@app.route('/static/dragoncity/srv/sync_error_track.php', methods=['POST', 'GET'])
@app.route('/static/dragoncity/sync_error_track.php', methods=['POST', 'GET'])
def sync_error_handler(): return ("", 200)

@app.route('/static/dragoncity/srv/track_game_status.php', methods=['GET', 'POST'])
@app.route('/static/dragoncity/track_game_status.php', methods=['GET', 'POST'])
def track_status_handler():
    user_id = (request.args.get('USERID') or request.form.get('USERID') or request.args.get('user_id') or request.form.get('user_id') or request.args.get('user') or request.form.get('user') or request.args.get('id') or request.form.get('id'))
    if user_id:
        with _active_players_lock: _active_players[str(user_id)] = time.time()

    response_data = {"result": True, "user_id": str(user_id) if user_id else "", "status": request.form.get('status', ''), "installId": request.form.get('installId', ''), "ts": int(time.time())}
    response = app.response_class(response=sign_packet(response_data), status=200, mimetype='text/plain')
    response.headers['Cache-Control'], response.headers['Pragma'] = 'no-store, no-cache, must-revalidate', 'no-cache'
    return response

@app.route('/static/dragoncity/deity_world/track/open', methods=['POST'])
@app.route('/static/dragoncity/deity_world/track/watch-tutorial', methods=['POST'])
def deity_world_track(): return jsonify({"result": True}), 200

@app.route('/stream')
def stream():
    user_id = request.args.get('USERID')
    if not user_id: return "USERID requerido", 400
    q = sse_register(user_id)
    def event_stream():
        while True:
            try: yield f"data: {q.get(timeout=20)}\n\n"
            except queue.Empty: yield "data: PING\n\n"
            except Exception: break
    return app.response_class(event_stream(), mimetype='text/event-stream')

@app.route('/static/dragoncity/srv/<path:filename>', methods=['GET', 'POST'])
@app.route('/static/dragoncity/<path:filename>', methods=['GET', 'POST'])
def srv_handler(filename):
    user_id = request.args.get('USERID') or request.form.get('USERID')
    target_id = request.form.get('user') or request.args.get('user')
    is_visiting = bool(target_id and target_id not in ('0', '', user_id))
    if is_visiting: user_id = target_id

    if filename in ('get_game_config.json', 'get_game_config.php'):
        response = app.response_class(response=sign_packet(load_game_config(user_id)), status=200, mimetype='text/plain')
        response.headers['Cache-Control'], response.headers['Pragma'] = 'no-store, no-cache, must-revalidate', 'no-cache'
        return response

    if filename in ('get_pvp_isle.json', 'get_pvp_isle.php', 'get_pvp_isle_info.php'):
        level, PAGE_SIZE = int(request.args.get('level', 1)), 8
        path = os.path.join(SRV_DIR, str(user_id), 'get_pvp_isle.json')
        if not os.path.exists(path): path = os.path.join(SRV_DIR, 'get_pvp_isle.json')
        with open(path, 'r', encoding='utf-8') as f: all_opponents = json.load(f)
        page = all_opponents[(level - 1) * PAGE_SIZE : (level - 1) * PAGE_SIZE + PAGE_SIZE]
        response = app.response_class(response=sign_packet(page), status=200, mimetype='text/plain')
        response.headers['Cache-Control'], response.headers['Pragma'] = 'no-store, no-cache, must-revalidate', 'no-cache'
        return response

    if filename in ('get_player_info.json', 'get_player_info.php'):
        from engine import check_and_update_black_market
        player_data = load_player(user_id)
        if 'playerInfo' in player_data:
            if not player_data['playerInfo'].get('pid'): player_data['playerInfo']['pid'] = user_id
            if not is_visiting:
                player_data, _ = check_and_update_black_market(player_data, user_id, load_game_config(user_id))
                save_player(player_data, user_id)
        return sign_packet(player_data), 200, {'Content-Type': 'text/plain; charset=utf-8'}

    return jsonify({"result": "200"})

@app.route('/delete_profile', methods=['POST'])
def delete_profile():
    try:
        user_id = request.get_json(force=True).get('user_id')
        if not user_id: return jsonify({"status": "error", "msg": "user_id requerido"}), 400
        user_dir = os.path.join(SAVES_DIR, str(user_id))
        if os.path.exists(user_dir):
            shutil.rmtree(user_dir)
            return jsonify({"status": "ok", "deleted": True})
        return jsonify({"status": "ok", "deleted": False})
    except Exception as e: return jsonify({"status": "error", "msg": str(e)}), 500

@app.route('/list_players', methods=['GET'])
def list_players():
    players = []
    if os.path.isdir(SAVES_DIR):
        for entry in os.listdir(SAVES_DIR):
            user_dir = os.path.join(SAVES_DIR, entry)
            user_file = os.path.join(user_dir, f"{entry}.json")
            if not os.path.isdir(user_dir) or not os.path.exists(user_file): continue
            try:
                with open(user_file, 'r', encoding='utf-8') as f: info = json.load(f).get('playerInfo', {}) or {}
                players.append({
                    'file': f"{entry}.json", 'pid': str(info.get('pid', entry) or entry), 'name': info.get('name', 'Desconocido') or 'Desconocido',
                    'level': info.get('level', 1), 'xp': info.get('xp', 0), 'gold': info.get('gold', 0), 'food': info.get('food', 0),
                    'cash': info.get('cash', 0), 'modified': int(os.path.getmtime(user_file)),
                })
            except Exception: pass
    players.sort(key=lambda s: s['modified'], reverse=True)
    return jsonify({'saves': players})

if __name__ == '__main__':
    asset_cache.build()
    add_hosts()

    threading.Thread(target=socket_policy_server, args=(5840,), daemon=True).start()
    threading.Thread(target=autosave_worker, daemon=True).start()

    print(f"Dragon City Reborn {version_n} {version_c}")
    print("Servidor creado por (vurzk-dev) Markut")
    print("-" * 50)
    print("Servidor listo. Abre http://127.0.0.1:80 en tu navegador.")
    print("-" * 50)

    app.run(host='127.0.0.1', port=80, debug=False, threaded=True)