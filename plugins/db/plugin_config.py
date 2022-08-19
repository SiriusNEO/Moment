# Command Part

COMMIT_COMMAND = "momcommit"
BACKUP_COMMAND = "mombackup"

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
BACKUP_PATH = "local/cmdb_backup.json"

QUERY_DISPLAY_THRESHOLD = 10
SEND_THRESHOLD = 3

MAX_INFO_LEN = 10

# db table

SHADOW_CODE = "shadow_code"

ID = "id"

THIS = "%this"