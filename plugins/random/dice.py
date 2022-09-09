"""
    Basic class in the expression
"""
from typing import Union
from core.error import Error
import random

from plugins.random.plugin_config import DICE_N_THRESHOLD, DICE_V_THRESHOLD

class DiceExpr:
    ...


class Integer(DiceExpr):
    """
        value: 值
    """
    def __init__(self, value: int):
        self.value = value


class PrimDiceExpr(DiceExpr):
    """
        XdY.
        X: int   是骰子个数
        Y: int   是骰子面数
    """
    def __init__(self, X: int, Y: int):
        self.X = X
        self.Y = Y


class ExprWithOp(DiceExpr):
    """
        op: str
        lhs: DiceExpr
        rhs: DiceExpr
    """
    def __init__(self, op: str, lhs: DiceExpr, rhs: DiceExpr):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs


"""
    build the dice expr.
"""
def build(text: str) -> Union[DiceExpr, Error]:
    # print("build:", text)

    # 空串错误
    if text == "":
        return Error("骰子表达式有误, 树构建失败", urge="Random_Plugin")

    bracket_list = []
    cnt = 0

    for i in range(len(text)):
        if text[i] == "(":
            if cnt == 0:
                bracket_list.append([])
                bracket_list[len(bracket_list)-1].append(i)
            cnt += 1
        elif text[i] == ")":
            cnt -= 1
            if cnt == 0:
                bracket_list[len(bracket_list)-1].append(i)
    
    encoded_text = text[:]
    if len(bracket_list) > 0:
        # 不改变长度
        for bra in bracket_list:
            encoded_text = encoded_text[:bra[0]+1] + "?"*(bra[1] - bra[0] - 1) + encoded_text[bra[1]:]
    
    # 按照优先级. 二元运算符
    # 0: + - 
    # 1: * / 
    # 2: ^
    op_list = [['+', '-'], ['*', '/'], ['^']]
    for op_level in range(3):
        op_pos = -1
        for i in range(len(encoded_text)):
            if op_level == 2:
                pos = i
            else:
                pos = len(encoded_text)-i-1
            if encoded_text[pos] in op_list[op_level]:
                op_pos = pos
                break
        
        if op_pos != -1:
            lhs = build(text[:op_pos])
            if isinstance(lhs, Error):
                return lhs
            rhs = build(text[op_pos+1:])
            if isinstance(rhs, Error):
                return rhs
            return ExprWithOp(text[op_pos], lhs, rhs)

    # bracket
    if len(bracket_list) > 0:
        assert len(bracket_list) == 1
        assert bracket_list[0][0] == 0
        assert bracket_list[0][1] == len(text)-1
        return build(text[1:len(text)-1])
    
    # prim
    d_pos = text.find("d")
    if d_pos != -1:
        if str.isdigit(text[:d_pos]) and str.isdigit(text[d_pos+1:]):
            return PrimDiceExpr(int(text[:d_pos]), int(text[d_pos+1:]))
        else:
            return Error("骰子表达式d两侧必须是非负整数!", urge="Random_Plugin")
    else:
        if str.isdigit(text):
            return Integer(int(text))
        else:
            return Error("骰子表达式常数必须是非负整数!", urge="Random_Plugin")

"""
    eval the dice expr.
"""
def evaluate(expr: Union[DiceExpr, Error]) -> Union[int, Error]:
    if isinstance(expr, Error):
        return expr
    elif isinstance(expr, Integer):
        if expr.value > DICE_V_THRESHOLD:
            return Error("常数太大!", urge="Random_Plugin")
        return expr.value
    elif isinstance(expr, PrimDiceExpr):
        result = 0
        if expr.X > DICE_N_THRESHOLD:
            return Error("骰子个数太大!", urge="Random_Plugin")
        if expr.Y > DICE_V_THRESHOLD:
            return Error("骰子面数太大!", urge="Random_Plugin")
        for _ in range(expr.X):
            result += random.randint(1, expr.Y)
        return result
    elif isinstance(expr, ExprWithOp):
        if expr.op == '+':
            result = evaluate(expr.lhs) + evaluate(expr.rhs)
        elif expr.op == '-':
            result = evaluate(expr.lhs) - evaluate(expr.rhs)
        elif expr.op == '*':
            result = evaluate(expr.lhs) * evaluate(expr.rhs)
        elif expr.op == '/':
            result = evaluate(expr.lhs) // evaluate(expr.rhs)
        elif expr.op == '^':
            result = evaluate(expr.lhs) ** evaluate(expr.rhs)
        else:
            return Error("内部错误: 未知的op")

        if result > DICE_V_THRESHOLD or result < -DICE_V_THRESHOLD:
            return Error("数值太大!", urge="Random_Plugin")
        
        return result