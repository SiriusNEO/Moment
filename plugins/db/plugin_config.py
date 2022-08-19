# Command Part

COMMIT_COMMAND = "momcommit"
BACKUP_COMMAND = "mombackup"

SPLIT = " "

INDEX_SYMBOL = ["[", "]"]

QUERY_ASSIGN = ["=", "?", ">", "<", "@"] 
MODIFY_ASSIGN = ["=", "+", "-"]

WORD_DEL = "del"
WORD_CLR = "clr"

TAG_ID = "id"

# --- Database ---

# db file structure
# local
#  img/
#  img/index
#  cmdb.json
#  userdb.json

CM_PATH = "local/cmdb.json"
BACKUP_PATH = "local/cmdb_backup.json"

QUERY_DISPLAY_THRESHOLD = 10

MAX_INFO_LEN = 10

# db table

SHADOW_CODE = "shadow_code"

ID = "id"

THIS = "%this"