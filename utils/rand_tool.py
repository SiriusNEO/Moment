import random

def random_str(slen = 32):
    random.seed()
    ret = ''
    base = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    base_len = len(base) - 1
    for i in range(slen):
        ret += base[random.randint(0, base_len)]
    return ret