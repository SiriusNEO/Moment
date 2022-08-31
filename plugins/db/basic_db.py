import json
import os

from core.error import Error
from core.message import Message
from plugins.db.db_event import TagPair

from plugins.db.plugin_config import WORD_DEL, WORD_CLR, SHADOW_CODE, ID

# the file structure depends on the image server
from core.image import *

from utils.log import Log

class DataBase:
    """
        path: str
        storage: list
        tag_type: dict
    """

    def __init__(self, path):
        self.path = path
        if os.path.exists(path):
            with open(path, "r") as fp:
                self.storage = list(json.load(fp, object_hook=decode_hook))
        else:
            Log.info("create database: ", path)
            self.storage = list()
            with open(path, "w") as fp:
                json.dump(self.storage, fp, cls=MessageJSONEncoder)
        
        self.tag_type = {}
        
        Log.info("database {0} init finish.".format(path))
    
    def load_from(self, path=None):
        if path is None:
            path = self.path
        try:
            with open(path, "r") as fp:
                self.storage = list(json.load(fp, object_hook=decode_hook))
        except Exception as e:
            return Error(e.args)

    
    def write_back(self, path=None):
        if path is None:
            path = self.path
        
        with open(path, "w") as fp:
            json.dump(self.storage, fp, cls=MessageJSONEncoder)


    def _insert(self, line: dict()):
        storage.append(line)
    
    # 此处在函数中对可变对象 ret 进行修改, 为引用效果

    def _single_query(self, index: TagPair, ret: list, is_first_query: bool):

        for line in self.storage:
            # 此 line 无此 tag. 注意 ID 特判
            if index.tag != ID and index.tag not in line:
                continue

            match_flag = None

            # 如果是多关键词, 需要匹配所有词
            if self.tag_type[index.tag] == list:
                match_flag = True
                for content in line[index.tag]:    
                    # 完全匹配
                    if index.typ == 0:
                        if not content == index.val:
                            match_flag = False
                            break

                    # 局部匹配 ?
                    elif index.typ == 1:
                        if type(content) != Message:
                            return Error("类型错误，对非信息关键词执行模糊匹配")
                        else: 
                            if not (content.text is not None and index.val.text != "" and content.text.find(index.val.text) != -1):
                                match_flag = False
                                break   
                     
                    # 局部匹配 @
                    elif index.typ == 4:
                        if type(content) != Message:
                            return Error("类型错误，对非信息关键词执行模糊匹配")
                        else: 
                            if not (content.text is not None and content.text != "" and index.val.text.find(content.text) != -1):
                                match_flag = False
                                break

                    else:
                        return Error("未知的查询类型")

            # 单关键词, 直接判断本身
            else:
                # 单关键词需要检查类型
                if type(index.val) != self.tag_type[index.tag]:
                    return Error("查询类型不匹配")
                
                # 完全匹配
                if index.typ == 0:
                    # 特判 id
                    if index.tag == ID:
                        match_flag = (self.storage.index(line) == index.val)
                    # 成功
                    elif index.val == line[index.tag]:
                        match_flag = True
                    # 失败
                    else:
                        match_flag = False

                # 局部匹配: ?
                elif index.typ == 1:
                    if index.tag == ID or type(line[index.tag]) != Message:
                        return Error("类型错误，对非信息类关键词执行模糊匹配")
                    else:
                        # 成功
                        if line[index.tag].text != None and index.val.text != "" and line[index.tag].text.find(index.val.text) != -1:
                            match_flag = True
                        # 失败
                        else:
                            match_flag = False
                
                # 局部匹配: @
                elif index.typ == 4:
                    if index.tag == ID or type(line[index.tag]) != Message:
                        return Error("类型错误，对非信息类关键词执行模糊匹配")
                    else:
                        # 成功
                        if line[index.tag].text != None and line[index.tag].text != "" and index.val.text.find(line[index.tag].text) != -1:
                            match_flag = True
                        # 失败
                        else:
                            match_flag = False
                
                # 大小匹配: > <
                elif index.typ == 2 or index.typ == 3:
                    if index.tag != ID and (type(line[index.tag]) != int or type(line[index.tag]) != float):
                        return Error("类型错误，对非数值关键词执行大小匹配")
                    else:
                        if index.tag == ID:
                            line_data = self.storage.index(line)
                        else:
                            line_data = line[index.tag]
                        # 成功
                        if (index.typ == 2 and line_data > index.val) or (index.typ == 3 and line_data < index.val):
                            match_flag = True
                        # 失败
                        else:
                            match_flag = False

            assert match_flag is not None
            # 结算
            if match_flag and is_first_query:
                ret.append(line)
            if not match_flag and not is_first_query and line in ret:
                ret.remove(line)


    def _single_modify_check(self, lines: list, modify: TagPair):
        # 检查合法性, 保证不合法不发生任何修改
        
        if modify.tag == ID:
            return Error("禁止修改id")
        
        if modify.typ >= 1 and self.tag_type[modify.tag] != list:
            return Error("此数据条目不支持list操作！")
        else:
            # 奇妙的逻辑
            if self.tag_type[modify.tag] != type(modify.val) and (self.tag_type[modify.tag] == list and type(modify.val) != Message):
                return Error("修改数据条目类型不匹配！")
        
    
    def _single_modify(self, lines: list, modify: TagPair):
        # 经过 check 之后无需检查合法性
        
        for line in lines:
            # 单点修改
            if modify.typ == 0:
                if self.tag_type[modify.tag] == list:
                    line[modify.tag] = list()
                    line[modify.tag].append(modify.val)
                else:
                    line[modify.tag] = modify.val
            # 添加
            elif modify.typ == 1:
                line[modify.tag].append(modify.val)
            # 删除
            elif modify.typ == 2:
                line[modify.tag].remove(modify.val)
            else:
                return Error("未知修改类型: {}".format(modify.typ))

    """
        返回两个 list, 表示消息与消息的 id 号
    """
    def query(self, indices: list, target_tag = None):
        lines = list()

        # [] 判断
        if len(indices) == 0:
            lines = self.storage[:]
        else:
            for i in range(len(indices)):
                error = self._single_query(indices[i], lines, (i == 0))

                if error != None:
                    return error, None

        # 指定字段返回, 不考虑第二返回值
        if target_tag is not None:
            ret = []
            for line in lines:
                if target_tag not in line:
                    return Error("所选目标不全都有tag: {}".format(target_tag)), None
            
            for line in lines:
                if self.tag_type[target_tag] == list:
                    ret += line[target_tag]
                else:
                    ret.append(line[target_tag])
            return ret, None
            
        ret_id = list()

        # id 直接强行赋值, 不储存
        for line in lines:
            ret_id.append(self.storage.index(line))

        return lines, ret_id


    def modify(self, indices: list, modifies: list, word: str, target_tag = None):
        # id is no need
        lines, _ = self.query(indices)

        if len(lines) == 0:
            return Error("没找到目标")

        if type(lines) == Error:
            return lines

        if word is not None and len(modifies) >= 1:
            return Error("命令修改不可同时与其它修改共存")
        
        if target_tag is not None and len(modifies) >= 1:
            return Error("修改指定字段时不支持命令修改")

        for modify in modifies:
            error = self._single_modify_check(lines, modify)

            if error != None:
                return error

            for modify_1 in modifies:
                if modify != modify_1 and modify.tag == modify_1.tag:
                    return Error("重复 tag 修改!")
        
        if word is not None:
            if target_tag is not None:
                for line in lines:
                    if target_tag not in line:
                        return Error("所选目标不全都有tag: {}".format(target_tag))
                if word == WORD_DEL:
                    for line in lines:
                        self.storage[self.storage.index(line)].pop(target_tag)
                elif word == WORD_CLR:
                    for line in lines:
                        if self.tag_type[target_tag] == list:
                            self.storage[self.storage.index(line)][target_tag] = []
                        elif self.tag_type[target_tag] == str:
                            self.storage[self.storage.index(line)][target_tag] = ""
                        elif self.tag_type[target_tag] == Message():
                            self.storage[self.storage.index(line)][target_tag] = Message()
                        elif self.tag_type[target_tag] == int or self.tag_type[target_tag] == float:
                            self.storage[self.storage.index(line)][target_tag] = 0
            else:
                if word == WORD_DEL:
                    for line in lines:
                        self.storage.remove(line)
                elif word == WORD_CLR:
                    for line in lines:
                        self.storage[self.storage.index(line)] = {}
        else:
            for modify in modifies:
                self._single_modify(lines, modify)
    

    def new(self, modifies: list):
        new_line = [dict()]
        new_line[0][SHADOW_CODE] = id(new_line[0])
        
        for modify in modifies:
            if modify.typ >= 1:
                return Error("新创建条目时禁止 list 操作")
            
            error = self._single_modify_check(new_line, modify)

            if error != None:
                return error

            for modify_1 in modifies:
                if modify != modify_1 and modify.tag == modify_1.tag:
                    return Error("重复 tag 修改！")

        for modify in modifies:
            self._single_modify(new_line, modify)

        self.storage.append(new_line[0])
        
    def display(self):
        print("database ({0}) start print: ".format(self.path))

        for line in self.storage:
            print(line)

                
