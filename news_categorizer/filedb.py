import json
import os
import threading

db_root = None
_lock = threading.Lock()
locks = {}


def init():
    global db_root
    root_path = os.path.abspath(os.curdir)
    db_root = os.path.join(root_path, "_db")
    os.makedirs(db_root, exist_ok=True)


def get_or_create_lock(key):
    global _lock, locks
    with _lock:
        if key in locks:
            lock = locks[key]
        else:
            lock = locks[key] = threading.Lock()
    return lock


def remove_lock(key):
    global _lock, locks
    with _lock:
        if key in locks:
            del locks[key]


def get_filepath(key):
    global db_root
    return os.path.join(db_root, key + ".json")


def exists(key):
    return os.path.isfile(get_filepath(key))


def find_by_id(key):
    global _lock, locks
    with get_or_create_lock(key):
        with open(get_filepath(key), "rt") as json_file:
            data = json.load(json_file)
    remove_lock(key)
    return data


def save(key, data):
    file_path = get_filepath(key)
    dir_path = os.path.dirname(file_path)
    os.makedirs(dir_path, exist_ok=True)
    global _lock, locks
    with get_or_create_lock(key):
        with open(file_path, "wt") as json_file:
            json.dump(data, json_file, indent=2, ensure_ascii=False)
    remove_lock(key)
