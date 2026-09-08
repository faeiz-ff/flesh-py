from enum import Enum, auto


class TokenType(Enum):
    LParen = auto(),
    RParen = auto(),
    ID = auto(),
    Define = auto(),
    Lambda = auto(),
    Let = auto(),
    If = auto(),
    Integer = auto(),
    Float = auto(),
    String = auto(),
    Cond = auto(),
    Begin = auto(),
    EOF = auto(),
    Else = auto(),
    Truth = auto(),
    Falsity = auto(),
    Nil = auto(),
    Dot = auto(),

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
            case TokenType.Truth: return "True"
            case TokenType.Falsity: return "False"
            case TokenType.Nil: return "Nil"
            case TokenType.Dot: return "."


class Token:
    def __init__(self, lexeme: str, index: int, ty: TokenType) -> None:
        self.lexeme = lexeme
        self.index = index
        self.ty = ty

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"Token {{ {self.lexeme}, {self.index}, {self.ty} }}"
