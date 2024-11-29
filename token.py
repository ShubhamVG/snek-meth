from enum import auto, Enum
from typing import Optional

import utils

class TokenType(Enum):
    # values and placeholders
    NUM = auto()
    VAR = auto()

    # BEDMAS symbols
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    POW = auto()
    LPAREN = auto()
    RPAREN = auto()

    # trig functions
    SIN = auto()
    COS = auto()
    TAN = auto()
    COT = auto()
    SEC = auto()
    CSC = auto()

    # other functions
    LN = auto()

    # I don't know how to describe this
    CLOSURE = auto()
    NEG = auto()


class Token:
    def __init__(
            self,
            ttype: TokenType,
            val: Optional[utils.Num] = None,
    ) -> None:
        self.ttype = ttype
        self.val = val


    def __repr__(self) -> str:
        if self.val is None:
            return f'<{self.ttype.name}>'

        return f'<{self.ttype.name}: {self.val}>'
