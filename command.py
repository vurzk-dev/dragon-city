import json
import time
import random
import math
import traceback

from flask import Blueprint, request

from logging_config import logger
from paths import SRV_DIR
from engine import (
    sign_packet,
    build_items_index, build_dragon_db, get_breed_result,
    generate_black_market_boxes, level_from_xp,
)
from get_game_config import load_game_config, get_item_config
from get_player_info import load_player, save_player
from sessions import sse_notify

bp = Blueprint('command', __name__)

comandos_añadidos = ['buy','buy_egg','hatch_egg','feed_dragon','set_goals','complete_goal','breed_dragon','move','store_item','place_stored_egg','place_stored_dragon','dragonarium_place_stored','sell','sell_egg','sell_dragon','sell_stored_item','sell_stored_dragon','orient','level_up','complete_tutorial','collect','expand_gold', 'expand_cash','activate','finish_building','upgrade','rename_dragon','speed_collect','speed_hatch','sync','ping','finish_breeding2','expand_island','move_dragon','buy_treasure_new','set_attack_team','deus_cards_generate','deus_cards_claim','begin_tournament','end_tournament','admin_speed_tournament','start_training','speed_training','finish_training','weekly_reward','place_stored_item','buy_treasure_popup','complete_collection','dragonarium_push','dragonarium_pull','dragonarium_add','attack_player','set_help_map','end_attack_f','assist_neighbor','clean_received_assists','assist_receive','kompu_boxes_new_list','kompu_boxes_open_box','kompu_boxes_claim_prize']

nombres_dragon = ["Roxy", "Horacio", "Sergi", "Kasia", "Xavi", "Draco", "Ignis", "Gabriel", "Abdona", "Adolfina", "Agripina", "Aleja", "Altagracia", "Amadora", "Amelia", "Anatolia", "Aniceta", "Antolina", "Apolonia", "Arcadia", "Argimira", "Atanasia", "Áurea", "Balbina", "Baltasara", "Basilisa", "Bercia", "Bernabea", "Bernarda", "Blacina", "Blasina", "Brígida", "Bonifacia", "Calista", "Casilda", "Castora", "Cayetana", "Celedonia", "Celestina", "Celina", "Cesárea", "Clementa", "Crisanta", "Crisóstoma", "Críspula", "Cristeta", "Dámasa", "Demetria", "Diega", "Dionisia", "Dominga", "Dominica", "Dorotea", "Dosinda", "Edelmira", "Edicta", "Eduvigis", "Efigenia", "Eleuteria", "Elicia", "Emerenciana", "Emeteria", "Ermisinda", "Escolástica", "Esmaragda", "Esmerencia", "Estanislá", "Etelvina", "Eudosia", "Eulogia", "Eustaquia", "Ezequiela", "Evarista", "Facunda", "Fausta", "Felicia", "Felisa", "Feliciana", "Froilana", "Fulgencia", "Gaspara", "Gelsumina", "Genoveva", "Getrudis", "Gertrudis", "Gervasia", "Gliceria", "Gracia", "Graciana", "Gregoria", "Guillerma", "Gumersinda", "Felicia", "Fidela", "Froilana", "Hermelinda", "Herminia", "Hilaria", "Humildad", "Indalecia", "Ilora", "Isidora", "Isidra", "Jacoba", "Jerónima", "Jesusa", "Jorja", "Juliana", "Laureana", "Leocadia", "Leoncia", "Liberata", "Librada", "Lopa", "Lorenza", "Luciana", "Lucrecia", "Mamesa", "Marciala", "Marciana", "Matea", "Matiasa", "Máxima", "Melchora", "Melitona", "Micaela", "Miguela", "Montserrate", "Nazaria", "Nemesia", "Nestora", "Nicanora", "Nicasia", "Jacinta", "Jesusa", "Olalla", "Olaya", "Orosia", "Parda", "Paspasia", "Patrocinia", "Peregrina", "Perpétua", "Petra", "Petrola", "Petrona", "Petronila", "Pia", "Polonia", "Pomposa", "Potencia", "Práxedes", "Preciosa", "Prisca", "Priscila", "Quintina", "Quiteria", "Ramira", "Reparada", "Ricarda", "Romualda", "Rudesinda", "Rufa", "Rufina", "Salvadora", "Sancia", "Sandalia", "Santas", "Santiaga", "Saturia", "Saturnina", "Sebastiana", "Segunda", "Semproniana", "Serapia", "Sergia", "Silvestra", "Simeona", "Simona", "Socorro", "Sotera", "Teodomira", "Teodora", "Teodosia", "Tiburcia", "Tomasa", "Toribia", "Úrsula", "Abundio", "Acacio", "Agapito", "Amalio", "Ambrosio", "Aniceto", "Anselmo", "Apolonio", "Aquilino", "Argimiro", "Arquimimo", "Arsenio", "Ascensio", "Asterio", "Atanasio", "Atilano", "Áureo", "Avelino", "Bartolo", "Basilio", "Baudilio", "Belarmino", "Benigno", "Bonifacio", "Buenaventura", "Calisto", "Calixto", "Casiano", "Casildo", "Castiano", "Casimiro", "Cecilio", "Celdonio", "Celedonio", "Cesáreo", "Cipriaco", "Cipriano", "Cipriniano", "Ciriaco", "Cirilo", "Clemente", "Cleto", "Columbano", "Conrado", "Crescencio", "Crisóstomo", "Crispín", "Críspulo", "Cruz", "Deogracias", "Dionisio", "Domiciano", "Doroteo", "Eleuterio", "Eliodoro", "Eliseo", "Emerico", "Emeterio", "Emmanuel", "Epafrodito", "Epifanio", "Escolástico", "Estanislao", "Eufrasio", "Eulogio", "Evelio", "Fabriciano", "Faustina", "Feliciano", "Florencio", "Floro", "Froilán", "Fructuoso", "Frutos", "Fulgencio", "Gregorio", "Guadalupe", "Gumersindo", "Helimenas", "Hermenegildo", "Herminio", "Hermógenes", "Higinio", "Hilario", "Hilarión", "Hipólito", "Indalecio", "Inocente", "Isabelo", "Isidoro", "Juvernón", "Laureano", "Leandro", "Leocadio", "León", "Leovigildo", "Lesmes", "Lisardo", "Lope", "Lupicinio", "Macabeo", "Macario", "Macedonio", "Margarito", "Magin", "Mauro", "Maximino", "Medardo", "Melitón", "Minervino", "Minervo", "Natalio", "Nemesio", "Nicanor", "Niceto", "Nicomedes", "Norberto", "Odón", "Orencio", "Pantaleón", "Paulilo", "Paulino", "Patricio", "Perfecto", "Petrolino", "Petronilo", "Pío", "Policarpo", "Polonio", "Pomposo", "Ponciano", "Primitivo", "Protasio", "Prudencio", "Regino", "Remigio", "Restituto", "Rinaldo", "Robustiano", "Romualdo", "Rómulo", "Rosalino", "Ruperto", "Rufino", "Rufo", "Sabas", "Sabiniano", "Salvio", "Sandalio", "Saturio", "Saturnino", "Serapio", "Servando", "Serbando", "Severo", "Silverio", "Silvestre", "Silvio", "Simeón", "Sinforosio", "Sinforoso", "Sofío", "Sofronio", "Sotero", "Teódulo", "Telesforo", "Teopisto", "Tereso", "Tiburcio", "Timoteo", "Toribio", "Trifón", "Trinitario", "Ulpiano", "Valeriano", "Venancio", "Victoriano", "Zoilo"]

