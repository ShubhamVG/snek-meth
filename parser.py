from typing import Optional

import meth
import token

class Parser:
    def __init__(self, tokens: list[token.Token]) -> None:
        self.tokens = tokens
        self.current_token: Optional[token.Token] = None
        self.pos = -1
        self.end = len(self.tokens) - 1
        self.advance()


    def advance(self) -> None:
        if self.pos > self.end:
            return
        elif self.pos == self.end:
            self.pos += 1
            self.current_token = None
            return

        self.pos += 1
        self.current_token = self.tokens[self.pos]


    def current_ttype_matches(
            self,
            *ttypes: tuple[token.TokenType, ...],
    ) -> bool:
        if self.current_token is None:
            return False

        return self.current_token.ttype in ttypes


    def get_syntax_tree(self) -> meth.EvalNode:
        return self.get_expr()


    def get_expr(self) -> Optional[meth.EvalNode]:
        left = self.get_term()

        while self.current_ttype_matches(
                token.TokenType.ADD,
                token.TokenType.SUB,
        ):
            op = self.current_token.ttype
            self.advance()
            right = self.get_term()

            if right is None:
                raise IncompleteExprError(self.pos)

            left = meth.BinaryNode(op=op, left=left, right=right)

        return left


    def get_term(self) -> Optional[meth.EvalNode]:
        left = self.get_factor()

        while self.current_ttype_matches(
                token.TokenType.MUL,
                token.TokenType.DIV,
        ):
            op = self.current_token.ttype
            self.advance()
            right = self.get_factor()

            if right is None:
                raise IncompleteExprError(self.pos)

            left = meth.BinaryNode(op=op, left=left, right=right)

        return left


    def get_factor(self) -> Optional[meth.EvalNode]:
        to_neg = False

        if self.current_ttype_matches(token.TokenType.ADD):
            self.advance()
        elif self.current_ttype_matches(token.TokenType.SUB):
            to_neg = True
            self.advance()

        left = self.get_atom()
        if to_neg:
            left = meth.UnaryNode(op=token.TokenType.NEG, val=left)

        if self.current_ttype_matches(token.TokenType.POW):
            self.advance()
            right = self.get_factor()
            left = meth.BinaryNode(
                    op=token.TokenType.POW,
                    left=left,
                    right=right,
            )

        return left


    def get_atom(self) -> Optional[meth.EvalNode]:
        if self.current_token.ttype in (token.TokenType.NUM, token.TokenType.VAR):
            t = self.current_token
            self.advance()
            return meth.UnaryNode(op=t.ttype, val=t.val)

        if self.current_ttype_matches(token.TokenType.LPAREN):
            self.advance()
            expr = self.get_expr()
            
            if self.current_ttype_matches(token.TokenType.RPAREN):
                self.advance()
                return expr
            else:
                raise MissingParenError(self.pos)

        if self.current_ttype_matches(
                token.TokenType.SIN,
                token.TokenType.COS,
                token.TokenType.TAN,
                token.TokenType.COT,
                token.TokenType.SEC,
                token.TokenType.CSC,
                token.TokenType.LN,
        ):
            op = self.current_token.ttype
            self.advance()
            expr: Optional[meth.EvalNode] = None

            if self.current_ttype_matches(token.TokenType.LPAREN):
                self.advance()
                expr = self.get_expr()
            else:
                raise MissingParenError(self.pos)

            if self.current_ttype_matches(token.TokenType.RPAREN):
                self.advance()
                return meth.UnaryNode(op=op, val=expr)
            else:
                raise MissingParenError(self.pos)


class ParserError(Exception):
    pass


class MissingParenError(ParserError):
    def __init__(self, pos: int) -> None:
        super().__init__(f'Expected parenthesis at {pos}')
        

class IncompleteExprError(ParserError):
    def __init__(self, pos: int) -> None:
        super().__init__(f'Expected expression at {pos}')
