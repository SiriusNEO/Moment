from model.message import Message

from model.event import *

from db.db_config import *
from event.event_config import *

"""
    data base part
"""

def assign_find(text: str, match_assigns: list):
    for ind in range(len(match_assigns)):
        pos = text.find(match_assigns[ind])
        if pos != -1:
            return pos, ind
    return -1, None

def bracket_parse(text: str, left: str, right: str):
    text = text.strip(' ')

    if text == "":
        return None

    if text[0] == left:
        right_pos = text.find(right)
        if right_pos == -1:
            return None
        return text[1:right_pos].strip(' '), text[right_pos+1:].strip(' ')

    return None

def assign_parse(text: str, match_assigns: list):
    ret = list()
    
    assigns = text.split(SPLIT)

    for assign in assigns:

        if assign == "":
            continue

        assign_pos, assign_typ = assign_find(assign, match_assigns)

        # no assign character
        if assign_pos == -1:
            return None
        
        tag = assign[0:assign_pos].strip(' ')
        value = assign[assign_pos+1:].strip(' ')
        
        # ignore the start
        ret.append([tag, value, assign_typ])
    
    return ret

def index_parse(text: str):
    if text == "":
        return []
    
    if str.isdigit(text):
        return [[TAG_ID, text, 0]]
    
    return None

def modify_word_parse(text: str):
    if text == WORD_DEL:
        return WORD_DEL
    elif text == WORD_CLR:
        return WORD_CLR
    
    return None

# [id] a = b
# ret: id, left_assign, right_assign
def one_database_parse(text: str, left: str, right: str):
    ret = None

    # two parts
    bracket_raw = bracket_parse(text, left, right)

    if bracket_raw == None:
        if text == "":
            return None

        # new
        if left == "[" and not str.isalpha(text[0]):
            return None
        elif left == "<":
            if len(text) < len(REG_CMD) or text[0:len(REG_CMD)] != REG_CMD:
                return None
            else:
                text = text[len(REG_CMD):]
                text = text.strip(' ')
        elif left == "{":
            if len(text) < len(ALIAS_CMD) or text[0:len(ALIAS_CMD)] != ALIAS_CMD:
                return None
            else:
                text = text[len(ALIAS_CMD):]
                text = text.strip(' ')

        assigns = assign_parse(text, MODIFY_ASSIGN)

        if assigns == None:
            return None
        
        ret = NewEvent()

        for assign in assigns:
            ret.modifies.append(TagPair(assign[0], assign[1], assign[2]))
        
        return ret
    
    left_assign = assign_parse(bracket_raw[0], QUERY_ASSIGN)
    left_other = index_parse(bracket_raw[0])

    right_assign = assign_parse(bracket_raw[1], MODIFY_ASSIGN)
    right_word = modify_word_parse(bracket_raw[1])

    # modify
    if (left_other != None or left_assign != None) and (right_assign != None or right_word != None) and bracket_raw[1] != "":
        ret = ModifyEvent()
        word = modify_word_parse(bracket_raw[1])
        
        if word != None:
            ret.word = word
        
        if left_other != None:
            for assign in left_other:
                ret.indices.append(TagPair(assign[0], assign[1], assign[2]))

        if left_assign != None:
            for assign in left_assign:
                ret.indices.append(TagPair(assign[0], assign[1], assign[2]))

        if right_assign != None:
            for assign in right_assign:
                ret.modifies.append(TagPair(assign[0], assign[1], assign[2]))

    # query
    elif left_other != None or left_assign != None:
        ret = QueryEvent()

        if left_other != None:
            for assign in left_other:
                ret.indices.append(TagPair(assign[0], assign[1], assign[2]))

        if left_assign != None:
            for assign in left_assign:
                ret.indices.append(TagPair(assign[0], assign[1], assign[2]))

    # error
    else:
        return None
    
    return ret

def database_cmd_parse(raw: Message):
    if raw.text != None:
        # root command first

        # user command next
        
        cm_event = one_database_parse(raw.text, '[', ']')

        if cm_event != None:
            cm_event.target_db = CM_PATH
            cm_event.quote = raw.quote
            return cm_event

        user_event = one_database_parse(raw.text, '<', '>')

        if user_event != None:
            user_event.target_db = USER_PATH
            user_event.quote = raw.quote
            return user_event

        alias_event = one_database_parse(raw.text, '{', '}')

        if alias_event != None:
            alias_event.target_db = ALIAS
            alias_event.quote = raw.quote
            return alias_event

    return None