FOOD_COSTS = [
    0, 5, 10, 20, 40, 80, 160, 320, 640, 1280,
    1664, 2163, 2812, 3656, 4753, 6178, 8032, 10441,
    13574, 17646, 22940, 29822, 38768, 50398, 65518,
    88173, 110725, 143943, 187126, 243264, 316243,
    411115, 534450, 694785, 903220, 1174187,
    1526443, 1984375, 2579688, 3353594, 4359673
]

@bp.route('/static/dragoncity/srv/packet.php', methods=['POST', 'GET'])
@bp.route('/static/dragoncity/packet.php', methods=['POST', 'GET'])
def packet_handler():
    user_id = request.args.get('USERID') or request.form.get('id')
    response_results = []

    if request.method == 'POST':
        data_raw = request.form.get('data', '')
        if ';' in data_raw:
            json_str = data_raw.split(';', 1)[1]
        else:
            json_str = data_raw

        try:
            payload      = json.loads(json_str)
            player_data  = load_player(user_id)
            game_config  = load_game_config(user_id)
            items_index  = build_items_index(game_config)
            commands     = payload.get('commands', [])

            for cmd_data in commands:
                cmd        = cmd_data.get('cmd')
                cmd_number = cmd_data.get('number')
                args       = cmd_data.get('args', [])
                cmd_result = "ok"

                try:
                    if cmd == 'buy':
                        iso_id, item_id, tx, ty, p_id, frame, flag = str(args[0]), args[1], args[2], args[3], args[4], args[5], args[6]
                        item_cfg = items_index.get(str(item_id))
                        for item in game_config.get('items', []):
                            if str(item.get('id')) == str(item_id):
                                item_cfg = item
                                break

                        if item_cfg:
                            group_type = item_cfg.get('group_type', '')
                            costs      = item_cfg.get('costs', {})
                            gold_cost  = costs.get('g', 0)
                            cash_cost  = costs.get('c', 0)

                            if gold_cost > 0:
                                player_data['playerInfo']['gold'] = max(0, player_data['playerInfo']['gold'] - gold_cost)
                            if cash_cost > 0:
                                player_data['playerInfo']['cash'] = max(0, player_data['playerInfo']['cash'] - cash_cost)

                            build_time = item_cfg.get('build_time', 0)
                            attributes = {}
                            current_ts = player_data.get('timestamp', int(time.time()))

                            if group_type == 'HABITAT':
                                attributes['ar']  = 0
                                attributes['lat'] = current_ts

                            if build_time > 0:
                                attributes['tb'] = current_ts + build_time
                            else:
                                xp_gain = item_cfg.get('xp', 0)
                                player_data['playerInfo']['xp'] += xp_gain

                            player_data['map']['items'][iso_id] = [item_id, tx, ty, p_id, frame, flag, attributes]

                    elif cmd == 'buy_egg':
                        egg_uid, dragon_id = args[0], args[1]
                        item_cfg = None
                        for item in game_config.get('items', []):
                            if str(item.get('id')) == str(dragon_id):
                                item_cfg = item
                                break

                        if item_cfg:
                            costs     = item_cfg.get('costs', {})
                            gold_cost = costs.get('g', 0)
                            cash_cost = costs.get('c', 0)

                            if gold_cost > 0:
                                player_data['playerInfo']['gold'] = max(0, player_data['playerInfo']['gold'] - gold_cost)
                            if cash_cost > 0:
                                player_data['playerInfo']['cash'] = max(0, player_data['playerInfo']['cash'] - cash_cost)

                            xp_gain = item_cfg.get('xp', 0)
                            player_data['playerInfo']['xp'] += xp_gain

                            if 'eggs' not in player_data['map']:
                                player_data['map']['eggs'] = []

                            player_data['map']['eggs'].append({
                                "id": egg_uid, "type": dragon_id, "name": random.choice(nombres_dragon),
                                "xp": 0, "hatched": False, "ts": int(time.time())
                            })

                    elif cmd == 'hatch_egg':
                        egg_uid, habitat_uid, dragon_name = args[0], args[2], args[3]
                        habitat_id = str(args[2])
                        current_ts = player_data.get('timestamp', int(time.time()))

                        if habitat_id in player_data['map']['items']:
                            item_data = player_data['map']['items'][habitat_id]
                            if len(item_data) > 6 and isinstance(item_data[6], dict) and 'ar' in item_data[6]:
                                item_data[6]['lat'] = current_ts
                                del item_data[6]['ar']

                        egg_data = None
                        if 'eggs' in player_data['map']:
                            for i, egg in enumerate(player_data['map']['eggs']):
                                if str(egg.get('id')) == str(egg_uid):
                                    egg_data = player_data['map']['eggs'].pop(i)
                                    break

                        if egg_data:
                            dragon_type_id = egg_data.get('type')
                            item_cfg       = get_item_config(game_config, dragon_type_id)

                            if item_cfg:
                                player_data['playerInfo']['xp'] += item_cfg.get('xp', 0)
                                attacks  = item_cfg.get('attacks', 0)

                                if 'dragons' not in player_data['map']:
                                    player_data['map']['dragons'] = []

                                player_data['map']['dragons'].append({
                                    "id": egg_uid, "type": dragon_type_id, "xp": 0,
                                    "habitatId": habitat_uid, "name": dragon_name,
                                    "ts": int(time.time()), "work_id": [], "nbKill": 0, "attack": attacks
                                })

                                if 'ownedDragons' not in player_data['map']:
                                    player_data['map']['ownedDragons'] = {}

                                id_str = str(dragon_type_id)
                                if id_str not in player_data['map']['ownedDragons']:
                                    player_data['map']['ownedDragons'][id_str] = [1, 0, 0]

                    elif cmd == 'feed_dragon':
                        dragon_uid = args[0]
                        if 'dragons' in player_data['map']:
                            for dragon in player_data['map']['dragons']:
                                if str(dragon.get('id')) == str(dragon_uid):
                                    current_xp    = dragon.get('xp', 0)
                                    current_level = (current_xp // 4) + 1

                                    if current_level >= len(FOOD_COSTS):
                                        break

                                    food_cost = FOOD_COSTS[current_level]

                                    if player_data['playerInfo']['food'] >= food_cost:
                                        player_data['playerInfo']['food'] -= food_cost
                                        dragon['xp'] = current_xp + 1
                                        new_level    = (dragon['xp'] // 4) + 1

                                        dragon_type_str = str(dragon.get('type'))
                                        if 'ownedDragons' not in player_data['map']:
                                            player_data['map']['ownedDragons'] = {}
                                        if dragon_type_str not in player_data['map']['ownedDragons']:
                                            player_data['map']['ownedDragons'][dragon_type_str] = [1, 0, 0]

                                        if new_level >= 4:
                                            player_data['map']['ownedDragons'][dragon_type_str][1] = 2
                                        if new_level >= 7:
                                            player_data['map']['ownedDragons'][dragon_type_str][2] = 3
                                    break

                    elif cmd == 'set_goals':
                        goal_id, goal_state = int(args[0]), json.loads(args[1])
                        if 'goals' not in player_data['privateState']:
                            player_data['privateState']['goals'] = [None] * 170
                        while len(player_data['privateState']['goals']) <= goal_id:
                            player_data['privateState']['goals'].append(None)
                        player_data['privateState']['goals'][goal_id] = goal_state

                    elif cmd == 'complete_goal':
                        goal_id     = int(args[0])
                        goal_config = game_config.get('goals', {}).get(str(goal_id))
                        if goal_config:
                            reward = goal_config.get('reward', {})
                            player_data['playerInfo']['gold'] += reward.get('g', 0)
                            player_data['playerInfo']['food'] += reward.get('f', 0)
                            player_data['playerInfo']['cash'] += reward.get('c', 0)
                            player_data['playerInfo']['xp']   += reward.get('x', 0)
                            player_data['privateState']['achievement_points'] += 35

                    elif cmd == 'breed_dragon':
                        iso_id, parent1_id, parent2_id, use_gems = str(args[0]), int(args[1]), int(args[2]), int(args[3])
                        current_ts = player_data.get('timestamp', int(time.time()))
                        boosted = False

                        if use_gems == 1:
                            boost_cost = game_config.get('globals', {}).get('RARITY_BOOST_COST', {}).get('value', 5)
                            if player_data['playerInfo']['cash'] >= int(boost_cost):
                                player_data['playerInfo']['cash'] -= int(boost_cost)
                                boosted = True

                        dragon1_type, dragon2_type = None, None
                        dragon1_level, dragon2_level = 1, 1

                        for d in player_data.get('map', {}).get('dragons', []):
                            if d.get('id') == parent1_id:
                                dragon1_type = d.get('type')
                                dragon1_level = (d.get('xp', 0) // 4) + 1
                            elif d.get('id') == parent2_id:
                                dragon2_type = d.get('type')
                                dragon2_level = (d.get('xp', 0) // 4) + 1

                        dragon_db = build_dragon_db(game_config)
                        outcome_id = get_breed_result(dragon1_type, dragon2_type, dragon1_level, dragon2_level, dragon_db, boosted) if dragon1_type and dragon2_type else 1011

                        duration = dragon_db[outcome_id]['breeding_time'] if outcome_id in dragon_db else 3600

                        if 'work' not in player_data['map']:
                            player_data['map']['work'] = {}

                        player_data['map']['work'][iso_id] = [parent1_id, parent2_id, current_ts, duration, outcome_id]
                        if iso_id in player_data['map'].get('items', {}):
                            player_data['map']['items'][iso_id][3] = current_ts

                        cmd_result = outcome_id

                    elif cmd == 'move':
                        iso_id, tx, ty, frame = str(args[0]), args[1], args[2], args[3]
                        if iso_id in player_data['map']['items']:
                            player_data['map']['items'][iso_id][1] = tx
                            player_data['map']['items'][iso_id][2] = ty
                            player_data['map']['items'][iso_id][4] = frame

                    elif cmd == 'store_item':
                        iso_id = str(args[0])
                        if iso_id in player_data['map']['items']:
                            item_id = str(player_data['map']['items'][iso_id][0])
                            del player_data['map']['items'][iso_id]
                            if 'store' not in player_data['map']: player_data['map']['store'] = {}
                            if 'items' not in player_data['map']['store']: player_data['map']['store']['items'] = {}
                            if item_id in player_data['map']['store']['items']:
                                player_data['map']['store']['items'][item_id] += 1
                            else:
                                player_data['map']['store']['items'][item_id] = 1

                    elif cmd == 'place_stored_egg':
                        egg_uid, dragon_id, is_gift = args[0], args[1], int(args[2])
                        item_cfg = get_item_config(game_config, dragon_id)
                        if item_cfg:
                            removed = False
                            if is_gift == 1:
                                if 'privateState' in player_data and 'giftsi' in player_data['privateState']:
                                    for i, gift in enumerate(player_data['privateState']['gifts']):
                                        if gift.get('iid') == dragon_id or gift.get('type') == dragon_id:
                                            player_data['privateState']['gifts'].pop(i)
                                            removed = True
                                            break
                            else:
                                if 'store' in player_data.get('map', {}):
                                    if 'dragons' in player_data['map']['store']:
                                        for i, d in enumerate(player_data['map']['store']['dragons']):
                                            if d.get('iid') == dragon_id:
                                                player_data['map']['store']['dragons'].pop(i)
                                                removed = True
                                                break
                                    if not removed and 'items' in player_data['map']['store']:
                                        str_dragon_id = str(dragon_id)
                                        if str_dragon_id in player_data['map']['store']['items']:
                                            if player_data['map']['store']['items'][str_dragon_id] > 1:
                                                player_data['map']['store']['items'][str_dragon_id] -= 1
                                            else:
                                                del player_data['map']['store']['items'][str_dragon_id]
                                            removed = True

                            if removed:
                                player_data['map']['eggs'].append({
                                    "id": egg_uid, "type": dragon_id, "name": random.choice(nombres_dragon),
                                    "xp": 0, "hatched": False, "ts": int(time.time())
                                })

                    elif cmd == 'place_stored_dragon':
                        dragon_uid, habitat_uid, dragon_name, dragon_type_id, dragon_lvl, is_gift = args[0], str(args[1]), args[2], int(args[3]), int(args[4]), int(args[5])
                        dragon_xp = 4 * dragon_lvl - 4
                        item_cfg = get_item_config(game_config, dragon_type_id)
                        if item_cfg:
                            removed = False
                            if is_gift == 1:
                                gifts_node = player_data.get('gifts') or player_data.get('privateState', {}).get('gifts') or player_data.get('map', {}).get('gifts')
                                if gifts_node and 'dragons' in gifts_node:
                                    for i, gift in enumerate(gifts_node['dragons']):
                                        if (isinstance(gift, dict) and (gift.get('iid') == dragon_type_id or gift.get('type') == dragon_type_id)) or (isinstance(gift, (str, int)) and str(gift) == str(dragon_type_id)):
                                            gifts_node['dragons'].pop(i)
                                            removed = True
                                            break
                            else:
                                if 'store' in player_data.get('map', {}) and 'dragons' in player_data['map']['store']:
                                    for i, stored_dragon in enumerate(player_data['map']['store']['dragons']):
                                        if (isinstance(stored_dragon, dict) and stored_dragon.get('iid') == dragon_type_id) or (isinstance(stored_dragon, (str, int)) and str(stored_dragon) == str(dragon_type_id)):
                                            player_data['map']['store']['dragons'].pop(i)
                                            removed = True
                                            break

                            current_ts = player_data.get('timestamp', int(time.time()))
                            if habitat_uid in player_data['map']['items']:
                                item_data = player_data['map']['items'][habitat_uid]
                                if len(item_data) > 6 and isinstance(item_data[6], dict) and 'ar' in item_data[6]:
                                    item_data[6]['lat'] = current_ts
                                    del item_data[6]['ar']

                            attacks = item_cfg.get('attacks', [])
                            player_data['map']['dragons'].append({
                                "id": dragon_uid, "type": dragon_type_id, "xp": dragon_xp,
                                "habitatId": habitat_uid, "name": dragon_name, "ts": current_ts,
                                "work_id": [], "nbKill": 0, "attack": attacks
                            })

                            id_str = str(dragon_type_id)
                            if id_str not in player_data['map']['ownedDragons']:
                                if dragon_xp >= 24: player_data['map']['ownedDragons'][id_str] = [1, 2, 3]
                                elif dragon_xp >= 12: player_data['map']['ownedDragons'][id_str] = [1, 2, 0]
                                else: player_data['map']['ownedDragons'][id_str] = [1, 0, 0]

                    elif cmd == 'dragonarium_place_stored':
                        dragon_name, dragon_type_id, dragon_lvl, is_gift = args[0], int(args[1]), int(args[2]), int(args[3])
                        dragon_uid = int(time.time() * 1000)
                        dragon_xp  = 4 * dragon_lvl - 4
                        item_cfg = get_item_config(game_config, dragon_type_id)
                        if item_cfg:
                            removed = False
                            if is_gift == 1:
                                gifts_node = player_data.get('gifts') or player_data.get('privateState', {}).get('gifts') or player_data.get('map', {}).get('gifts')
                                if gifts_node and 'dragons' in gifts_node:
                                    for i, gift in enumerate(gifts_node['dragons']):
                                        if (isinstance(gift, dict) and (gift.get('iid') == dragon_type_id or gift.get('type') == dragon_type_id)) or (isinstance(gift, (str, int)) and str(gift) == str(dragon_type_id)):
                                            gifts_node['dragons'].pop(i)
                                            removed = True
                                            break
                            else:
                                if 'store' in player_data.get('map', {}) and 'dragons' in player_data['map']['store']:
                                    for i, stored_dragon in enumerate(player_data['map']['store']['dragons']):
                                        if (isinstance(stored_dragon, dict) and stored_dragon.get('iid') == dragon_type_id) or (isinstance(stored_dragon, (str, int)) and str(stored_dragon) == str(dragon_type_id)):
                                            player_data['map']['store']['dragons'].pop(i)
                                            removed = True
                                            break

                            category_index = 0
                            attributes     = item_cfg.get('attributes', [])
                            if 'pu' in attributes: category_index = 4
                            elif 'l' in attributes: category_index = 3
                            elif 'd' in attributes: category_index = 2
                            elif 'm' in attributes: category_index = 1

                            current_ts = player_data.get('timestamp', int(time.time()))
                            player_data['privateState']['dragonarium'][category_index].append({
                                "id": dragon_uid, "type": dragon_type_id, "xp": dragon_xp,
                                "habitatId": 0, "name": dragon_name, "ts": current_ts,
                                "work_id": [], "nbKill": 0, "attack": item_cfg.get('attacks', [])
                            })

                            id_str = str(dragon_type_id)
                            if id_str not in player_data['map']['ownedDragons']:
                                if dragon_xp >= 24: player_data['map']['ownedDragons'][id_str] = [1, 2, 3]
                                elif dragon_xp >= 12: player_data['map']['ownedDragons'][id_str] = [1, 2, 0]
                                else: player_data['map']['ownedDragons'][id_str] = [1, 0, 0]

                    elif cmd == 'sell':
                        iso_id = str(args[0])
                        if iso_id in player_data['map']['items']:
                            item_type_id = str(player_data['map']['items'][iso_id][0])
                            item_cfg = get_item_config(game_config, item_type_id)
                            if item_cfg:
                                player_data['playerInfo']['gold'] += item_cfg.get('sell_price', {}).get('g', 0)
                            del player_data['map']['items'][iso_id]

                    elif cmd == 'sell_egg':
                        egg_uid = args[0]
                        egg_index = next((i for i, e in enumerate(player_data['map']['eggs']) if e.get('id') == egg_uid), None)
                        if egg_index is not None:
                            dragon_type = str(player_data['map']['eggs'][egg_index].get('type'))
                            item_cfg = get_item_config(game_config, dragon_type)
                            if item_cfg:
                                player_data['playerInfo']['gold'] += item_cfg.get('sell_price', {}).get('g', 0)
                            player_data['map']['eggs'].pop(egg_index)

                    elif cmd == 'sell_dragon':
                        dragon_uid = args[0]
                        dragon_index = next((i for i, d in enumerate(player_data['map']['dragons']) if d.get('id') == dragon_uid), None)
                        if dragon_index is not None:
                            dragon_type = str(player_data['map']['dragons'][dragon_index].get('type'))
                            item_cfg = get_item_config(game_config, dragon_type)
                            if item_cfg:
                                player_data['playerInfo']['gold'] += item_cfg.get('sell_price', {}).get('g', 0)
                            player_data['map']['dragons'].pop(dragon_index)

                    elif cmd == 'sell_stored_item':
                        item_id_to_sell = str(args[0])
                        item_cfg = get_item_config(game_config, item_id_to_sell)
                        if item_cfg:
                            sell_price = item_cfg.get('sell_price', {}).get('g', 0)
                            if 'store' in player_data['map'] and 'items' in player_data['map']['store']:
                                store_items = player_data['map']['store']['items']
                                if item_id_to_sell in store_items:
                                    if store_items[item_id_to_sell] > 1:
                                        store_items[item_id_to_sell] -= 1
                                    else:
                                        del store_items[item_id_to_sell]
                                    player_data['playerInfo']['gold'] += sell_price

                    elif cmd == 'sell_stored_dragon':
                        dragon_id, dragon_lvl, is_gift = int(args[0]), int(args[1]), int(args[2])
                        item_cfg = get_item_config(game_config, dragon_id)
                        if item_cfg:
                            sell_price = item_cfg.get('sell_price', {}).get('g', 0)
                            target_list = player_data.get('privateState', {}).get('gifts') if is_gift == 1 else player_data.get('map', {}).get('store', {}).get('dragons')
                            if target_list is not None:
                                index_to_remove = -1
                                for i, d in enumerate(target_list):
                                    if d.get('iid') == dragon_id and d.get('lvl') == dragon_lvl:
                                        index_to_remove = i
                                        break
                                if index_to_remove != -1:
                                    target_list.pop(index_to_remove)
                                    player_data['playerInfo']['gold'] += sell_price

                    elif cmd == 'orient':
                        iso_id, frame = str(args[0]), args[1]
                        if iso_id in player_data['map']['items']:
                            player_data['map']['items'][iso_id][4] = frame

                    elif cmd == 'level_up':
                        new_level = int(args[0])
                        player_data['playerInfo']['level'] = new_level
                        levels_config = game_config.get('levels', [])
                        if 0 <= new_level - 1 < len(levels_config):
                            reward = levels_config[new_level - 1].get('reward', {})
                            for reward_type, reward_amount in reward.items():
                                if reward_type == 'c': player_data['playerInfo']['cash'] += reward_amount
                                elif reward_type == 'g': player_data['playerInfo']['gold'] += reward_amount
                                elif reward_type == 'f': player_data['playerInfo']['food'] += reward_amount
                                elif reward_type == 'x': player_data['playerInfo']['xp'] += reward_amount

                        if new_level >= 5 and player_data['privateState'].get('BlackMarketTs', 0) == 0:
                            current_ts = player_data.get('timestamp', int(time.time()))
                            player_data['privateState']['BlackMarketTs'] = current_ts
                            retraso = random.randint(86400, 259200)
                            player_data['privateState']['BlackMarketStart'] = current_ts + retraso
                            player_data['privateState']['BlackMarketEnd']   = player_data['privateState']['BlackMarketStart'] + 259200
                            unique_dragon, cajas, cajas_mezcladas = generate_black_market_boxes(game_config)
                            player_data['privateState']['BlackMarketUniqueDragon']   = unique_dragon
                            player_data['privateState']['kompuBoxesDragons']         = cajas
                            player_data['privateState']['kompuBoxesShuffledDragons'] = cajas_mezcladas

                    elif cmd == 'complete_tutorial':
                        player_data['playerInfo']['completed_tutorial'] = str(args[0])

                    elif cmd in ['expand_gold', 'expand_cash']:
                        expansion_id = int(args[0])
                        prices_list  = game_config.get('expansion_prices', [])
                        current_idx  = len(player_data['map'].get('expansions', []))
                        if current_idx < len(prices_list):
                            price_data = prices_list[current_idx]
                            if cmd == 'expand_gold':
                                costo, recurso_key = int(price_data.get('coins', 0)), 'gold'
                            else:
                                costo, recurso_key = int(price_data.get('cash', 0)), 'cash'
                            if player_data['playerInfo'][recurso_key] >= costo:
                                player_data['playerInfo'][recurso_key] -= costo
                                if expansion_id not in player_data['map']['expansions']:
                                    player_data['map']['expansions'].append(expansion_id)

                    elif cmd == 'collect':
                        iso_id = str(args[0])
                        if iso_id in player_data['map']['items']:
                            item_data = player_data['map']['items'][iso_id]
                            while len(item_data) <= 6: item_data.append({})
                            if not isinstance(item_data[6], dict): item_data[6] = {}
                            attrs, current_ts = item_data[6], int(time.time())

                            if len(args) > 1 and isinstance(args[1], (int, float)):
                                player_data['playerInfo']['gold'] += int(args[1])
                                item_data[3], attrs['lat'] = current_ts, current_ts
                            elif len(args) > 1 and args[1] == "fc":
                                if 'cp' in attrs:
                                    cp_index = int(attrs['cp']) - 1
                                    collect_values = game_config.get('globals', {}).get('COLLECT_VALUES', {}).get('value', [])
                                    collect_xp     = game_config.get('globals', {}).get('COLLECT_XP', {}).get('value', [])
                                    if 0 <= cp_index < len(collect_values):
                                        player_data['playerInfo']['food'] += int(collect_values[cp_index])
                                        player_data['playerInfo']['xp']   += int(collect_xp[cp_index])
                                    del attrs['cp']
                                item_data[3] = 0
                            else:
                                item_data[3] = 0
                                if 'lat' in attrs: attrs['lat'] = current_ts

                    elif cmd == 'activate':
                        iso_id, cp_val = str(args[0]), args[1]
                        if iso_id in player_data['map']['items']:
                            item_data = player_data['map']['items'][iso_id]
                            while len(item_data) < 7: item_data.append({})
                            attrs = item_data[6]
                            item_cfg = next((item for item in game_config.get('items', []) if str(item.get('id')) == str(item_data[0])), None)
                            if item_cfg:
                                if item_cfg.get('group_type', '') == 'FARM' or 'multiCollectable' in item_cfg.get('properties', {}):
                                    if isinstance(cp_val, int) and cp_val > 0:
                                        collect_prices = game_config.get('globals', {}).get('COLLECT_PRICE', {}).get('value', [])
                                        if (cp_val - 1) < len(collect_prices):
                                            cost = collect_prices[cp_val - 1]
                                            if 'g' in cost: player_data['playerInfo']['gold'] = max(0, player_data['playerInfo']['gold'] - cost['g'])
                                            if 'c' in cost: player_data['playerInfo']['cash'] = max(0, player_data['playerInfo']['cash'] - cost['c'])
                                        attrs['cp'], item_data[3] = cp_val, int(time.time())
                                    elif cp_val == 0:
                                        attrs['cp'], item_data[3] = 0, 0
                                elif item_cfg.get('group_type', '') == 'OBSTACLE':
                                    costs = item_cfg.get('costs', {})
                                    if 'g' in costs: player_data['playerInfo']['gold'] = max(0, player_data['playerInfo']['gold'] - costs['g'])
                                    if 'c' in costs: player_data['playerInfo']['cash'] = max(0, player_data['playerInfo']['cash'] - costs['c'])
                                    item_data[3] = int(time.time())

                    elif cmd == 'finish_building':
                        iso_id = str(args[0])
                        if iso_id in player_data['map']['items']:
                            item_data = player_data['map']['items'][iso_id]
                            item_cfg  = get_item_config(game_config, item_data[0])
                            if item_cfg: player_data['playerInfo']['xp'] += item_cfg.get('xp', 0)
                            item_data[3] = 0
                            if len(item_data) > 6 and isinstance(item_data[6], dict) and 'tb' in item_data[6]:
                                del item_data[6]['tb']

                    elif cmd == 'upgrade':
                        unique_id = str(args[0])
                        if unique_id in player_data['map']['items']:
                            item_data, current_type_id = player_data['map']['items'][unique_id], str(player_data['map']['items'][unique_id][0])
                            all_items = game_config.get('items', {})
                            current_item_conf = all_items.get(current_type_id) if isinstance(all_items, dict) else next((i for i in all_items if str(i.get('id')) == current_type_id), None)
                            if current_item_conf and 'upgrades_to' in current_item_conf:
                                new_type_id = str(current_item_conf['upgrades_to'])
                                new_item_conf = all_items.get(new_type_id) if isinstance(all_items, dict) else next((i for i in all_items if str(i.get('id')) == new_type_id), None)
                                if new_item_conf:
                                    item_data[0] = int(new_type_id)
                                    build_time, current_ts = new_item_conf.get('build_time', 0), int(time.time())
                                    while len(item_data) < 7: item_data.append(0)
                                    if not isinstance(item_data[6], dict): item_data[6] = {}
                                    if build_time > 0:
                                        item_data[6]['tb'] = current_ts + build_time
                                    else:
                                        item_data[6].pop('tb', None)
                                        item_data[3] = 0

                    elif cmd == 'rename_dragon':
                        for dragon in player_data.get('map', {}).get('dragons', []):
                            if dragon.get('id') == args[0]:
                                dragon['name'] = str(args[1])
                                break

                    elif cmd == 'speed_collect':
                        unique_id = str(args[0])
                        if unique_id in player_data['map']['items']:
                            item_data = player_data['map']['items'][unique_id]
                            props = item_data[6] if len(item_data) > 6 and isinstance(item_data[6], dict) else {}
                            if 'cp' in props:
                                crop_id = int(props['cp'])
                                collect_minutes = game_config.get('globals', {}).get('COLLECT_MINUTES', {}).get('value', [0.5, 5, 30, 120, 360, 720, 1440, 2160, 2880])
                                if 1 <= crop_id <= len(collect_minutes):
                                    duration_seconds = int(collect_minutes[crop_id - 1] * 60)
                                    time_remaining = max(0, duration_seconds - (int(time.time()) - int(item_data[3])))
                                    gems_cost = max(1, (time_remaining + 3599) // 3600)
                                    if player_data['playerInfo']['cash'] >= gems_cost:
                                        player_data['playerInfo']['cash'] -= gems_cost
                                        item_data[3] = int(time.time()) - duration_seconds

                    elif cmd == 'speed_hatch':
                        egg_id = args[0]
                        if 'eggs' in player_data.get('map', {}):
                            egg_data = next((egg for egg in player_data['map']['eggs'] if egg.get('id') == egg_id), None)
                            if egg_data:
                                dragon_type = str(egg_data.get('type'))
                                all_items = game_config.get('items', [])
                                dragon_conf = all_items.get(dragon_type) if isinstance(all_items, dict) else next((i for i in all_items if str(i.get('id')) == dragon_type), None)
                                if dragon_conf:
                                    hatching_time = dragon_conf.get('hatching_time', 0)
                                    time_remaining = max(0, hatching_time - (int(time.time()) - int(egg_data.get('ts', 0))))
                                    gems_cost = max(1, (time_remaining + 3599) // 3600)
                                    if player_data['playerInfo']['cash'] >= gems_cost:
                                        player_data['playerInfo']['cash'] -= gems_cost
                                        egg_data['ts'] = int(time.time()) - hatching_time

                    elif cmd in ['sync', 'ping']:
                        pass

                    elif cmd == 'finish_breeding2':
                        breeding_iso_id, new_egg_uid, hatchery_iso_id = str(args[0]), args[1], str(args[2])
                        work_data = player_data.get('map', {}).get('work', {}).get(breeding_iso_id)
                        if work_data:
                            dragon_id = work_data[4]
                            if 'eggs' not in player_data['map']: player_data['map']['eggs'] = []
                            player_data['map']['eggs'].append({"id": new_egg_uid, "type": dragon_id, "name": random.choice(nombres_dragon), "xp": 0, "ts": int(time.time())})
                            del player_data['map']['work'][breeding_iso_id]
                            if breeding_iso_id in player_data['map'].get('items', {}): player_data['map']['items'][breeding_iso_id][3] = 0
                        cmd_result = dragon_id

                    elif cmd == 'expand_island':
                        expansion_id, cost_index = int(args[0]), int(args[1])
                        if 'expansions' not in player_data['map']: player_data['map']['expansions'] = []
                        if expansion_id not in player_data['map']['expansions']: player_data['map']['expansions'].append(expansion_id)
                        try:
                            islands_costs = game_config.get('globals', {}).get('ISLANDS_COSTS', {}).get('value', [])
                            if cost_index < len(islands_costs):
                                cost_item = islands_costs[cost_index]
                                cost_obj = cost_item.get('value', cost_item) if isinstance(cost_item, dict) else {}
                                for res_type, amount in cost_obj.items():
                                    amt = int(amount)
                                    if res_type == 'g': player_data['playerInfo']['gold'] = max(0, player_data['playerInfo']['gold'] - amt)
                                    elif res_type == 'c': player_data['playerInfo']['cash'] = max(0, player_data['playerInfo']['cash'] - amt)
                        except Exception: pass

                    elif cmd == 'move_dragon':
                        dragon_uid, new_habitat_id = int(args[0]), int(args[1])
                        for dragon in player_data.get('map', {}).get('dragons', []):
                            if int(dragon.get('id', 0)) == dragon_uid:
                                dragon['habitatId'] = new_habitat_id
                                break

                    elif cmd == 'buy_treasure_new':
                        treasure_id = str(args[0])
                        if 'treasure_items' in game_config and treasure_id in game_config['treasure_items']:
                            treasure_data = game_config['treasure_items'][treasure_id]
                            price, amount, res_type = int(treasure_data.get('price', 0)), int(treasure_data.get('amount', 0)), treasure_data.get('type', '')
                            if res_type == 'g': res_type = 'gold'
                            elif res_type == 'f': res_type = 'food'
                            if player_data.get('playerInfo', {}).get('cash', 0) >= price:
                                player_data['playerInfo']['cash'] -= price
                                player_data['playerInfo'][res_type] = player_data['playerInfo'].get(res_type, 0) + amount

                    elif cmd == 'set_attack_team':
                        team_type, team_ids_str = cmd_data.get('args')[0], cmd_data.get('args')[1]
                        team_ids = json.loads(team_ids_str)
                        if "teams" not in player_data["privateState"]: player_data["privateState"]["teams"] = {}
                        player_data["privateState"]["teams"][team_type] = [{"id": int(dragon_id)} for dragon_id in team_ids]

                    elif cmd == 'deus_cards_generate':
                        is_paid, is_super = int(args[0]) if len(args) > 0 else 0, int(args[1]) if len(args) > 1 else 0
                        if is_super == 1:
                            player_data['playerInfo']['cash'] = max(0, player_data['playerInfo']['cash'] - game_config.get('globals', {}).get('DRAGON_CARDS_SUPER_TRY', {}).get('value', 10))
                        elif is_paid == 1:
                            player_data['playerInfo']['cash'] = max(0, player_data['playerInfo']['cash'] - game_config.get('globals', {}).get('DRAGON_CARDS_TRY', {}).get('value', 3))
                        prize_id = random.randint(0, 8)
                        if 'deus_cards' not in player_data['privateState']: player_data['privateState']['deus_cards'] = {}
                        player_data['privateState']['deus_cards']['pending_prize'] = prize_id
                        cmd_result = prize_id

                    elif cmd == 'deus_cards_claim':
                        prize_id = player_data['privateState'].get('deus_cards', {}).get('pending_prize', 0)
                        prize_cfg = next((p for p in game_config.get('dragon_card_prizes', []) if p.get('id') == prize_id), None)
                        if prize_cfg:
                            reward = prize_cfg.get('reward', {})
                            if isinstance(reward, dict):
                                player_data['playerInfo']['gold'] += reward.get('g', 0)
                                player_data['playerInfo']['food'] += reward.get('f', 0)
                                player_data['playerInfo']['cash'] += reward.get('c', 0)
                            elif isinstance(reward, int):
                                player_data['map']['store']['dragons'].append({"iid": reward, "lvl": 0})
                        if 'deus_cards' in player_data['privateState']: player_data['privateState']['deus_cards']['pending_prize'] = None
                        player_data['privateState']['deusCardsLastTimestamp'] = int(time.time())

                    elif cmd == 'begin_tournament':
                        player_data['privateState']['beginTournamentTs'] = int(time.time())

                    elif cmd == 'end_tournament':
                        player_won, kills_log = str(args[0]) == "1", json.loads(args[1]) if len(args) > 1 else {}
                        current_ts = int(time.time())
                        player_data['privateState']['endTournamentTs'] = current_ts
                        if kills_log and 'dragons' in player_data.get('map', {}):
                            for dragon in player_data['map']['dragons']:
                                dragon_id_str = str(dragon.get('id'))
                                if dragon_id_str in kills_log: dragon['nbKill'] = dragon.get('nbKill', 0) + int(kills_log[dragon_id_str])
                        if player_won:
                            current_tourney = str(player_data['privateState'].get('currentTournament', 1))
                            tourney_data = game_config.get('tournaments', {}).get(current_tourney)
                            if tourney_data:
                                rewards = tourney_data.get('reward', {}).get('resources', {})
                                player_data['playerInfo']['gold'] += rewards.get('g', 0)
                                player_data['playerInfo']['food'] += rewards.get('f', 0)
                                player_data['playerInfo']['cash'] += rewards.get('c', 0)
                                player_data['privateState']['currentTournament'] = int(current_tourney) + 1
                                player_data['privateState']['achievement_points'] += 50

                    elif cmd == 'admin_speed_tournament':
                        speed_up_price = game_config.get('globals', {}).get('TOURNAMENT_SPEED_UP_PRICE', {}).get('value', 2)
                        cooldown_secs = game_config.get('globals', {}).get('TOURNAMENT_COOLDOWN', {}).get('value', 12) * 3600
                        if player_data['playerInfo']['cash'] >= speed_up_price:
                            player_data['playerInfo']['cash'] -= speed_up_price
                            player_data['privateState']['beginTournamentTs'] = max(0, player_data['privateState'].get('beginTournamentTs', 0) - cooldown_secs)

                    elif cmd == 'start_training':
                        building_uid, dragon_uid, attack_id, attack_pos = str(args[0]), args[1], args[2], args[3]
                        if 'work' not in player_data['map']: player_data['map']['work'] = {}
                        player_data['map']['work'][building_uid] = [dragon_uid, attack_id, int(time.time()), attack_pos]
                        for dragon in player_data.get('map', {}).get('dragons', []):
                            if str(dragon.get('id')) == str(dragon_uid): dragon['work_id'] = int(building_uid); break

                    elif cmd == 'speed_training':
                        building_uid = str(args[0])
                        if 'work' in player_data.get('map', {}) and building_uid in player_data['map']['work']:
                            work_data = player_data['map']['work'][building_uid]
                            attack_id, start_ts, current_ts = int(work_data[1]), int(work_data[2]), int(time.time())
                            dragon_uid, attack_pos = str(work_data[0]), int(work_data[3])
                            training_time = game_config.get('attacks', {}).get(attack_id, {}).get('training_time', 0)
                            speed_up_cost = max(1, math.ceil(max(0, training_time - (current_ts - start_ts)) / 3600.0))
                            if player_data['playerInfo']['cash'] >= speed_up_cost:
                                player_data['playerInfo']['cash'] -= speed_up_cost
                                player_data['map']['work'][building_uid][2] = current_ts - training_time - 10
                            dragon_found = False
                            for dragon in player_data.get('map', {}).get('dragons', []):
                                if str(dragon.get('id')) == dragon_uid:
                                    dragon_found = True
                                    if 'attack' not in dragon or not isinstance(dragon['attack'], list): dragon['attack'] = [-1, -1, -1, -1]
                                    while len(dragon['attack']) <= attack_pos: dragon['attack'].append(-1)
                                    dragon['attack'][attack_pos], dragon['work_id'] = attack_id, []
                                    break
                            if dragon_found: del player_data['map']['work'][building_uid]

                    elif cmd == 'finish_training':
                        building_uid = str(args[0])
                        if 'work' in player_data.get('map', {}) and building_uid in player_data['map']['work']:
                            work_data = player_data['map']['work'][building_uid]
                            dragon_uid, attack_id, attack_pos = str(work_data[0]), int(work_data[1]), int(work_data[3])
                            dragon_found = False
                            for dragon in player_data.get('map', {}).get('dragons', []):
                                if str(dragon.get('id')) == dragon_uid:
                                    dragon_found = True
                                    if 'attack' not in dragon or not isinstance(dragon['attack'], list): dragon['attack'] = [-1, -1, -1, -1]
                                    while len(dragon['attack']) <= attack_pos: dragon['attack'].append(-1)
                                    dragon['attack'][attack_pos], dragon['work_id'] = attack_id, []
                                    break
                            if dragon_found: del player_data['map']['work'][building_uid]

                    elif cmd == 'weekly_reward':
                        reward_args = json.loads(args[0])
                        reward_index, dragon_index = int(reward_args[0]), int(reward_args[1]) if len(reward_args) > 1 else 0
                        monday_rewards = game_config.get('globals', {}).get('MONDAY_BONUS_REWARDS', {}).get('value', [])
                        monday_dragons = game_config.get('globals', {}).get('MONDAY_BONUS_REWARDS_DRAGONS', {}).get('value', [])
                        if reward_index < len(monday_rewards):
                            reward = monday_rewards[reward_index]
                            r_type, r_value = reward.get('type'), reward.get('value', 0)
                            if r_type == 'g': player_data['playerInfo']['gold'] += r_value
                            elif r_type == 'c': player_data['playerInfo']['cash'] += r_value
                            elif r_type == 'f': player_data['playerInfo']['food'] += r_value
                            elif r_type == 'u':
                                dragon_id = monday_dragons[dragon_index] if dragon_index < len(monday_dragons) else 1011
                                if 'eggs' not in player_data['map']: player_data['map']['eggs'] = []
                                player_data['map']['eggs'].append({"id": int(time.time()) + random.randint(1000, 9999), "type": dragon_id, "name": "Bonus", "xp": 0, "hatched": False, "ts": int(time.time())})
                            if 'privateState' not in player_data: player_data['privateState'] = {}
                            player_data['privateState']['timeStampMondayBonus'] = int(time.time())

                    elif cmd == 'place_stored_item':
                        iso_id, item_id, tx, ty = str(args[0]), str(args[1]), args[2], args[3]
                        item_found = False
                        if 'store' in player_data['map'] and 'items' in player_data['map']['store'] and item_id in player_data['map']['store']['items']:
                            item_found = True
                            if player_data['map']['store']['items'][item_id] > 1: player_data['map']['store']['items'][item_id] -= 1
                            else: del player_data['map']['store']['items'][item_id]
                            if not player_data['map']['store']['items']: del player_data['map']['store']['items']
                        if item_found: player_data['map']['items'][iso_id] = [int(item_id), int(tx), int(ty), 0, 0, 1, {}]

                    elif cmd == 'buy_treasure_popup':
                        treasure_id = int(args[0])
                        treasures_db = {
                            1: {"type": "gold", "amount": 75000,  "price": 15}, 2: {"type": "gold", "amount": 200000, "price": 30},
                            3: {"type": "gold", "amount": 500000, "price": 80}, 5: {"type": "food", "amount": 10000,  "price": 15},
                            6: {"type": "food", "amount": 22500,  "price": 30}, 7: {"type": "food", "amount": 70000,  "price": 80},
                        }
                        if treasure_id in treasures_db:
                            treasure = treasures_db[treasure_id]
                            if player_data['playerInfo']['cash'] >= treasure["price"]:
                                player_data['playerInfo']['cash'] -= treasure["price"]
                                if treasure["type"] == "food": player_data['playerInfo']['food'] += treasure["amount"]
                                elif treasure["type"] == "gold": player_data['playerInfo']['gold'] += treasure["amount"]

                    elif cmd == 'complete_collection':
                        collection_id = int(args[0])
                        if 'completedCollection' not in player_data['privateState']: player_data['privateState']['completedCollection'] = []
                        if collection_id not in player_data['privateState']['completedCollection']:
                            player_data['privateState']['completedCollection'].append(collection_id)
                            collection_found = next((col for col in game_config.get('collections', []) if col.get('id') == collection_id), None)
                            if collection_found:
                                rewards = collection_found.get('reward', {})
                                player_data['playerInfo']['gold'] += rewards.get("g", 0)
                                player_data['playerInfo']['food'] += rewards.get("f", 0)
                                player_data['playerInfo']['cash'] += rewards.get("c", 0)
                                player_data['playerInfo']['xp']   += rewards.get("x", 0)
                                player_data['privateState']['achievement_points'] += 75

                    elif cmd == 'dragonarium_push':
                        dragon_id = int(args[0])
                        if 'dragonariumSlot' not in player_data['privateState'] or len(player_data['privateState'].get('dragonariumSlot', [])) < 5: player_data['privateState']['dragonariumSlot'] = [2, 2, 2, 1, 1]
                        if 'dragonarium' not in player_data['privateState'] or len(player_data['privateState'].get('dragonarium', [])) < 5: player_data['privateState']['dragonarium'] = [[], [], [], [], []]
                        dragon_to_move = next((d for d in player_data.get('map', {}).get('dragons', []) if d.get('id') == dragon_id), None)
                        if dragon_to_move:
                            dragon_type, category_index = dragon_to_move.get('type'), 0
                            item_data = next((item for item in game_config.get('items', []) if item.get('id') == dragon_type), None)
                            if item_data:
                                attributes = item_data.get('attributes', [])
                                if 'pu' in attributes: category_index = 4
                                elif 'l' in attributes: category_index = 3
                                elif 'd' in attributes: category_index = 2
                                elif 'm' in attributes: category_index = 1
                            dragon_to_move['habitatId'] = 0
                            player_data['privateState']['dragonarium'][category_index].append(dragon_to_move)
                            player_data['map']['dragons'].remove(dragon_to_move)

                    elif cmd == 'dragonarium_pull':
                        category_index, dragon_index, target_habitat_id = int(args[1]), int(args[2]), int(args[3])
                        dragonarium = player_data.get('privateState', {}).get('dragonarium', [])
                        if 0 <= category_index < len(dragonarium) and 0 <= dragon_index < len(dragonarium[category_index]):
                            dragon_to_move = dragonarium[category_index].pop(dragon_index)
                            dragon_to_move['habitatId'] = target_habitat_id
                            if 'map' not in player_data: player_data['map'] = {}
                            if 'dragons' not in player_data['map']: player_data['map']['dragons'] = []
                            player_data['map']['dragons'].append(dragon_to_move)

                    elif cmd == 'dragonarium_add':
                        slot_index = int(args[0])
                        player_data['playerInfo']['cash'] -= [2, 2, 3, 4, 5][slot_index]
                        if 'dragonariumSlot' not in player_data['privateState'] or len(player_data['privateState'].get('dragonariumSlot', [])) < 5: player_data['privateState']['dragonariumSlot'] = [2, 2, 2, 1, 1]
                        player_data['privateState']['dragonariumSlot'][slot_index] += 1

                    elif cmd == 'set_help_map':
                        help_id = str(args[0])
                        if 'helpMap' not in player_data['privateState']: player_data['privateState']['helpMap'] = []
                        if help_id not in player_data['privateState']['helpMap']: player_data['privateState']['helpMap'].append(help_id)

                    elif cmd == 'attack_player':
                        target_player_id, current_time = str(args[0]), int(time.time())
                        units = []
                        try:
                            with open(os.path.join(SRV_DIR, 'pvp_players_info.json'), 'r', encoding='utf-8') as f: pvp_db = json.load(f)
                            if target_player_id in pvp_db:
                                victim_data = pvp_db[target_player_id]
                                pvp_team_ids = [d['id'] for d in victim_data.get('privateState', {}).get('teams', {}).get('pvp', [])]
                                dragons_by_id = {d['id']: d for d in victim_data.get('map', {}).get('dragons', [])}
                                for dragon_id in pvp_team_ids:
                                    dragon = dragons_by_id.get(dragon_id)
                                    if dragon: units.append({"name": dragon.get("name", "Dragon"), "type": dragon["type"], "lvl": level_from_xp(dragon.get("xp", 0), dragon["type"]), "id": dragon["id"]})
                        except Exception: pass
                        if 'privateState' not in player_data: player_data['privateState'] = {}
                        if 'attacksSent' not in player_data['privateState']: player_data['privateState']['attacksSent'] = []
                        player_data['privateState']['attacksSent'].append({"victim_id": target_player_id, "time": current_time})
                        cmd_result = units

                    elif cmd == 'end_attack_f':
                        target_player_id, position, win_status = str(args[0]), int(args[1]), int(args[2])
                        kills_log = json.loads(args[3]) if len(args) > 3 and args[3] else {}
                        if win_status == 1:
                            if 'universAttackWin' not in player_data['map']: player_data['map']['universAttackWin'] = []
                            player_data['privateState']['achievement_points'] += 35
                            target_found = False
                            for i, entry in enumerate(player_data['map']['universAttackWin']):
                                if isinstance(entry, list) and len(entry) >= 3 and str(entry[0]) == target_player_id:
                                    player_data['map']['universAttackWin'][i], target_found = position, True
                                    break
                            if not target_found: player_data['map']['universAttackWin'].append(position)
                        if kills_log and 'dragons' in player_data['map']:
                            for dragon in player_data['map']['dragons']:
                                if str(dragon.get('id')) in kills_log: dragon['nbKill'] = dragon.get('nbKill', 0) + int(kills_log[str(dragon.get('id'))])
                        victories = len(player_data['map'].get('universAttackWin', []))
                        if win_status == 1 and victories >= 7:
                            player_data['playerInfo']['pvpLevel'] = player_data['playerInfo'].get('pvpLevel', 1) + 1
                            player_data['privateState']['achievement_points'] += 120
                            player_data['map']['universAttackWin'] = []
                            cmd_result = True
                        else: cmd_result = None

                    elif cmd == 'assist_neighbor':
                        target_player_id, clicks = str(args[0]), json.loads(args[1])
                        victim_data = load_player(target_player_id)
                        victim_data.setdefault("map", {})
                        if not isinstance(victim_data["map"].get("receivedAssists"), dict): victim_data["map"]["receivedAssists"] = {}
                        victim_data["map"]["receivedAssists"].setdefault("u" + str(user_id), []).extend(clicks)
                        save_player(victim_data, target_player_id)

                    elif cmd == 'clean_received_assists':
                        received = player_data.get("map", {}).get("receivedAssists", {})
                        if isinstance(received, dict) and "u" + str(args[0]) in received: del received["u" + str(args[0])]

                    elif cmd == 'assist_receive':
                        item_type_id = int(args[0])
                        group_type = next((item.get("group_type", "") for item in game_config.get("items", []) if item.get("id") == item_type_id), None)
                        player_data["playerInfo"]["xp"]   += 10
                        if group_type == "HABITAT": player_data["playerInfo"]["gold"] += 10
                        elif group_type == "FARM": player_data["playerInfo"]["food"] += 10

                    elif cmd in ['kompu_boxes_new_list', 'kompu_boxes_claim_prize']:
                        if cmd == 'kompu_boxes_new_list': player_data['playerInfo']['cash'] -= 3
                        else:
                            current_opened = player_data['privateState'].get('kompuBoxesOpened', 0)
                            kompu_dragons  = player_data['privateState'].get('kompuBoxesDragons', [])
                            if current_opened > 0 and len(kompu_dragons) >= current_opened:
                                player_data['map']['store']['dragons'].append({"iid": kompu_dragons[current_opened - 1], "lvl": 0})
                            player_data['privateState']['kompuBoxesOpened'] = 0

                        unique_dragon_id = game_config.get('kompu_offers', [{}])[0].get('rewards', {}).get('uniqueDragonId')
                        dragons_cat_234 = [i['id'] for i in game_config.get('items', []) if i.get('group_type') == 'DRAGON' and i.get('category') in [2, 3, 4]]
                        dragons_cat_4   = [i['id'] for i in game_config.get('items', []) if i.get('group_type') == 'DRAGON' and i.get('category') == 4]
                        dragons_cat_5   = [i['id'] for i in game_config.get('items', []) if i.get('group_type') == 'DRAGON' and i.get('category') == 5]
                        pool_dragons = random.sample(dragons_cat_234, min(4, len(dragons_cat_234)))
                        while len(pool_dragons) < 4: pool_dragons.append(random.choice(dragons_cat_234))
                        pool_dragons.append(random.choice(dragons_cat_4))
                        if unique_dragon_id and random.random() <= 0.10: pool_dragons.append(unique_dragon_id)
                        else: pool_dragons.append(random.choice(dragons_cat_5))
                        player_data['privateState']['kompuBoxesDragons'] = pool_dragons[:]
                        shuffled = pool_dragons[:]
                        random.shuffle(shuffled)
                        player_data['privateState']['kompuBoxesShuffledDragons'] = shuffled
                        cmd_result = {"kompuBoxesDragons": pool_dragons, "kompuBoxesShuffledDragons": shuffled}

                    elif cmd == 'kompu_boxes_open_box':
                        current_opened = player_data['privateState'].get('kompuBoxesOpened', 0)
                        player_data['playerInfo']['cash'] -= 20 if current_opened == 0 else 10
                        if current_opened < 6: player_data['privateState']['kompuBoxesOpened'] = current_opened + 1

                except Exception as e:
                    logger.error("[X] [ERROR] Fallo en comando '" + str(cmd) + "': " + str(e))
                    traceback.print_exc()

                response_results.append({
                    "result": cmd_result, "number": cmd_number, "cmd": cmd,
                    "resources": {"pu": {"gold": player_data['playerInfo']['gold'], "cash": player_data['playerInfo']['cash'], "food": player_data['playerInfo']['food'], "xp": player_data['playerInfo']['xp']}},
                    "error": None
                })

            save_player(player_data, user_id)
            player_data['timestamp'] = int(time.time())
            sse_notify(user_id, "JUEGO_GUARDADO")

        except Exception as e:
            logger.error("[X] [ERROR] Fallo procesando packet.php: " + str(e))
            traceback.print_exc()

    return sign_packet({"result": True, "response": response_results, "ts": int(time.time()), "publishActions": 0})