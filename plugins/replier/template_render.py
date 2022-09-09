import re

from core.error import Error

from plugins.replier.plugin_config import *

"""
    带参模板串解析库

    规则:
        {} 作为关键字符, {} 内的内容为参数名, 如果 {} 内没填参数名默认以 1 2 3 ... 往下命名

    argmap: 参数名 -> {串 (text: str) -> 串中位置}
"""

"""
    解析带参串, 得到一个 list, list 中每个元素是一个二元组, 代表左右括号位置
"""
def get_bracket_list(text: str):
    bracket_list = []
    detect_left = False
    not_continue = False

    for i in range(len(text)):
        if text[i] == TEMPLATE_BRACKET[0]:
            if not_continue:
                return Error("不能连续参数, 无法解析")
            if not detect_left:
                detect_left = True
                bracket_list.append([])
                bracket_list[len(bracket_list)-1].append(i)
            else:
                return Error("括号不匹配")
        elif text[i] == TEMPLATE_BRACKET[1]:
            if detect_left:
                detect_left = False
                bracket_list[len(bracket_list)-1].append(i)
                not_continue = True
            else:
                return Error("括号不匹配")
        else:
            not_continue = False

    return bracket_list


"""
    Input: 一个带 {} 的字符串
    Return: 一个把 {} 之间的东西都抽掉的字符串
    并填充此 argmap
"""
def extract_argmap(text: str, argmap: dict):
    bracket_list = get_bracket_list(text)

    if isinstance(bracket_list, Error):
        return bracket_list

    ret_text = text[:]
    replace_symbol = "髍"
    for i in range(len(bracket_list)):
        ret_text = ret_text[:bracket_list[i][0]] + TEMPLATE_BRACKET[0] + replace_symbol*(bracket_list[i][1]-bracket_list[i][0]-1) + TEMPLATE_BRACKET[1] + ret_text[bracket_list[i][1]+1:]

    ret_text = ret_text.replace(replace_symbol, "")

    self_incre = 0

    for i in range(len(bracket_list)):
        argname = text[bracket_list[i][0]+1:bracket_list[i][1]].strip()

        if argname == "":
            argname = str(self_incre)
            self_incre += 1

        if not argname in argmap:
            argmap[argname] = {}
        
        if not ret_text in argmap[argname]:
            argmap[argname][ret_text] = []
        
        argmap[argname][ret_text].append(i)

    return ret_text

"""
    匹配一个 text 和一个 template
"""
def template_match(text: str, template: str):
    pattern = "^" + template.replace(TEMPLATE_BRACKET[0] + TEMPLATE_BRACKET[1], "\S[\s\S]*") + "$"
    return re.match(pattern, text) is not None


"""
    根据一个 template 串和一个 argmap, 收集 text 中的所有 arg 信息并返回.
    Return: 一个 dict (collected_map), argname -> argvalue
"""
def collect(text: str, template: str, argmap: dict):
    ret = {}
    arg_count = 0
    
    i = 0
    j = 0
    while i < len(template):
        if template[i] == TEMPLATE_BRACKET[0]:
            # 跳过右括号
            # 现在指向右括号下一个
            i += 2
        
            argvalue = ""

            # 如果不是末尾的参数情况, 只要一直等到相等就好
            # 此时的 j 指向argvalue第一个字符
            if i < len(template):
                while text[j] != template[i]:
                    argvalue += text[j]
                    j += 1
                    if j >= len(text):
                        return Error("collect failed")
 
            # 末尾参数, 直接拉到结束, j 无所谓了
            else:
                argvalue = text[j:]

            for argname in argmap:
               if arg_count in argmap[argname][template]: 
                    ret[argname] = argvalue
                    arg_count += 1
                    break
        else:
            i += 1
            j += 1
    
    return ret

"""
    渲染一个带参的 template 为正常串
    Input: 带参串 raw
    Return: 渲染完毕的串
"""
def render(raw: str, collected_map: dict):
    bracket_list = get_bracket_list(raw)
    
    self_incre = 0
    for i in range(len(bracket_list)):
        argname = raw[bracket_list[i][0]+1: bracket_list[i][1]].strip()
        
        if argname == "":
            argname = str(self_incre)
            left_pos = bracket_list[i][0] + self_incre
            right_pos = bracket_list[i][1] + self_incre
            self_incre += 1

            raw = raw[:left_pos+1] + argname + raw[right_pos:]
    
    ret = raw[:]
    for argname in collected_map:
        ret = ret.replace(TEMPLATE_BRACKET[0] + argname + TEMPLATE_BRACKET[1], collected_map[argname])

    return ret