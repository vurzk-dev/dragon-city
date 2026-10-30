import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] [%(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("constants")


class Constant:
    CATEGORIES = {
        1:  {"name": "Village",      "subs": [11, 12, 13, 14, 15, 16, 17, 18, 19, 110, 111, 112]},
        2:  {"name": "Defense",      "subs": [21, 22, 23, 24, 25, 26, 27, 28, 29, 210, 211, 212]},
        3:  {"name": "Army",         "subs": [32, 33, 34, 35, 36]},
        4:  {"name": "Decorations",  "subs": [41, 42, 43, 44]},
        5:  {"name": "Wonders",      "subs": []},
        6:  {"name": "",             "subs": [61, 62]},
        12: {"name": "New",          "subs": [121, 122]},
    }

    SUBCATEGORIES = {
        11: "Terra",   12: "Flame",   13: "Sea",    14: "Nature",
        15: "Electric",16: "Ice",     17: "Metal",  18: "Dark",
        19: "Light",   110: "War",    111: "Pure",  112: "Legend",
        21: "Terra",   22: "Flame",   23: "Sea",    24: "Nature",
        25: "Electric",26: "Ice",     27: "Metal",  28: "Dark",
        29: "Light",   210: "War",    211: "Pure",  212: "Legend",
        32: "Farms",   33: "Crystals",34: "Breeding",
        35: "Specials",36: "Temples",
        41: "Tiles",   42: "Plants",  43: "Flags",  44: "Others",
        61: "Gold",    62: "Food",    121: "Dragons",122: "Others",
    }

    GROUP_DRAGON           = "DRAGON"
    GROUP_HABITAT          = "HABITAT"
    GROUP_FARM             = "FARM"
    GROUP_BUILDING         = "BUILDING"
    GROUP_BOOSTER          = "BOOSTER"
    GROUP_DECO             = "DECO"
    GROUP_OBSTACLE         = "OBSTACLE"
    GROUP_SOCIAL_BUILDING  = "SOCIAL BUILDING"
    GROUP_COLLECTISLAND    = "COLLECTISLAND"
    GROUP_PROMOISLAND      = "PROMOISLAND"
    GROUP_CROSSPROMOTION   = "CROSSPROMOTION"
    GROUP_MISTERY_EGG      = "MISTERY_EGG"
    GROUP_LOSTITEM         = "LOSTITEM"
    GROUP_ATREZZO          = "ATREZZO"
    GROUP_POPUP            = "POPUP"
    GROUP_UNIT             = "UNIT"
    GROUP_CALENDAR_ISLAND  = "CALENDAR_ISLAND"

    ELEM_TERRA     = "e"
    ELEM_FLAME     = "f"
    ELEM_SEA       = "w"
    ELEM_NATURE    = "p"
    ELEM_ELECTRIC  = "el"
    ELEM_ICE       = "i"
    ELEM_METAL     = "m"
    ELEM_DARK      = "d"
    ELEM_LIGHT     = "li"
    ELEM_WAR       = "wr"
    ELEM_PURE      = "pu"
    ELEM_LEGEND    = "l"
    ELEM_PHYSICAL  = "ph"

    ELEMENT_NAMES = {
        "e": "Terra",    "f": "Flame",   "w": "Sea",
        "p": "Nature",   "el": "Electric","i": "Ice",
        "m": "Metal",    "d": "Dark",    "li": "Light",
        "wr": "War",     "pu": "Pure",   "l": "Legend",
        "ph": "Physical"
    }

    OPPOSITE_ELEMENTS = {
        "e":  {"e":0.5,"f":1,  "w":0,  "p":2,  "el":1, "i":1,  "m":0.5,"d":2,  "l":1, "pu":1, "li":1, "wr":1},
        "f":  {"e":0.5,"f":0.5,"w":2,  "p":1,  "el":1, "i":2,  "m":0,  "d":1,  "l":1, "pu":1, "li":1, "wr":1},
        "w":  {"e":1,  "f":2,  "w":0.5,"p":0,  "el":2, "i":1,  "m":1,  "d":1,  "l":1, "pu":1, "li":1, "wr":2},
        "p":  {"e":1,  "f":1,  "w":0.5,"p":0.5,"el":1, "i":1,  "m":1,  "d":2,  "l":1, "pu":1, "li":2, "wr":0},
        "el": {"e":0,  "f":2,  "w":1,  "p":1,  "el":0.5,"i":1, "m":2,  "d":0.5,"l":1, "pu":1, "li":1, "wr":1},
        "i":  {"e":1,  "f":1,  "w":1,  "p":2,  "el":1, "i":0.5,"m":1,  "d":0,  "l":1, "pu":1, "li":0.5,"wr":2},
        "m":  {"e":2,  "f":0.5,"w":1,  "p":1,  "el":0, "i":2,  "m":0.5,"d":1,  "l":1, "pu":1, "li":1, "wr":1},
        "d":  {"e":1,  "f":1,  "w":1,  "p":1,  "el":1, "i":0.5,"m":2,  "d":0.5,"l":1, "pu":1, "li":2, "wr":1},
        "l":  {"e":1,  "f":1,  "w":1,  "p":1,  "el":1, "i":1,  "m":1,  "d":1,  "l":2, "pu":1, "li":1, "wr":1},
        "ph": {"e":1,  "f":1,  "w":1,  "p":1,  "el":1, "i":1,  "m":1,  "d":1,  "l":0.5,"pu":1, "li":1, "wr":1},
        "pu": {"e":1,  "f":1,  "w":1,  "p":1,  "el":1, "i":1,  "m":1,  "d":1,  "l":1, "pu":0.5,"li":1, "wr":1},
        "li": {"e":1,  "f":0,  "w":1,  "p":0.5,"el":2, "i":1,  "m":1,  "d":2,  "l":1, "pu":1, "li":0.5,"wr":1},
        "wr": {"e":2,  "f":1,  "w":2,  "p":1,  "el":0.5,"i":0, "m":1,  "d":1,  "l":1, "pu":1, "li":1, "wr":0.5},
    }

    BREED_OPPOSITE = {
        "e": ["m"], "f": ["i"], "p": ["el"], "el": ["p"],
        "i": ["f"], "m": ["e"], "w": ["wr"], "wr": ["w"],
        "li": ["d"], "d": ["li"],
    }

    CAT_COMMON    = 1
    CAT_UNCOMMON  = 2
    CAT_RARE      = 3
    CAT_EPIC      = 4
    CAT_LEGENDARY = 5

    DRAGON_CATEGORY_NAMES = {
        1: "Common", 2: "Uncommon", 3: "Rare", 4: "Epic", 5: "Legendary"
    }

    DIFF_EASY   = 1
    DIFF_MEDIUM = 2
    DIFF_HARD   = 3

    RES_GOLD = "gold"
    RES_FOOD = "food"
    RES_CASH = "cash"
    RES_XP   = "xp"

    COST_GOLD = "g"
    COST_CASH = "c"
    COST_FOOD = "f"
    COST_XP   = "x"

    MAP_ITEMS              = "items"
    MAP_DRAGONS            = "dragons"
    MAP_EGGS               = "eggs"
    MAP_WORK               = "work"
    MAP_STORE              = "store"
    MAP_EXPANSIONS         = "expansions"
    MAP_OWNED_DRAGONS      = "ownedDragons"
    MAP_UNIVERS_ATTACK_WIN = "universAttackWin"
    MAP_RECEIVED_ASSISTS   = "receivedAssists"
    MAP_ISLAND_NUMBER      = "islandNumber"

    PS_GOALS                     = "goals"
    PS_TEAMS                     = "teams"
    PS_DRAGONARIUM               = "dragonarium"
    PS_DRAGONARIUM_SLOT          = "dragonariumSlot"
    PS_ACHIEVEMENT_POINTS        = "achievement_points"
    PS_BLACK_MARKET_START        = "BlackMarketStart"
    PS_BLACK_MARKET_END          = "BlackMarketEnd"
    PS_BLACK_MARKET_TS           = "BlackMarketTs"
    PS_BLACK_MARKET_UNIQUE_DRAGON= "BlackMarketUniqueDragon"
    PS_KOMPU_BOXES_DRAGONS       = "kompuBoxesDragons"
    PS_KOMPU_BOXES_SHUFFLED      = "kompuBoxesShuffledDragons"
    PS_KOMPU_BOXES_OPENED        = "kompuBoxesOpened"
    PS_ATTACKS_SENT              = "attacksSent"
    PS_HELP_MAP                  = "helpMap"
    PS_TIME_STAMP_MONDAY_BONUS   = "timeStampMondayBonus"
    PS_DEUS_CARDS_LAST_TIMESTAMP = "deusCardsLastTimestamp"
    PS_CURRENT_TOURNAMENT        = "currentTournament"
    PS_BEGIN_TOURNAMENT_TS       = "beginTournamentTs"
    PS_END_TOURNAMENT_TS         = "endTournamentTs"
    PS_GIFTS                     = "gifts"
    PS_DEUS_VAULT                = "deusVault"
    PS_LAST_UPGRADES             = "lastUpgrades"
    PS_MESSAGE                   = "message"
    PS_NEIGHBOR_ASSISTS          = "neighborAssists"
    PS_QUALITY                   = "quality"
    PS_XMAS_PRESENT_RECEIVED     = "xmasPresentReceived"
    PS_DEUS_CARDS_LAST_GENERATED = "deusCardsLastGenerated"
    PS_CASINO_SPINS              = "casinoSpins"
    PS_CASINO_SPIN_COUNTER       = "casinoSpinCounter"
    PS_CASINO_PRIZE_COUNTER      = "casinoPrizeCounter"
    PS_KOMPU_SPELLS              = "kompuSpells"
    PS_KOMPU_LAST_TIMESTAMP      = "kompuLastTimeStamp"
    PS_KOMPU_STEPS               = "kompuSteps"
    PS_KOMPU_COMPLETED           = "kompuCompleted"
    PS_KOMPU_PLAY                = "kompuPlay"
    PS_SHOWED_NEWS_TIMESTAMP     = "showedNewsTimestamp"
    PS_COLLECT_GAME              = "collectGame"
    PS_TIMESTAMP_LAST_BONUS      = "timestampLastBonus"
    PS_COMPLETED_COLLECTION      = "completedCollection"

    MAX_DRAGON_LEVEL = 40
    XP_PER_LEVEL     = 4

    FOOD_COSTS = [
        0, 5, 10, 20, 40, 80, 160, 320, 640, 1280,
        1664, 2163, 2812, 3656, 4753, 6178, 8032, 10441,
        13574, 17646, 22940, 29822, 38768, 50398, 65518,
        85173, 110725, 143943, 187126, 243264, 316243,
        347867, 382654, 420919, 463011, 509312, 560243,
        616267, 677894, 745683, 820251
    ]

    DRAGONARIUM_COSTS       = [2, 2, 3, 4, 5]
    DRAGONARIUM_START_SLOTS = [2, 2, 2, 1, 1]

    DRAGONS = {
        1000:  "Nature Dragon", 1001:  "Firebird Dragon", 1002:  "Mercury Dragon",
        1003:  "Gummy Dragon", 1004:  "Lantern Fish Dragon", 1005:  "Tropical Dragon",
        1006:  "Zombie Dragon", 1007:  "Petroleum Dragon", 1008:  "Dandelion Dragon",
        1009:  "Jade Dragon", 1010:  "Star Dragon", 1011:  "Terra Dragon",
        1012:  "Flaming rock Dragon", 1013:  "Armadillo Dragon", 1014:  "Cloud Dragon",
        1015:  "Laser Dragon", 1016:  "Mud Dragon", 1017:  "Nenufar Dragon",
        1018:  "Hedgehog Dragon", 1019:  "Icecube Dragon", 1020:  "Flame Dragon",
        1021:  "Neon Dragon", 1022:  "Pearl Dragon", 1023:  "Cool Fire Dragon",
        1024:  "Medieval Dragon", 1025:  "Penguin Dragon", 1026:  "Ice Dragon",
        1028:  "Carnivore Plant Dragon", 1029:  "Fluorescent Dragon", 1031:  "Electric Dragon",
        1032:  "Battery Dragon", 1033:  "Sea Dragon", 1039:  "Metal Dragon",
        1040:  "Dark Dragon", 1041:  "Legendary Dragon", 1042:  "Vampire Dragon",
        1043:  "Alpine Dragon", 1044:  "Poo Dragon", 1045:  "Volcano Dragon",
        1046:  "Blizzard Dragon", 1047:  "Rattlesnake Dragon", 1048:  "Gold Dragon",
        1049:  "Soccer Dragon", 1050:  "Platinum Dragon", 1051:  "Pirate Dragon",
        1052:  "Crystal Dragon", 1053:  "Wind Dragon", 1054:  "Mirror Dragon",
        1055:  "Coral Dragon", 1056:  "Spicy Dragon", 1057:  "Waterfall Dragon",
        1058:  "Cactus Dragon", 1059:  "Storm Dragon", 1060:  "Ice Cream Dragon",
        1061:  "Mojito Dragon", 1062:  "Chameleon Dragon", 1063:  "Hot Metal Dragon",
        1064:  "Snowflake Dragon", 1065:  "Seashell Dragon", 1066:  "Moose Dragon",
        1067:  "Dragonfly Dragon", 1068:  "Venom Dragon", 1069:  "Steampunk Dragon",
        1070:  "Dark Fire Dragon", 1071:  "Butterfly Dragon", 1072:  "Robot Dragon",
        1073:  "Pure Terra Dragon", 1074:  "Pure Flame Dragon", 1075:  "Pure Sea Dragon",
        1076:  "Pure Nature Dragon", 1077:  "Pure Electric Dragon", 1078:  "Pure Ice Dragon",
        1079:  "Pure Metal Dragon", 1080:  "Pure Dark Dragon", 1081:  "Pure Dragon",
        1082:  "Paladin Dragon", 1083:  "Fossil Dragon", 1084:  "Seahorse Dragon",
        1085:  "Sky Dragon", 1086:  "Bat Dragon", 1087:  "Aztec Dragon",
        1088:  "Chinese Dragon", 1089:  "King Dragon", 1090:  "Wizard Dragon",
        1091:  "Two headed Dragon", 1092:  "Plankton Dragon", 1093:  "Uncle Sam Dragon",
        1094:  "Evil Pumpkin Dragon", 1095:  "Viking Dragon", 1096:  "Jelly Dragon",
        1097:  "Quetzal Dragon", 1098:  "Queen Dragon", 1099:  "Thanksgiving Dragon",
        1100:  "Santa Dragon", 1101:  "Ghost Dragon", 1102:  "Deep Forest Dragon",
        1103:  "Ninja Dragon", 1104:  "Ice&Fire Dragon", 1105:  "Aurora Dragon",
        1106:  "Music Dragon", 1107:  "Block Dragon", 1108:  "Butterfly Dragon (2)",
        1109:  "Alien Dragon", 1110:  "Great White Dragon", 1111:  "Pharaoh Dragon",
        1112:  "Paradise Dragon", 1113:  "Gaudi Dragon", 1114:  "Cool Fire Dragon (2)",
        1115:  "Octopus Dragon", 1116:  "Jellyfish Dragon", 1117:  "Carnival Dragon",
        1118:  "Love Dragon", 1119:  "Dujur Dragon", 1120:  "T-Rex Dragon",
        1121:  "Brontosaurus Dragon", 1122:  "Hydra Dragon", 1123:  "Mars Dragon",
        1124:  "Prisma Dragon", 1125:  "Centipede Dragon", 1126:  "Emerald Dragon",
        1127:  "St Patrick's Dragon", 1128:  "Ruby Dragon", 1129:  "Angry Dragon",
        1130:  "Lava Dragon", 1131:  "Joker Dragon", 1132:  "Chainmail Dragon",
        1133:  "Sphynx Dragon", 1134:  "Mummy Dragon", 1135:  "Diamond Dragon",
        1136:  "Demon Dragon", 1137:  "Gargoyle Dragon", 1138:  "Deep Red Dragon",
        1139:  "Blue Dragon", 1140:  "Archangel Dragon", 1141:  "Lightning Dragon",
        1142:  "Ancient Dragon", 1143:  "Wurm Dragon", 1144:  "Light Dragon Test",
        1145:  "War Dragon Test", 1146:  "Eternal Dragon Test", 1147:  "Glacial Dragon",
        1148:  "Cerberus Dragon", 1149:  "Burning Dragon", 1150:  "Treasure Dragon",
        1151:  "Granite Dragon", 1152:  "Bone Dragon", 1153:  "Wyvern Dragon",
        1154:  "Predator Dragon", 1155:  "Poseidon Dragon", 1156:  "Hades Dragon",
        1157:  "Atlas Dragon", 1158:  "Justice Dragon", 1159:  "Sun Dragon",
        1160:  "Gaia Dragon", 1161:  "Luminsicent Dragon", 1162:  "Rainbow Dragon",
        1163:  "War Dragon", 1164:  "Juggernaut Dragon", 1165:  "Colossal Dragon",
        1166:  "Red Woods Dragon", 1167:  "Leviathan Dragon", 1168:  "Panzer Dragon",
        1169:  "Nirobi", 1170:  "Droconos", 1171:  "Monstruous Dragon",
        1172:  "Ivory Dragon", 1173:  "Moon Dragon", 1174:  "Toxic Dragon",
        1175:  "Obsidian Dragon", 1176:  "Meteor Dragon", 1177:  "Hammer Dragon",
        1178:  "Tribal Dragon", 1179:  "Origami Dragon", 1180:  "Tiny Dragon",
        1181:  "Nightwind Dragon", 1182:  "Thor Dragon", 1183:  "Loki Dragon",
        1184:  "Odin Dragon", 1185:  "Fallen Angel Dragon", 1186:  "Cold Star Dragon",
        1187:  "Photon Dragon", 1188:  "Elfic Dragon", 1190:  "Tesla Dragon",
        1192:  "Nirobi (2)", 1193:  "Dark Stone Dragon", 1194:  "White Knight Dragon",
        1195:  "Black Knight Dragon", 1196:  "Thief Dragon", 1197:  "Deus Pet Dragon",
        1198:  "Midas Dragon", 1199:  "Kryptonite Dragon", 1201:  "Blue Fire Dragon",
        1202:  "Hypno Dragon", 1207:  "Rockfeller Dragon", 1208:  "King Solomon Dragon",
        1209:  "Scrooge Dragon", 1210:  "Robin Hood Dragon", 1211:  "Wrestler Dragon",
        1212:  "Clover Dragon", 1214:  "Poker Dragon", 1221:  "Master Dragon",
        1223:  "Chimera Dragon", 1224:  "Eclipse Dragon", 1225:  "Specter Dragon",
        1226:  "Cat Dragon", 1227:  "Crossfire Dragon", 1229:  "Frozen Wind Dragon",
        1231:  "Aztec Warrior Dragon", 1232:  "Aztec Priest Dragon", 1233:  "Aztec Emperor Dragon",
        1260:  "Chobby Dragon", 1263:  "Blind Dragon", 1264:  "Cookie Dragon",
        1265:  "Elements Dragon", 1267:  "Giant Wings Dragon", 1268:  "Amethyst Dragon",
        1269:  "Peace Dragon", 1271:  "Heart Dragon", 1273:  "Twister Dragon",
        1274:  "Sylvan Dragon", 1282:  "Cosmo Dragon", 1283:  "Columbus Dragon",
        1284:  "Bavarian Dragon", 1286:  "Frankie Dragon", 1287:  "Halloween Dragon",
        1288:  "Animation Dragon", 1291:  "Oni Dragon", 1292:  "Hearts Queen Dragon",
        1293:  "Big Hat Dragon", 1294:  "Quartz Dragon", 1295:  "Dark Elf Dragon",
        1297:  "Snow Man Dragon", 1298:  "Xmas Elf Dragon", 1300:  "Middle Earth Dragon",
        1301:  "Shogun Dragon", 1302:  "Martial Arts Dragon",
    }

    HABITATS = {
        24:  "Nature Habitat", 25:  "Big Nature Habitat", 26:  "Terra Habitat",
        27:  "Big Terra Habitat", 28:  "Flame Habitat", 29:  "Big Flame Habitat",
        30:  "Sea Habitat", 31:  "Big Sea Habitat", 32:  "Ice Habitat",
        33:  "Big Ice Habitat", 34:  "Electric Habitat", 35:  "Big Electric Habitat",
        36:  "Metal Habitat", 37:  "Big Metal Habitat", 38:  "Dark Habitat",
        39:  "Big Dark Habitat", 40:  "Legend Habitat", 90:  "Kindergarten",
        110: "Pure Habitat", 111: "Pure Habitat", 112: "Pure Habitat",
        113: "Pure Habitat", 114: "Pure Habitat", 115: "Pure Habitat",
        116: "Pure Habitat", 117: "Pure Habitat", 118: "Pure Habitat",
        125: "Santa Habitat", 130: "Dragonarium", 134: "Egyptian Habitat",
        139: "Dungeon Habitat", 140: "Light Habitat", 141: "Big Light Habitat",
        142: "War Habitat", 143: "Big War Habitat", 144: "Ancient Habitat",
        145: "Big Ancient Habitat", 150: "Olympus Habitat", 153: "Big Pure Habitat",
        159: "Viking Habitat", 164: "Aztec Habitat", 172: "Dojo Habitat",
    }

    HABITAT_IDS = {
        "TERRA":      26,  "TERRA_BIG":   27, "FLAME":      28,  "FLAME_BIG":   29,
        "SEA":        30,  "SEA_BIG":     31, "NATURE":     24,  "NATURE_BIG":  25,
        "ELECTRIC":   34,  "ELECTRIC_BIG":35, "ICE":        32,  "ICE_BIG":     33,
        "METAL":      36,  "METAL_BIG":   37, "DARK":       38,  "DARK_BIG":    39,
        "LIGHT":      140, "LIGHT_BIG":   141, "WAR":        142, "WAR_BIG":     143,
        "LEGEND":     40,  "PURE":        110, "PURE_BIG":   153, "SANTA":      125,
        "EGYPTIAN":   134, "DUNGEON":     139, "OLYMPUS":    150, "VIKING":     159,
        "AZTEC":      164, "DOJO":        172,
    }

    HATCHERY             = 1
    BREEDING_MOUNTAIN    = 19
    ULTRA_BREEDING_TREE  = 80
    STADIUM              = 20
    DRAGON_MARKET        = 79
    RECRUITMENT_TAVERN   = 81
    TRAINING_CENTER      = 22
    DEUS_VAULT           = 128
    DRAGONARIUM          = 130
    KINDERGARTEN         = 90
    DEUS_BREEDING_NEST   = 160
    DEUS_BREEDING_NEST_P = 162

    TEMPLE_MAGIC    = 9
    TEMPLE_NOBLE    = 10
    TEMPLE_KNIGHT   = 11
    TEMPLE_MASTER   = 12
    TEMPLE_EPIC     = 166
    TEMPLE_WONDERS  = 167

    CRYSTAL_NATURE   = 2
    CRYSTAL_TERRA    = 3
    CRYSTAL_FLAME    = 4
    CRYSTAL_ICE      = 5
    CRYSTAL_ELECTRIC = 6
    CRYSTAL_SEA      = 7
    CRYSTAL_DARK     = 8
    CRYSTAL_LEGEND   = 14
    CRYSTAL_METAL    = 15

    FARM       = 16
    FARM_BIG   = 17
    FARM_HUGE  = 18

    OBSTACLE_ROCK        = 45
    OBSTACLE_ROCK_MED    = 46
    OBSTACLE_ROCK_BIG    = 47
    OBSTACLE_BUSH        = 48
    OBSTACLE_TREE_MED    = 49
    OBSTACLE_TREE_BIG    = 50
    OBSTACLE_ROCK_HUGE   = 76
    OBSTACLE_ROCK_GIANT  = 77

    HATCHERY_2 = 55
    HATCHERY_3 = 56
    HATCHERY_4 = 57

    DEUS_STATUE          = 21
    TERRAIN              = 54
    ELF_HOME             = 58
    FOUNTAIN             = 59
    MAGIC_MUSHROOM       = 60
    GLOWY_FLOWER         = 61
    CATEYE_FLOWER        = 62
    BLUE_SNAIL_PLANT     = 63
    PURPLE_SNAIL_PLANT   = 64
    CHINESE_ARCH         = 65
    LITTLE_DRAGON_STATUE = 66
    DRAGON_STATUE        = 67
    OLD_POND             = 68
    WILLOW_TREE          = 69
    STONE_TILE           = 72
    FANCY_TILE           = 73
    LUXURY_TILE          = 74
    SUPER_TILE           = 75
    YING_YANG_FLAG       = 82
    DRAGONHEAD_FLAG      = 83
    DRAGON_FLAG          = 84
    CLOUD_FLAG           = 85
    EGG_FLAG             = 86
    TOWER_FLAG           = 87
    DRAGON_HEDGE         = 88
    LUXURY_EGG_STATUE    = 89
    DRAGON_CLUB_STATUE   = 119
    BREEDING_BOOST       = 120

    UNCLE_SAM_ISLAND     = 121
    XMAS_ISLAND          = 122
    TREASURE_HUNT_ISLAND = 126
    PIRATE_ISLAND        = 127
    DINOSAUR_ISLAND      = 129
    ALIEN_ISLAND         = 131
    CROSS_DCI            = 132
    DINOSAUR_ISLAND_2    = 133
    EGYPTIAN_ISLAND      = 135
    CENTRAL_ISLAND_IPH2  = 136
    DUNGEON_BASE         = 138
    DUNGEON_ISLAND       = 146
    OLYMPUS_ISLAND       = 148
    MONSTER_LEGENDS      = 151
    DCA_ISLAND           = 152
    VIKING_ISLAND        = 158
    CASTLE_ISLAND        = 161
    AZTEC_ISLAND         = 163
    EGYPTIAN_ISLAND_2    = 165
    HALLOWEEN_ISLAND     = 168
    WONDERLAND_ISLAND    = 169
    CHRISTMAS_ISLAND     = 170
    DOJO_ISLAND          = 171

    LOST_SNAIL_WIZARD = 101
    LOST_BABY_ELF     = 102
    LOST_BABY_UNICORN = 103
    LOST_GOLD_TREE    = 104
    CROSS_SE          = 105
    CROSS_SW          = 106
    ANKH              = 137
    DUNGEON_KEY       = 147
    GREEK_VASE        = 149

    MISTERY_EGG_SMALL  = 154
    MISTERY_EGG_MEDIUM = 155
    MISTERY_EGG_LARGE  = 156
    MISTERY_EGG_SUPER  = 157

    ZEPPELIN          = 2000
    POPUP_ST_PATRICK  = 5000
    POPUP_APRIL_FOOLS = 5001
    POPUP_MOON_DRAGON = 5002

    ATTACKS = {
        1:  {"name": "Punch",              "type": "PHYSICAL","element": "ph","damage": 100},
        2:  {"name": "Flying kick",        "type": "PHYSICAL","element": "ph","damage": 150},
        3:  {"name": "Hard charge",        "type": "PHYSICAL","element": "ph","damage": 200},
        4:  {"name": "Stunning hit",       "type": "PHYSICAL","element": "ph","damage": 250},
        5:  {"name": "Head butt",          "type": "PHYSICAL","element": "ph","damage": 300},
        6:  {"name": "Judo Kick",          "type": "PHYSICAL","element": "ph","damage": 350},
        7:  {"name": "Lava balls",         "type": "FIRE",    "element": "f", "damage": 150},
        8:  {"name": "Flaming Arrows",     "type": "FIRE",    "element": "f", "damage": 200},
        9:  {"name": "Nuclear hit",        "type": "FIRE",    "element": "f", "damage": 300},
        10: {"name": "Stitching roots",    "type": "PLANT",   "element": "p", "damage": 150},
        11: {"name": "Poison Ivy",         "type": "PLANT",   "element": "p", "damage": 200},
        12: {"name": "Leaf blast",         "type": "PLANT",   "element": "p", "damage": 300},
        13: {"name": "Earthquake",         "type": "EARTH",   "element": "e", "damage": 150},
        14: {"name": "Meteor shower",      "type": "EARTH",   "element": "e", "damage": 200},
        15: {"name": "Tumble weed",        "type": "EARTH",   "element": "e", "damage": 300},
        16: {"name": "Tsunami",            "type": "WATER",   "element": "w", "damage": 150},
        17: {"name": "Flooding",           "type": "WATER",   "element": "w", "damage": 200},
        18: {"name": "Storm",              "type": "WATER",   "element": "w", "damage": 300},
        19: {"name": "Frost nova",         "type": "ICE",     "element": "i", "damage": 150},
        20: {"name": "Ice spikes",         "type": "ICE",     "element": "i", "damage": 200},
        21: {"name": "Snow storm",         "type": "ICE",     "element": "i", "damage": 300},
        22: {"name": "Lightning",          "type": "ELECTRIC","element": "el","damage": 150},
        23: {"name": "Laser beam",         "type": "ELECTRIC","element": "el","damage": 200},
        24: {"name": "Electric shock",     "type": "ELECTRIC","element": "el","damage": 300},
        25: {"name": "Life drain",         "type": "DARK",    "element": "d", "damage": 150},
        26: {"name": "Leech",              "type": "DARK",    "element": "d", "damage": 200},
        27: {"name": "Ghost cloud",        "type": "DARK",    "element": "d", "damage": 300},
        28: {"name": "Nail rain",          "type": "METAL",   "element": "m", "damage": 150},
        29: {"name": "Magneto",            "type": "METAL",   "element": "m", "damage": 200},
        30: {"name": "Rust",               "type": "METAL",   "element": "m", "damage": 300},
        31: {"name": "Legendary wind",     "type": "LEGEND",  "element": "l", "damage": 150},
        32: {"name": "Paralyzing spell",   "type": "LEGEND",  "element": "l", "damage": 200},
        33: {"name": "Rainbow",            "type": "LEGEND",  "element": "l", "damage": 300},
        34: {"name": "Hammer fist",        "type": "PHYSICAL","element": "ph","damage": 500},
        35: {"name": "Karate Brick Break", "type": "PHYSICAL","element": "ph","damage": 600},
        36: {"name": "Deus sword",         "type": "PHYSICAL","element": "ph","damage": 700},
        37: {"name": "Flamethrower",       "type": "FIRE",    "element": "f", "damage": 500},
        38: {"name": "Magma storm",        "type": "FIRE",    "element": "f", "damage": 600},
        39: {"name": "Rottening spell",    "type": "PLANT",   "element": "p", "damage": 500},
        40: {"name": "Bee hive",           "type": "PLANT",   "element": "p", "damage": 600},
        41: {"name": "Asteroid",           "type": "EARTH",   "element": "e", "damage": 500},
        42: {"name": "Sand storm",         "type": "EARTH",   "element": "e", "damage": 600},
        43: {"name": "Acid Rain",          "type": "WATER",   "element": "w", "damage": 500},
        44: {"name": "Whirlpool",          "type": "WATER",   "element": "w", "damage": 600},
        45: {"name": "Icy wind",           "type": "ICE",     "element": "i", "damage": 500},
        46: {"name": "Cryogenic freeze",   "type": "ICE",     "element": "i", "damage": 600},
        47: {"name": "Electro Ball",       "type": "ELECTRIC","element": "el","damage": 500},
        48: {"name": "Tesla Ray",          "type": "ELECTRIC","element": "el","damage": 600},
        49: {"name": "The Grim Reaper",    "type": "DARK",    "element": "d", "damage": 500},
        50: {"name": "Black hole",         "type": "DARK",    "element": "d", "damage": 600},
        51: {"name": "Cannon Balls",       "type": "METAL",   "element": "m", "damage": 500},
        52: {"name": "Ninja stars",        "type": "METAL",   "element": "m", "damage": 600},
        53: {"name": "Aurora Borealis",    "type": "LEGEND",  "element": "l", "damage": 800},
        54: {"name": "Legend spell",       "type": "LEGEND",  "element": "l", "damage": 900},
        55: {"name": "Hypnosis",           "type": "PURE",    "element": "pu","damage": 700},
        56: {"name": "Pure energy",        "type": "PURE",    "element": "pu","damage": 700},
        57: {"name": "Pure light",         "type": "PURE",    "element": "pu","damage": 700},
        58: {"name": "Light Sword",        "type": "LIGHT",   "element": "li","damage": 200},
        59: {"name": "Light Prism",        "type": "LIGHT",   "element": "li","damage": 250},
        60: {"name": "Light Star",         "type": "LIGHT",   "element": "li","damage": 300},
        61: {"name": "Giant Crack",        "type": "WAR",     "element": "wr","damage": 250},
        62: {"name": "Giant Mouth",        "type": "WAR",     "element": "wr","damage": 300},
        63: {"name": "Giant Claw",         "type": "WAR",     "element": "wr","damage": 350},
        64: {"name": "Enlightning Wisdom", "type": "LIGHT",   "element": "li","damage": 500},
        65: {"name": "Out of Time",        "type": "LIGHT",   "element": "li","damage": 600},
        66: {"name": "Astro Hit",          "type": "WAR",     "element": "wr","damage": 650},
        67: {"name": "War Fist",           "type": "WAR",     "element": "wr","damage": 700},
    }

    ATTACK_TRAINING_TIME = {
        1: 43200, 2: 43200, 3: 43200, 4: 43200, 5: 43200, 6: 43200,
        7: 43200, 8: 43200, 9: 43200, 10: 43200, 11: 43200, 12: 43200,
        13: 43200, 14: 43200, 15: 43200, 16: 43200, 17: 43200, 18: 43200,
        19: 43200, 20: 43200, 21: 43200, 22: 43200, 23: 43200, 24: 43200,
        25: 43200, 26: 43200, 27: 43200, 28: 43200, 29: 43200, 30: 43200,
        31: 43200, 32: 43200, 33: 43200,
        34: 86400, 35: 86400, 37: 86400, 39: 86400, 41: 86400, 43: 86400,
        45: 86400, 47: 86400, 49: 86400, 51: 86400, 53: 86400, 55: 86400,
        36: 172800, 38: 172800, 40: 172800, 42: 172800, 44: 172800,
        46: 172800, 48: 172800, 50: 172800, 52: 172800, 54: 172800,
        56: 172800, 57: 172800, 58: 172800, 59: 172800, 60: 172800,
        61: 172800, 62: 172800, 63: 172800, 64: 172800, 65: 172800,
        66: 172800, 67: 172800,
    }

    MAX_LEVEL                = 99
    MAX_DRAGON_POPULATION    = [0, 20]
    MAX_POPULATION_CAP       = 175
    MAX_POPULATION_PER_LEVEL = 3
    START_MAX_POPULATION     = 20
    MAX_DRAGON_CAP_STEP      = 10

    NORMAL_BREED_COST     = 0
    RARITY_BOOST_COST     = 5
    RARITY_BOOST_LEVEL    = 6

    COLLECT_MINUTES = [0.5, 5, 30, 120, 360, 720, 1440, 2160, 2880]
    COLLECT_VALUES  = [5, 25, 75, 200, 500, 1500, 5000, 10000, 50000]
    COLLECT_XP      = [25, 250, 1000, 5000, 15000, 75000, 250000, 500000, 2500000]
    COLLECT_PRICE   = [{"g":50},{"g":250},{"g":1000},{"g":5000},{"g":15000},
                       {"g":75000},{"g":500000},{"g":1000000},{"g":5000000}]
    COLLECT_HELP_SECONDS = 3600

    ISLANDS_COSTS          = [{"g":0},{"g":100000},{"c":25},{"c":100},{"c":250},{"c":400}]
    MIN_LEVEL_ISLAND_PUBE  = 20

    PVP_REWARD             = {"c": 2}
    MAX_GOLD_STOLEN        = 20000
    GOLD_STOLEN_BOTTOM_PCT = 15
    GOLD_STOLEN_TOP_PCT    = 35
    SPYINGS_MAX            = 3
    SPYINGS_PERIOD_HOURS   = 24

    TOURNAMENT_COOLDOWN       = 12
    TOURNAMENT_SPEED_UP_PRICE = 2

    DRAGON_CARDS_TRY       = 3
    DRAGON_CARDS_SUPER_TRY = 10

    KOMPU_MIN_LEVEL        = 5
    KOMPU_BOX_OPEN_PRICE   = 20
    KOMPU_BOX_CHANGE_PRICE = 3

    DAILY_BONUS = [{"f":250},{"g":1500},{"f":1000},{"g":3000},{"f":2000}]
    MONDAY_BONUS_REWARDS         = [{"type":"g","value":2500},{"type":"u","value":None},{"type":"c","value":5}]
    MONDAY_BONUS_REWARDS_DRAGONS = [1000,1011,1020,1026,1031,1033,1039]

    LEVELS_XP_REQUIRED = [
        0, 200, 500, 1400, 2900, 4900, 9900, 19900, 34900, 59900,
        94900, 144900, 244900, 394900, 694900, 1194900, 1944900,
        2944900, 4194900, 5694900, 7444900, 9444900, 11944900,
        14944900, 18444900, 22444900, 26944900, 31944900, 37444900,
        43444900, 49944900, 56944900, 64444900, 72444900, 80944900,
        89944900, 99444900, 109444900, 119944900, 130944900,
        142444900, 154444900, 166944900, 179944900, 193444900,
        207444900, 221944900, 236944900, 252444900, 268444900,
        287444900, 309444900, 334444900, 362444900, 393444900,
        427444900, 464444900, 504444900, 547444900, 593444900,
        642444900, 694444900, 749444900, 807444900, 868444900,
        932444900, 999444900, 1069444900, 1142444900, 1218444900,
        1297444900, 1379444900, 1464444900, 1552444900, 1643444900,
        1737444900, 1834444900, 1934444900, 2037444900, 2143444900,
        2252444900, 2364444900, 2479444900, 2597444900, 2718444900,
        2842444900, 2969444900, 3099444900, 3232444900, 3368444900,
        3507444900, 3649444900, 3794444900, 3942444900, 4093444900,
        4247444900, 4404444900, 4564444900, 4727444900,
    ]

    TREASURE_ITEMS = {
        1: {"name":"Some Gold",             "amount":75000,  "price":15,  "type":"g"},
        2: {"name":"Quite a lot of Gold",   "amount":200000, "price":30,  "type":"g"},
        3: {"name":"A lot of Gold",         "amount":500000, "price":80,  "type":"g"},
        4: {"name":"Large amount of Gold",  "amount":1250000,"price":150, "type":"g"},
        5: {"name":"Nibble",                "amount":10000,  "price":15,  "type":"f"},
        6: {"name":"Meal",                  "amount":22500,  "price":30,  "type":"f"},
        7: {"name":"Menu",                  "amount":70000,  "price":80,  "type":"f"},
        8: {"name":"Catering",              "amount":140000, "price":150, "type":"f"},
        9: {"name":"Banquet",               "amount":200000, "price":200, "type":"f"},
    }

    TREASURE_ITEMS_LEGACY = {
        1: {"type":"gold", "amount":75000,  "price":15},
        2: {"type":"gold", "amount":200000, "price":30},
        3: {"type":"gold", "amount":500000, "price":80},
        5: {"type":"food", "amount":10000,  "price":15},
        6: {"type":"food", "amount":22500,  "price":30},
        7: {"type":"food", "amount":70000,  "price":80},
    }

    TREASURE_GOLD_1 = 1
    TREASURE_GOLD_2 = 2
    TREASURE_GOLD_3 = 3
    TREASURE_GOLD_4 = 4
    TREASURE_FOOD_1 = 5
    TREASURE_FOOD_2 = 6
    TREASURE_FOOD_3 = 7
    TREASURE_FOOD_4 = 8
    TREASURE_BANQUET= 9

    MISTERY_EGG_REWARDS = {
        "SMALL": {
            "rewards":  [1020, 1045, 1016, 1005, 1000, 1033, {"g":1000}, {"f":80}],
            "chances":  [8, 8, 8, 8, 8, 8, 25, 25]
        },
        "MEDIUM": {
            "rewards":  [1031, 1019, 1015, 1059, 1016, 1033, {"g":3000}, {"f":200}],
            "chances":  [8, 8, 8, 8, 8, 8, 25, 25]
        },
        "LARGE": {
            "rewards":  [1026, 1048, 1004, 1066, 1031, 1039, {"g":4700}, {"f":300}],
            "chances":  [8, 8, 8, 8, 8, 8, 25, 25]
        },
        "SUPER": {
            "rewards":  [1039, 1040, 1050, 1067, 1021, 1006, {"g":10000}, {"f":600}],
            "chances":  [8, 8, 8, 8, 8, 8, 25, 25]
        },
    }

    DEUS_VAULT_RECIPES = [
        {"id":0,  "result":1119, "components":[1023,1031], "costs":{"c":1500},   "probability":100},
        {"id":1,  "result":1098, "components":[1024,1017], "costs":{"g":2500000},"probability":70},
        {"id":2,  "result":1095, "components":[1023,1019], "costs":{"c":300},    "probability":100},
        {"id":3,  "result":1092, "components":[1055,1058], "costs":{"c":200},    "probability":100},
        {"id":4,  "result":1087, "components":[1005,1056], "costs":{"c":350},    "probability":100},
        {"id":5,  "result":1083, "components":[1040,1026], "costs":{"g":5000000},"probability":70},
        {"id":6,  "result":1086, "components":[1068,1013], "costs":{"c":125},    "probability":100},
        {"id":7,  "result":1084, "components":[1004,1008], "costs":{"c":50},     "probability":100},
        {"id":8,  "result":1089, "components":[1024,1063], "costs":{"c":450},    "probability":100},
        {"id":9,  "result":1085, "components":[1015,1046], "costs":{"c":250},    "probability":100},
        {"id":10, "result":1096, "components":[1057,1045], "costs":{"c":150},    "probability":100},
        {"id":11, "result":1097, "components":[1058,1056], "costs":{"c":175},    "probability":100},
        {"id":12, "result":1099, "components":[1007,1020], "costs":{"c":125},    "probability":100},
        {"id":13, "result":1103, "components":[1009,1002], "costs":{"c":100},    "probability":100},
        {"id":14, "result":1110, "components":[1032,1026], "costs":{"c":70},     "probability":100},
        {"id":15, "result":1091, "components":[1005,1040], "costs":{"c":90},     "probability":100},
    ]

    COLLECTIONS = {
        1:  {"name":"The Elemental collection",     "dragons":[1011,1020,1033,1000,1031], "reward":{"c":2}},
        2:  {"name":"The Monstrous collection",     "dragons":[1016,1044,1005,1018,1028], "reward":{"c":3}},
        3:  {"name":"The Red Hot collection",       "dragons":[1001,1012,1045,1056,1024], "reward":{"c":2}},
        4:  {"name":"The Scary collection",         "dragons":[1040,1042,1051,1006,1047], "reward":{"c":3}},
        5:  {"name":"The Blue Planet collection",   "dragons":[1017,1057,1055,1025,1004], "reward":{"c":2}},
        6:  {"name":"The Heavy Metal collection",   "dragons":[1039,1048,1002,1050,1013], "reward":{"c":4}},
        7:  {"name":"The Frosty collection",        "dragons":[1026,1046,1019,1043,1023], "reward":{"c":2}},
        8:  {"name":"The Legendary collection",     "dragons":[1041,1053,1054,1052],       "reward":{"c":5}},
        9:  {"name":"The Bizarre collection",       "dragons":[1003,1049,1007,1022,1009], "reward":{"c":3}},
        10: {"name":"The Heaven & Earth collection","dragons":[1058,1014,1010,1059,1008], "reward":{"c":2}},
        11: {"name":"The Sparky collection",        "dragons":[1015,1032,1029,1021],       "reward":{"c":4}},
        12: {"name":"The Hot&Cold collection",      "dragons":[1070,1064,1063,1060,1061], "reward":{"c":3}},
        13: {"name":"The First Pure collection",    "dragons":[1081,1073,1074,1075,1076], "reward":{"c":5}},
        14: {"name":"The Second Pure collection",   "dragons":[1077,1078,1079,1080],       "reward":{"c":4}},
        15: {"name":"The Tough collection",         "dragons":[1062,1065,1066,1067,1068], "reward":{"c":3}},
        16: {"name":"The Festive collection",       "dragons":[1112,1117,1180,1069,1095], "reward":{"c":4}},
        17: {"name":"The Gaia collection",          "dragons":[1084,1092,1105,1102,1177], "reward":{"c":5}},
        18: {"name":"The Sky Masters collection",   "dragons":[1071,1085,1086,1083,1130], "reward":{"c":7}},
        19: {"name":"The Multiheaded collection",   "dragons":[1091,1104,1122],            "reward":{"c":5}},
        20: {"name":"The Elder collection",         "dragons":[1124,1125,1110,1087],       "reward":{"c":4}},
        21: {"name":"The Happy collection",         "dragons":[1129,1096,1106,1107,1131], "reward":{"c":5}},
        22: {"name":"The Luxurious collection",     "dragons":[1126,1128,1135,1150,1172], "reward":{"c":5}},
        23: {"name":"The Basic light collection",   "dragons":[1140,1158,1159,1160,1161], "reward":{"c":3}},
        24: {"name":"The Advanced light collection","dragons":[1162,1185,1186,1187,1188],"reward":{"c":9}},
        25: {"name":"The Basic war collection",     "dragons":[1163,1164,1165,1166,1167], "reward":{"c":3}},
        26: {"name":"The Advanced war collection",  "dragons":[1168,1181,1190,1193],       "reward":{"c":9}},
    }

    TOURNAMENTS = {
        1:  {"name":"Terra Tournament",          "reward":{"c":1,"g":1000}},
        2:  {"name":"Flame Tournament",          "reward":{"c":2,"g":1500}},
        3:  {"name":"Sea Tournament",            "reward":{"c":2,"g":2000}},
        4:  {"name":"Emerald Cup",               "reward":{"c":2,"g":2500}},
        5:  {"name":"Nature Tournament",         "reward":{"c":2,"g":3000}},
        6:  {"name":"Electric Tournament",       "reward":{"c":2,"g":3500}},
        7:  {"name":"Ice Tournament",            "reward":{"c":2,"g":4000}},
        8:  {"name":"Sapphire Cup",              "reward":{"c":2,"g":4500}},
        9:  {"name":"Metal Tournament",          "reward":{"c":2,"g":5000}},
        10: {"name":"Dark Tournament",           "reward":{"c":2,"g":5500}},
        11: {"name":"Legendary Tournament",      "reward":{"c":2,"g":6000}},
        12: {"name":"Diamond Cup",               "reward":{"c":2,"g":6500}},
        13: {"name":"Terra Tournament Lv.2",     "reward":{"c":2,"g":7000}},
        14: {"name":"Flame Tournament Lv.2",     "reward":{"c":2,"g":7500}},
        15: {"name":"Sea Tournament Lv.2",       "reward":{"c":2,"g":8000}},
        16: {"name":"Emerald Cup Lv.2",          "reward":{"c":2,"g":8500}},
        17: {"name":"Nature Tournament Lv.2",    "reward":{"c":2,"g":9000}},
        18: {"name":"Electric Tournament Lv.2",  "reward":{"c":2,"g":9500}},
        19: {"name":"Ice Tournament Lv.2",       "reward":{"c":2,"g":10000}},
        20: {"name":"Sapphire Cup Lv.2",         "reward":{"c":2,"g":10500}},
        21: {"name":"Metal Tournament Lv.2",     "reward":{"c":2,"g":11000}},
        22: {"name":"Dark Tournament Lv.2",      "reward":{"c":2,"g":11500}},
        23: {"name":"Legendary Tournament Lv.2", "reward":{"c":2,"g":12000}},
        24: {"name":"Diamond Cup Lv.2",          "reward":{"c":2,"g":12500}},
    }

    DRAGON_CARD_PRIZES = [
        {"id":0, "reward":{"g":5000},   "weight":1,   "weight_paid":1.5, "weight_super":0},
        {"id":1, "reward":{"f":1000},   "weight":1.3, "weight_paid":2,   "weight_super":0},
        {"id":2, "reward":"retry",      "weight":3,   "weight_paid":4,   "weight_super":0},
        {"id":3, "reward":{"g":40000},  "weight":7,   "weight_paid":4,   "weight_super":2.525},
        {"id":4, "reward":{"g":50000},  "weight":10,  "weight_paid":5,   "weight_super":2.525},
        {"id":5, "reward":{"f":7500},   "weight":15,  "weight_paid":6,   "weight_super":2.525},
        {"id":6, "reward":{"f":20000},  "weight":30,  "weight_paid":9,   "weight_super":3.75},
        {"id":7, "reward":1153,         "weight":40,  "weight_paid":9,   "weight_super":10},
        {"id":8, "reward":{"c":50},     "weight":50,  "weight_paid":20,  "weight_super":10},
    ]

    DRAGONARIUM_SLOT_CATEGORIES = {
        "pu": 4,
        "l":  3,
        "d":  2,
        "m":  1,
        "_":  0,
    }

    HABITAT_GROUP_TYPES = {
        "e": 26, "f": 28, "w": 30, "p": 24, "el": 34,
        "i": 32, "m": 36, "d": 38, "li": 140, "wr": 142,
        "l": 40, "pu": 110,
    }

    ELEMENT_HABITAT_MAP = {
        "e":  [26, 27],
        "f":  [28, 29],
        "w":  [30, 31],
        "p":  [24, 25],
        "el": [34, 35],
        "i":  [32, 33],
        "m":  [36, 37],
        "d":  [38, 39],
        "li": [140, 141],
        "wr": [142, 143],
        "l":  [40],
        "pu": [110, 111, 112, 113, 114, 115, 116, 117, 118, 153],
    }

    HABITAT_CAPACITY = {
        24: 2, 25: 4, 26: 2, 27: 4, 28: 2, 29: 4,
        30: 1, 31: 3, 32: 1, 33: 3, 34: 2, 35: 4,
        36: 2, 37: 4, 38: 2, 39: 4, 40: 1,
        90: 5, 110: 2, 153: 3,
    }

    HABITAT_MAX_GOLD = {
        24: 10000,  25: 40000, 26: 500,    27: 10000,
        28: 5000,   29: 20000, 30: 7500,   31: 30000,
        32: 15000,  33: 60000, 34: 12500,  35: 50000,
        36: 17500,  37: 70000, 38: 20000,  39: 80000,
        40: 350000, 90: 7500,  110: 80000, 153: 240000,
    }

    RACE_HUMAN  = "h"
    RACE_ORC    = "o"
    RACE_ELF    = "e"
    RACE_UNDEAD = "u"
    RACE_DWARF  = "d"

    SELL_REASON_KILL     = "KILL"
    SELL_REASON_CLEAN    = "CLEAN"
    SELL_REASON_BULLDOZE = "BLDZE"
    SELL_REASON_UNKNOWN  = "UNKNOWN"

    DRAGON_XP_PER_LEVEL = 4
    DRAGON_MAX_LEVEL    = 40

    MIN_LEVEL_DRAGON_BOOK           = 10
    MIN_LEVEL_TRAINING              = 15
    MIN_LEVEL_ATTACKS_1             = 10
    MIN_LEVEL_ATTACKS_2             = 15
    MIN_LEVEL_ATTACKS_3             = 20
    MIN_LEVEL_ATTACK_SIEGE_1        = 25
    MIN_LEVEL_ATTACK_SIEGE_2        = 30
    MIN_LEVEL_ATTACK_SIEGE_3        = 35
    MIN_LEVEL_UP_OFFER              = 7
    MIN_LEVEL_TO_SELL_EGG           = 10
    MINIMUM_LEVEL_FOR_BANNER_POPUP  = 5


logger.info("[=] [ENCONTRADO] Categorías cargadas: " + str(len(Constant.CATEGORIES)))
logger.info("[=] [ENCONTRADO] Subcategorías cargadas: " + str(len(Constant.SUBCATEGORIES)))
logger.info("[=] [ENCONTRADO] Dragones registrados: " + str(len(Constant.DRAGONS)))
logger.info("[=] [ENCONTRADO] Hábitats registrados: " + str(len(Constant.HABITATS)))
logger.info("[=] [ENCONTRADO] Ataques registrados: " + str(len(Constant.ATTACKS)))
logger.info("[=] [ENCONTRADO] Colecciones registradas: " + str(len(Constant.COLLECTIONS)))
logger.info("[=] [ENCONTRADO] Torneos registrados: " + str(len(Constant.TOURNAMENTS)))
logger.info("[=] [ENCONTRADO] Recetas de Deus Vault: " + str(len(Constant.DEUS_VAULT_RECIPES)))
logger.info("[<] [FINALIZADO] Repositorio de constantes cargado correctamente.")