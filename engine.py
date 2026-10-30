import json
import os
import time
import hmac
import hashlib
import random

from logging_config import logger
from paths import SRV_DIR, SECRET_KEY

def sign_packet(payload_dict):
    json_payload = json.dumps(payload_dict, separators=(',', ':'))
    signature = hmac.new(
        SECRET_KEY.encode('utf-8'),
        json_payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return f"{signature};{json_payload}"

WEIGHT_DIFFICULTY         = {1: 55, 2: 25, 3: 5}
WEIGHT_DIFFICULTY_BOOSTED = {1: 40, 2: 35, 3: 25}

CATEGORY_MULTIPLIER = {
    1: 0.65, 2: 0.90, 3: 0.55, 4: 0.22, 5: 0.15,
}

LEGENDARY_COMBOS_BY_ATTRS = {
    frozenset({'w','p','i','f'}): [1041, 1054],
    frozenset({'e','m','f','i'}): [1041, 1052, 1053, 1054],
    frozenset({'w','p','f','i'}): [1052, 1053],
    frozenset({'w','d'}):         [1052],
}

LEGENDARY_FROM_COMBO_CHANCE = 15.0
PURE_DRAGON_BASE_ID = 1081
PURE_CHANCE_BASE    = 3.0
PURE_CHANCE_BOOSTED = 5.0
PURE_ELEMENT_IDS = [1082, 1083, 1084, 1085, 1086, 1087, 1088, 1089]
PURE_ELEMENT_CHANCE_BASE    = 5.0
PURE_ELEMENT_CHANCE_BOOSTED = 7.5

def build_items_index(config):
    return {str(item.get('id')): item for item in config.get('items', [])}

def build_dragon_db(config):
    db = {}
    for item in config.get('items', []):
        if item.get('group_type') != 'DRAGON':
            continue
        db[item['id']] = {
            'name':          item.get('name', 'Unknown'),
            'attributes':    set(item.get('attributes', [])),
            'difficulty':    item.get('difficulty', 3),
            'category':      item.get('category', 1),
            'breeding_time': item.get('breeding_time', 86400),
            'breedable':     item.get('breedable', 0),
        }
    return db

def get_breed_result(dragon1_type, dragon2_type, level1, level2, dragon_db, boosted=False):
    if dragon1_type not in dragon_db or dragon2_type not in dragon_db:
        return 1011

    parent1 = dragon_db[dragon1_type]
    parent2 = dragon_db[dragon2_type]
    pool    = parent1['attributes'] | parent2['attributes']

    is_leg1 = 'l' in parent1['attributes']
    is_leg2 = 'l' in parent2['attributes']

    if is_leg1 != is_leg2:
        valid_any = [
            dtype for dtype, ddata in dragon_db.items()
            if ddata['breedable'] > 0 and level1 >= ddata['breedable'] and level2 >= ddata['breedable']
        ]
        if valid_any:
            return random.choice(valid_any)

    if is_leg1 and is_leg2:
        pure_chance = PURE_CHANCE_BOOSTED if boosted else PURE_CHANCE_BASE
        pe_chance   = PURE_ELEMENT_CHANCE_BOOSTED if boosted else PURE_ELEMENT_CHANCE_BASE
        roll = random.uniform(0, 100)

        if roll < pure_chance:
            if PURE_DRAGON_BASE_ID in dragon_db:
                return PURE_DRAGON_BASE_ID
        elif roll < pure_chance + pe_chance:
            pure_with_el = [
                did for did, dd in dragon_db.items()
                if 'pu' in dd['attributes'] and len(dd['attributes']) > 1 and dd['attributes'] != {'pu'}
            ]
            if not pure_with_el:
                pure_with_el = [i for i in PURE_ELEMENT_IDS if i in dragon_db]
            if pure_with_el:
                return random.choice(pure_with_el)

    if boosted:
        key = frozenset(pool)
        if key in LEGENDARY_COMBOS_BY_ATTRS:
            if random.uniform(0, 100) < LEGENDARY_FROM_COMBO_CHANCE:
                possible = [lid for lid in LEGENDARY_COMBOS_BY_ATTRS[key] if lid in dragon_db]
                if possible:
                    return random.choice(possible)

    candidates = []
    weights_diff = WEIGHT_DIFFICULTY_BOOSTED if boosted else WEIGHT_DIFFICULTY

    for dtype, ddata in dragon_db.items():
        if ddata['breedable'] == 0:
            continue
        if level1 < ddata['breedable'] or level2 < ddata['breedable']:
            continue

        attrs = ddata['attributes']
        if not attrs or not attrs.issubset(pool) or 'l' in attrs or 'pu' in attrs:
            continue

        diff = ddata['difficulty']
        cat  = ddata['category']
        base_w = weights_diff.get(diff, 5)
        mult   = CATEGORY_MULTIPLIER.get(cat, 0.01)
        final_w = base_w * mult

        if final_w > 0:
            candidates.append((dtype, final_w))

    if not candidates:
        return dragon1_type

    total = sum(w for _, w in candidates)
    r     = random.uniform(0, total)
    cumulative = 0
    for dtype, w in candidates:
        cumulative += w
        if r <= cumulative:
            return dtype

    return candidates[-1][0]

def generate_black_market_boxes(user_game_config):
    cat_1, cat_2_3, cat_4_5, cat_3_4_5 = [], [], [], []
    cat_4, cat_5 = [], []

    for item in user_game_config.get('items', []):
        if item.get('group_type') == 'DRAGON' and 'category' in item:
            cat = item['category']
            d_id = item['id']
            if cat == 1: cat_1.append(d_id)
            elif cat in [2, 3]: cat_2_3.append(d_id)
            if cat == 4: cat_4.append(d_id)
            if cat == 5: cat_5.append(d_id)
            if cat in [4, 5]: cat_4_5.append(d_id)
            if cat in [3, 4, 5]: cat_3_4_5.append(d_id)

    unique_dragon = random.choice(cat_3_4_5) if cat_3_4_5 else 1041
    kompu_boxes = []

    if len(cat_2_3) >= 3:
        kompu_boxes.extend(random.sample(cat_2_3, 3))
    else:
        kompu_boxes.extend(cat_2_3)
        while len(kompu_boxes) < 3: kompu_boxes.append(1011)

    if len(cat_4) >= 2:
        kompu_boxes.extend(random.sample(cat_4, 2))
    else:
        kompu_boxes.extend(cat_4)
        while len(kompu_boxes) < 5: kompu_boxes.append(1011)

    if random.randint(1, 100) <= 10:
        kompu_boxes.append(unique_dragon)
    else:
        kompu_boxes.append(random.choice(cat_5) if cat_5 else 1041)

    kompu_shuffled = list(kompu_boxes)
    random.shuffle(kompu_shuffled)
    return unique_dragon, kompu_boxes, kompu_shuffled

def build_kompu_offers_payload(user_game_config, start_timestamp, unique_dragon):
    cat_1, cat_2_3, cat_4_5, cat_3_4_5 = [], [], [], []
    for item in user_game_config.get('items', []):
        if item.get('group_type') == 'DRAGON' and 'category' in item:
            cat = item['category']
            d_id = item['id']
            if cat == 1: cat_1.append(d_id)
            elif cat in [2, 3]: cat_2_3.append(d_id)
            if cat in [4, 5]: cat_4_5.append(d_id)
            if cat in [3, 4, 5]: cat_3_4_5.append(d_id)

    pool_x2 = random.sample(cat_1, min(10, len(cat_1))) if cat_1 else [1011]
    pool_x3 = random.sample(cat_2_3, min(10, len(cat_2_3))) if cat_2_3 else [1011]
    pool_x4 = random.sample(cat_4_5, min(7, len(cat_4_5))) if cat_4_5 else [1041]
    pool_x5 = random.sample(cat_3_4_5, min(5, len(cat_3_4_5))) if cat_3_4_5 else [1041]

    return [{
        "id": 1, "starts_at": start_timestamp, "duration": 259200, "game_type": 4,
        "resetable": 0, "pick_prize": 0, "hurry_up_cost": 10, "timer_between": 21600,
        "viral_icon": [], "rewards": {"uniqueDragonId": unique_dragon, "prizes": [pool_x2, pool_x3, pool_x4, pool_x5]}
    }]

def check_and_update_black_market(player_data, user_id, game_config):
    current_ts = player_data.get('timestamp', 0)
    bm_start = int(player_data['privateState']['BlackMarketStart'] or 0)
    bm_end   = int(player_data['privateState']['BlackMarketEnd'] or 0)

    if bm_start == 0 or bm_end == 0:
        return player_data, game_config

    config_modificado = False

    if current_ts >= bm_end:
        game_config['kompu_offers'] = []
        player_data['privateState']['BlackMarketTs'] = current_ts
        nuevo_descanso = random.randint(259200, 604800)
        player_data['privateState']['BlackMarketStart'] = current_ts + nuevo_descanso
        player_data['privateState']['BlackMarketEnd']   = player_data['privateState']['BlackMarketStart'] + 259200

        unique_dragon, cajas, cajas_mezcladas = generate_black_market_boxes(game_config)
        player_data['privateState']['BlackMarketUniqueDragon']   = int(unique_dragon)
        player_data['privateState']['kompuBoxesDragons']         = cajas
        player_data['privateState']['kompuBoxesShuffledDragons'] = cajas_mezcladas
        config_modificado = True

    elif current_ts >= bm_start and current_ts < bm_end:
        if not game_config.get('kompu_offers'):
            unique_dragon = int(player_data.get('BlackMarketUniqueDragon', 1041))
            game_config['kompu_offers'] = build_kompu_offers_payload(game_config, bm_start, unique_dragon)
            config_modificado = True

    if config_modificado:
        user_dir = os.path.join(SRV_DIR, str(user_id))
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        user_config_path = os.path.join(user_dir, 'get_game_config.json')
        with open(user_config_path, 'w', encoding='utf-8') as f:
            json.dump(game_config, f, separators=(',', ':'))

    return player_data, game_config

def level_from_xp(xp, dragon_type=None):
    if not xp or xp <= 0:
        return 1
    calculated_level = (xp // 4) + 1
    if calculated_level > 40:
        calculated_level = 40
    return int(calculated_level)