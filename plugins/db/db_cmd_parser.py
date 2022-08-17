from model.message import Message
from plugins.db.db_event import *
from plugins.db.plugin_config import *


def assign_find(text: str, assign_op: list):
    for ind in range(len(assign_op)):
        pos = text.find(assign_op[ind])
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


def assign_parse(text: str, assign_op: list):
    ret = list()
    
    assigns = text.split(SPLIT)

    for assign in assigns:

        if assign == "":
            continue

        assign_pos, assign_typ = assign_find(assign, assign_op)

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
        if not str.isalpha(text[0]):
            return None

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

"""
    Parsing database cmd
    return None: parse failed, not a valid database command
"""
def database_cmd_parse(raw: Message):
    if raw.text != None:
        cm_event = one_database_parse(raw.text, INDEX_SYMBOL[0], INDEX_SYMBOL[1])

        if cm_event != None:
            cm_event.quote = raw.quote
            return cm_event

    return None