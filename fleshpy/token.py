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
    Begin = 11,
    EOF = 12,
    Else = 13,

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        match self:
            case TokenType.LParen: return "("
            case TokenType.RParen: return ")"
            case TokenType.ID: return "Identifier"
            case TokenType.Define: return "Define"
            case TokenType.Lambda: return "("
            case TokenType.Let: return "Let"
            case TokenType.If: return "If"
            case TokenType.Integer: return "Integer"
            case TokenType.Float: return "Float"
            case TokenType.String: return "String"
            case TokenType.Cond: return "Cond"
            case TokenType.Begin: return "Begin"
            case TokenType.EOF: return "EOF"
            case TokenType.Else: return "Else"


class Token:
    def __init__(self, lexeme: str, index: int, ty: TokenType) -> None:
        self.lexeme = lexeme
        self.index = index
        self.ty = ty

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"Token {{ {self.lexeme}, {self.index}, {self.ty} }}"
