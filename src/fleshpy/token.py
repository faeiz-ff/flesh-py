
from enum import Enum


class TokenType(Enum):
    LParen = 0,
    RParen = 1,
    ID = 2,
    Define = 3,
    Lambda = 4,
    Let = 5,
    If = 6,
    Integer = 7,
    Float = 8,
    String = 9,
    Cond = 10,
    Block = 11,


class Token:
    def __init__(self, lexeme: str, index: int, ty: TokenType) -> None:
        self.lexeme = lexeme
        self.index = index
        self.ty = ty
