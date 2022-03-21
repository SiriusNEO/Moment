
from db.db_config import *

from model.event import *

from model.error import Error

from db.basic_db import DataBase

db_table = {
    CM_PATH: DataBase(CM_PATH), 
    USER_PATH: DataBase(USER_PATH),
    ALIAS_PATH: DataBase(ALIAS_PATH)
}

db_col = {
    CM_PATH: CM_COL,
    USER_PATH: USER_COL,
    ALIAS_PATH: ALIAS_COL
}

def info_cut(text: str):
    if len(text) > MAX_INFO_LEN:
        return text[0:MAX_INFO_LEN] + "..."
    return text

def display_line(line: dict, id: int):
    ret = "{0}: ".format(id)
    for tag in line:
        if tag == SHADOW_CODE:
            continue
        if COL_T[tag] == list:
            ret += "{0}=".format(tag)
            if len(line[tag]) > 1:
                ret += "["
            
            for val in line[tag]:
                # 一定是 msg
                ret += val.msg_2_str() + ", "
            ret = ret[0: len(ret)-2]

            if len(line[tag]) > 1:
                ret += "]"
        else:
            ret += "{0}={1}".format(tag, info_cut(str(line[tag])))
        ret += "; "
    return ret[0: len(ret)-2]

def msg_wrap(tag_pair: TagPair):
    if COL_T[tag_pair.tag] == list:
        if tag_pair.val == THIS:
            tag_pair.val = event.quote
        else:
            text = tag_pair.val
            tag_pair.val = Message()
            tag_pair.val.text = text
    elif COL_T[tag_pair.tag] == int:
        if not str.isdigit(tag_pair.val):
            return Error("{0}应该是个整数！".format(tag_pair.tag))
        tag_pair.val = int(tag_pair.val)
    elif COL_T[tag_pair.tag] == float:
        if not is_float(tag_pair.val):
            return Error("{0}应该是个浮点数！".format(tag_pair.tag))
        tag_pair.val = float(tag_pair.val)

def db_event_handle(event: BaseEvent):
    reply = Message()

    # 信息包装
    if hasattr(event, 'indices'):
        for index in event.indices:
            if index.tag not in db_col[event.target_db]:
                return Error("标签不存在！")
            error = msg_wrap(index)
            if error != None:
                return error
    
    if hasattr(event, 'modifies'):
        for modify in event.modifies:
            if modify.tag not in db_col[event.target_db]:
                return Error("标签不存在！")
            error = msg_wrap(modify)
            if error != None:
                return error

    event.tell()

    if type(event) == QueryEvent:
        print(event.target_db)

        result, result_id = db_table[event.target_db].query(event.indices)

        if type(result) == Error:
            return result
        else:
            if len(result) == 0:
                reply.text = "很遗憾, 查询结果为空"
            elif len(result) > QUERY_DISPLAY_THRESHOLD:
                reply.text = "共有 {0} 条数据, 仅显示最新 {1} 条:\n".format(len(result), QUERY_DISPLAY_THRESHOLD)
                for i in range(len(result)-QUERY_ASSIGN, len(result)):
                    reply.text += result[i] + "\n"
            else:
                reply.text = "共有 {0} 条数据:\n".format(len(result))
                for i in range(len(result)):
                    # to do: 更好的显示方式
                    reply.text += display_line(result[i], result_id[i])
                    if i < len(result)-1:
                        reply.text += "\n"

    elif type(event) == ModifyEvent:
        
        result = db_table[event.target_db].modify(event.indices, event.modifies, event.word)

        if type(result) == Error:
            return result
        else:
            reply.text = "修改成功!"

    elif type(event) == NewEvent:
        
        result = db_table[event.target_db].new(event.modifies)

        if type(result) == Error:
            return result
        else:
            reply.text = "添加成功!"

    else:
        return Error("非数据库事件被分派到给数据库中心处理")
    
    display()

    return reply

def display():
    for db_path in db_table:
        db_table[db_path].display()