from core.message import Message
from plugins.db.db_event import *
from plugins.db.plugin_config import *

import re

"""
    在字符串中匹配 assign_op
"""
def assign_find(text: str, assign_op: list):
    for ind in range(len(assign_op)):
        pos = text.find(assign_op[ind])
        if pos != -1:
            return pos, ind
    return -1, None

"""
    处理下标括号
    返回括号里的和括号外的内容, 均经过 strip
"""
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

"""
    处理 tag_name assign_op tag_value 这种形式的串
"""
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

"""
    语法糖: [id=1] 相当于 [1]
"""
def index_parse(text: str):
    if text == "":
        return []
    
    if str.isdigit(text):
        return [[TAG_ID, text, 0]]
    
    return None

"""
    特判两种 modify word
"""
def modify_word_parse(text: str):
    if text == WORD_DEL:
        return WORD_DEL
    elif text == WORD_CLR:
        return WORD_CLR
    
    return None

"""
    .key 判断, 需要括号外的半截字符粗
"""
def with_tag_parse(text: str):
    if len(text) == 0 or text[0] != MEMBER_SYMBOL:
        return None
    text_split = text.split(" ")
    return text_split[0][1:]


"""
    [id] a=b
    return the event
"""
def get_event(text: str):
    ret = None

    # two parts
    bracket_raw = bracket_parse(text, INDEX_SYMBOL[0], INDEX_SYMBOL[1])

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

    target_tag = with_tag_parse(bracket_raw[1])
    if target_tag is not None:
        remain_right = bracket_raw[1].replace(MEMBER_SYMBOL + target_tag, "").strip(" ")
    else:
        remain_right = bracket_raw[1].strip(" ")

    right_assign = assign_parse(remain_right, MODIFY_ASSIGN)
    right_word = modify_word_parse(remain_right)

    # modify
    if (left_other != None or left_assign != None) and (right_assign != None or right_word != None) and remain_right != "":
        ret = ModifyEvent()
        ret.target_tag = target_tag
        word = modify_word_parse(remain_right)
        
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
        ret.target_tag = target_tag

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
        if raw.text == COMMIT_COMMAND:
            return CommitEvent()
        elif raw.text == BACKUP_COMMAND:
            return BackupEvent()
        elif raw.text == RELOAD_COMMAND:
            return ReloadEvent()
        elif raw.text == ROLLBACK_COMMAND:
            return RollbackEvent()
        
        index_match = re.match(INDEX_REGEX, raw.text)
        modify_match = re.match(MODIFY_REGEX, raw.text)

        if index_match or modify_match:
            if index_match:
                modify_body = raw.text[index_match.span()[1]:].strip()
                if modify_body != "" and not re.match(MODIFY_REGEX, modify_body):
                    return None

            cm_event = get_event(raw.text)
            # cm_event.tell()

            if cm_event != None:
                cm_event.quote = raw.quote
                return cm_event

    return None