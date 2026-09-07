from fleshpy.lexer import Lexer
from fleshpy.token import TokenType


def test_number():
    lexer = Lexer()

    tokens = lexer.lex("10")
    assert tokens[0].lexeme == "10"
    assert tokens[0].index == 0
    assert tokens[0].ty == TokenType.Integer


def test_number_float():
    lexer = Lexer()

    tokens = lexer.lex("10.01")
    assert tokens[0].lexeme == "10.01"
    assert tokens[0].index == 0
    assert tokens[0].ty == TokenType.Float


def test_keywords():
    lexer = Lexer()

    tokens = lexer.lex("if cond block let define lambda")
    assert tokens[0].ty == TokenType.If
    assert tokens[1].ty == TokenType.Cond
    assert tokens[2].ty == TokenType.Block
    assert tokens[3].ty == TokenType.Let
    assert tokens[4].ty == TokenType.Define
    assert tokens[5].ty == TokenType.Lambda


def test_symbols():
    lexer = Lexer()

    tokens = lexer.lex("()")
    assert tokens[0].ty == TokenType.LParen
    assert tokens[1].ty == TokenType.RParen


def test_string():
    lexer = Lexer()

    tokens = lexer.lex('"This is a string!" "\\"escaped\\""')
    assert tokens[0].ty == TokenType.String
    assert tokens[1].ty == TokenType.String
    assert tokens[1].lexeme == '"escaped"'


def test_program():
    lexer = Lexer()

    tokens = lexer.lex("(define variable (+ 1 1))")
    assert tokens[0].ty == TokenType.LParen
    assert tokens[1].ty == TokenType.Define
    assert tokens[2].ty == TokenType.ID
    assert tokens[3].ty == TokenType.LParen
    assert tokens[4].ty == TokenType.ID
    assert tokens[5].ty == TokenType.Integer
    assert tokens[6].ty == TokenType.Integer
    assert tokens[7].ty == TokenType.RParen
    assert tokens[8].ty == TokenType.RParen
