# Command Part

COMMIT_COMMAND = "momcommit"
BACKUP_COMMAND = "mombackup"
RELOAD_COMMAND = "momreload"
ROLLBACK_COMMAND = "momrollback"

SHOWDB_COMMAND = "showdb"
USEDB_COMMAND = "usedb"

RECORD_COMMAND = "recording"
RECORD_MAX_NUM = 10

SPLIT = " "

INDEX_SYMBOL = ["[", "]"]
MEMBER_SYMBOL = "."

QUERY_ASSIGN = ["=", "?", ">", "<", "@"] 
MODIFY_ASSIGN = ["=", "+", "-"]

WORD_DEL = "del"
WORD_CLR = "clr"

TAG_ID = "id"

INDEX_REGEX = "^\[(\s*)((([a-z]+)(=|\?|<|>|@)\S+|[0-9]+)((\s+)(([a-z]+)(=|\?|<|>|@)\S+))*)?(\s*)\](\.[a-z]+)?"
MODIFY_REGEX = "^(del|clr|([a-z]+)(=|\+|-)(\S+)(\ ([a-z]+)(=|\+|-)(\S+))*)$"

# --- Database ---

# db file structure
# local
#  img/
#  img/index
#  cmdb.json
#  userdb.json

CM_PATH = "local/cmdb.json"
BACKUP_PATH_SUFFIX = "_backup"

QUERY_DISPLAY_THRESHOLD = 10
SEND_THRESHOLD = 3

MAX_INFO_LEN = 10
MAX_LIST_ITEMS = 4

# db table

SHADOW_CODE = "shadow_code"

ID = "id"

THIS = "%this"
ABOVE  = "%above"
NEXT = "%next"
SPLIT_THIS = "%split"

AUTO_SAVE_TIME = [13, 20]