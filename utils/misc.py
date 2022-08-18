"""
    Find all postions of pattern in origin
"""
def find_all(origin: str, patten: str) -> list:
    ret = []
    start_pos = 0
    while True:
        start_pos = origin.find(patten, start_pos)
        if start_pos != -1:
            ret.append(start_pos)
            start_pos += len(patten)
        else:
            break
    return ret
