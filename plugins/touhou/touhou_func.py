from plugins.touhou.plugin_config import *
import json
import random


def get_role(collection: str):
    fp = open(TOUHOU_ROLE_PATH, "r", encoding="utf-8")
    role_table = json.load(fp=fp)
    random.seed()
    if collection == "":
        all_list = list()
        for col in role_table:
            all_list += role_table[col]
        index = random.randint(1, len(all_list))
        for col in role_table:
            if all_list[index-1] in role_table[col]:
                collection = col
                break
        return all_list[index-1], collection

    if collection not in role_table:
        return "", ""

    role_list = role_table[collection]
    index = random.randint(1, len(role_list))
    return role_list[index-1], collection


def list_role(collection: str):
    fp = open(TOUHOU_ROLE_PATH, "r", encoding="utf-8")
    role_table = json.load(fp=fp)

    if collection not in role_table:
        return list()

    return role_table[collection]


def get_sc(role: str):
    fp = open(TOUHOU_SC_PATH, "r", encoding="utf-8")
    sc_table = json.load(fp=fp)
    random.seed()
    if role == "":
        all_list = list()
        for col in sc_table:
            all_list += sc_table[col]
        index = random.randint(1, len(all_list))
        for rol in sc_table:
            if all_list[index - 1] in sc_table[rol]:
                role = rol
                break
        return all_list[index - 1], role

    if role not in sc_table:
            return "", ""

    sc_list = sc_table[role]
    index = random.randint(1, len(sc_list))
    return sc_list[index-1], role


def list_sc(role: str):
    fp = open(TOUHOU_SC_PATH, "r", encoding="utf-8")
    sc_table = json.load(fp=fp)

    if role not in sc_table:
        return ""
    return sc_table[role]