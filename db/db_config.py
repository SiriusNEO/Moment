# db file structure
# local
#  img/
#  img/index
#  cmdb.json
#  userdb.json

IMG_PATH = "local/img/"
CM_PATH = "local/cmdb.json"
USER_PATH = "local/userdb.json"
ALIAS_PATH = "local/aliasdb.json"

QUERY_DISPLAY_THRESHOLD = 10

MODIFY_THRESHOLD = 5

MAX_INFO_LEN = 10

# db table

SHADOW_CODE = "shadow_code"

ID = "id"

THIS = "%this"

ALRAM = "alarm"

COL_T = {
            "id": int,  
            "cm": list,  
            "key": list,  
            "full": list,  
            "time": str,    
            "freq": float,  
            "at_who": str, 
            "qt_who": str,
            "act": int,
            "ps": str,
            "qq": int,  
            "name": str,    
            "prof": list,   
            "priv": int,    
            "coin": int, 
            "alias": str,     
            "cmd": str
        }

CM_COL   = ["id", "cm", "key", "full", "time", "freq", "at_who", "qt_who", "act", "ps"]

USER_COL   = ["id", "qq", "name", "prof", "priv", "coin"]

ALIAS_COL   = ["id", "alias", "cmd"] 