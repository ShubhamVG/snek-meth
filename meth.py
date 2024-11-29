from enum import auto, Enum

import token
import math

import utils

class EvalNode:
    pass


MathNode = utils.Num | EvalNode

class UnaryNode(EvalNode):
    def __init__(
            self,
            op: token.TokenType,
            val: MathNode | str, # str is for variable names
    ) -> None:
        self.op = op
        self.val = val


    def __repr__(self) -> str:
        return f'Unary(op:{self.op}, val:{self.val})'


class BinaryNode(EvalNode):
    def __init__(
            self,
            op: token.TokenType,
            left: MathNode,
            right: MathNode,
    ) -> None:
        self.op = op
        self.left = left
        self.right = right


    def __repr__(self) -> str:
        return f'Binary(op:{self.op}, l:{self.left}, r:{self.right})'


class Interpreter:
    def __init__(self, m_node: MathNode) -> None:
        self.m_node = m_node


    def evaluate(self, var_dict: dict[str, utils.Num]) -> utils.Num:
        return Interpreter._evaluate(self.m_node, var_dict)


    @staticmethod
    def _evaluate(
            m_node: MathNode,
            var_dict: dict[str, utils.Num],
    ) -> utils.Num:
        if m_node.op == token.TokenType.NUM:
            return m_node.val

        if m_node.op == token.TokenType.VAR:
            if m_node.val in var_dict:
                return var_dict[m_node.val]
            else:
                raise UnknownVariableError(m_node.val)

        if m_node.op == token.TokenType.ADD:
            left = Interpreter._evaluate(m_node.left, var_dict)
            right = Interpreter._evaluate(m_node.right, var_dict)

            return left + right

        if m_node.op == token.TokenType.SUB:
            left = Interpreter._evaluate(m_node.left, var_dict)
            right = Interpreter._evaluate(m_node.right, var_dict)

            return left - right

        if m_node.op == token.TokenType.MUL:
            left = Interpreter._evaluate(m_node.left, var_dict)
            right = Interpreter._evaluate(m_node.right, var_dict)

            return left * right

        if m_node.op == token.TokenType.DIV:
            left = Interpreter._evaluate(m_node.left, var_dict)
            right = Interpreter._evaluate(m_node.right, var_dict)

            return left / right

        if m_node.op == token.TokenType.POW:
            left = Interpreter._evaluate(m_node.left, var_dict)
            right = Interpreter._evaluate(m_node.right, var_dict)

            return left ** right

        if m_node.op == token.TokenType.SIN:
            val = Interpreter._evaluate(m_node.val, var_dict)
            return math.sin(val)

        if m_node.op == token.TokenType.COS:
            val = Interpreter._evaluate(m_node.val, var_dict)
            return math.cos(val)

        if m_node.op == token.TokenType.TAN:
            val = Interpreter._evaluate(m_node.val, var_dict)
            return math.tan(val)

        if m_node.op == token.TokenType.COT:
            val = Interpreter._evaluate(m_node.val, var_dict)
            return math.cot(val)

        if m_node.op == token.TokenType.SEC:
            val = Interpreter._evaluate(m_node.val, var_dict)
            return math.sec(val)

        if m_node.op == token.TokenType.CSC:
            val = Interpreter._evaluate(m_node.val, var_dict)
            return math.csc(val)

        if m_node.op == token.TokenType.LN:
            val = Interpreter._evaluate(m_node.val, var_dict)
            return math.log(val)

        if m_node.op == token.TokenType.NEG:
            val = Interpreter._evaluate(m_node.val, var_dict)
            return -val


class InterpreterError(Exception):
    pass


class UnknownVariableError(InterpreterError):
    def __init__(self, var_name: str) -> None:
        super().__init__(
                f'Unknown symbol or value not present in var_dict of {var_name}'
        )
