import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] [%(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger("version")

version_n = "Demo"
version_c = "v0.0.1"

def migrate_loaded_save(save: dict) -> bool:
    current_version = save.get("version")
    if current_version != version_c:
        save["version"] = version_c
        return True
    return False