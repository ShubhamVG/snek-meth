from collections.abc import Container
from string import ascii_lowercase, digits

import token
import utils

_CHAR_TO_TOKEN_DICT = {
        '+': token.Token(token.TokenType.ADD),
        '-': token.Token(token.TokenType.SUB),
        '*': token.Token(token.TokenType.MUL),
        '/': token.Token(token.TokenType.DIV),
        '^': token.Token(token.TokenType.POW),
        '(': token.Token(token.TokenType.LPAREN),
        ')': token.Token(token.TokenType.RPAREN),
}

_FN_NAME_TO_TOKEN_DICT = {
        'sin': token.Token(token.TokenType.SIN),
        'cos': token.Token(token.TokenType.COS),
        'tan': token.Token(token.TokenType.TAN),
        'cot': token.Token(token.TokenType.COT),
        'sec': token.Token(token.TokenType.SEC),
        'csc': token.Token(token.TokenType.CSC),
        'ln': token.Token(token.TokenType.LN),
}


class Lexer:
    def __init__(self, expr: str) -> None:
        self.expr = expr.replace(" ", "")
        self.pos = -1
        self.end_pos = len(self.expr) - 1
        self.current_char: Optional[str] = None
        self.advance()


    def advance(self) -> None:
        if self.pos > self.end_pos:
            return
        elif self.pos == self.end_pos:
            self.pos += 1
            self.current_char = None
            return

        self.pos += 1
        self.current_char = self.expr[self.pos]


    def curr_char_matches(self, *items: tuple[Container, ...]) -> bool:
        for item in items:
            if self.pos <= self.end_pos and self.current_char in item:
                return True

        return False


    def get_name(self) -> str:
        name = ''

        while self.curr_char_matches(ascii_lowercase):
            name += self.current_char
            self.advance()

        return name


    def get_num(self) -> utils.Num:
        num_str = ''
        decimal_found = False
        allowed_chars = digits + '.'

        while self.curr_char_matches(allowed_chars):
            if self.current_char == '.':
                if decimal_found:
                    raise DoubleDecimalError(num_str)

                decimal_found = True

            num_str += self.current_char
            self.advance()

        return utils.Num(num_str)


    def get_tokens(self) -> list[token.Token]:
        tokens: list[token.Token] = []

        while self.pos <= self.end_pos:
            if self.current_char in _CHAR_TO_TOKEN_DICT:
                t = _CHAR_TO_TOKEN_DICT[self.current_char]
                tokens.append(t)
                self.advance()
            elif self.current_char in digits:
                num = self.get_num()
                t = token.Token(token.TokenType.NUM, num)
                tokens.append(t)
            elif self.current_char in ascii_lowercase:
                name = self.get_name()
                t = _FN_NAME_TO_TOKEN_DICT.get(name, None)
                
                if t is not None:
                    tokens.append(t)
                else:
                    t = token.Token(token.TokenType.VAR, name)
                    tokens.append(t)
            else:
                raise InvalidCharError(self.current_char)

        return tokens


class LexerError(Exception):
    pass


class DoubleDecimalError(LexerError):
    def __init__(self, num_str: str) -> None:
        super().__init__(f'Second decimal found with {num_str}')


class InvalidCharError(LexerError):
    def __init__(self, inv_char: str) -> None:
        super().__init__(f'Invalid char {inv_char}')


# class InvalidTokenError(LexerError):
#     def __init__(self, inv_tok_str: str) -> None:
#         super().__init__(f'Invalid token {inv_tok_str}')
