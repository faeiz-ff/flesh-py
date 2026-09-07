from typing import Optional

from fleshpy.token import Token, TokenType


class Lexer:
    def __init__(self) -> None:
        self.idx = 0
        self.text = ""

    def curr(self) -> Optional[str]:
        return self.text[self.idx] if self.idx < len(self.text) else None

    def number(self) -> Token:
        begin = self.idx
        is_float = False
        curr = self.curr()
        while curr is not None and curr.isdigit():
            self.idx += 1
            curr = self.curr()

            if curr == '.' and not is_float:
                is_float = True
                self.idx += 1
                curr = self.curr()

        lexeme = self.text[begin:self.idx]

        # lex forwards the self.idx after every token
        # so we need to decrement it in here
        self.idx -= 1

        if is_float:
            return Token(lexeme, begin, TokenType.Float)
        else:
            return Token(lexeme, begin, TokenType.Integer)

    def key_or_id(self) -> Token:
        begin = self.idx

        curr = self.curr()
        while curr is not None and \
                curr != '(' and curr != ')' and \
                not curr.isspace():
            self.idx += 1
            curr = self.curr()

        lexeme = self.text[begin:self.idx]

        tok = Token(lexeme, begin, TokenType.ID)
        match lexeme:
            case 'define': tok.ty = TokenType.Define
            case 'if': tok.ty = TokenType.If
            case 'lambda': tok.ty = TokenType.Lambda
            case 'cond': tok.ty = TokenType.Cond
            case 'block': tok.ty = TokenType.Block
            case 'let': tok.ty = TokenType.Let

        return tok

    def skip_whitespace(self) -> None:
        curr = self.curr()
        while curr is not None and curr.isspace():
            self.idx += 1
            curr = self.curr()

    def lex(self, text: str) -> list[Token]:
        tokens: list[Token] = []
        self.idx = 0
        self.text = text

        while self.idx < len(self.text):
            self.skip_whitespace()
            lexeme = self.text[self.idx]

            if lexeme.isdigit():
                tokens.append(self.number())
            elif lexeme == '(':
                tokens.append(Token(lexeme, self.idx, TokenType.LParen))
            elif lexeme == ')':
                tokens.append(Token(lexeme, self.idx, TokenType.RParen))
            else:
                tokens.append(self.key_or_id())
            self.idx += 1

        return tokens
