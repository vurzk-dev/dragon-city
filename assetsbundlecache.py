import os

from logging_config import logger
from paths import BASE_DIR

class AssetsBundleCache:
    def __init__(self):
        self.file_cache = {}

    def build(self):
        self.file_cache.clear()
        for root, dirs, files in os.walk(BASE_DIR):
            dirs[:] = [d for d in dirs if d not in ('web', 'markut-logs', 'saves', '.git', '__pycache__', 'build', 'villages')]
            for file in files:
                if file.endswith(('.py', '.log', '.txt', '.db', '.sqlite')):
                    continue
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, BASE_DIR).replace('\\', '/')
                self.file_cache[rel_path] = full_path

    def get(self, path):
        normalized = path.replace('\\', '/').lstrip('/')
        return self.file_cache.get(normalized)

asset_cache = AssetsBundleCache()