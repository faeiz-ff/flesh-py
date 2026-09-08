import fleshpy.ast as ast

from fleshpy.lexer import Lexer
from fleshpy.parser import Parser
from fleshpy.token import Token, TokenType


def get_tree(text: str) -> ast.Program:
    lexer = Lexer()
    parser = Parser()
    tokens = lexer.lex(text)
    return parser.parse(tokens)


def test_simple_define():
    program = get_tree("(define a 10)")
    definition = program.exprs[0]
    assert isinstance(definition, ast.Definition)

    assert definition.token.lexeme == "a"
    assert isinstance(definition.expr, ast.IntLiteral)

    assert definition.expr.token.lexeme == "10"


def test_lambda_define():
    program = get_tree("(define (id x) x)")

    definition = program.exprs[0]
    assert isinstance(definition, ast.Definition)
    assert definition.token.lexeme == "id"

    lambda_expr = definition.expr
    assert isinstance(lambda_expr, ast.Lambda)
    assert len(lambda_expr.params) == 1
    assert lambda_expr.params[0].lexeme == "x"


def test_lambda():
    program = get_tree("(lambda (x) x)")

    lambda_expr = program.exprs[0]
    assert isinstance(lambda_expr, ast.Lambda)
    assert len(lambda_expr.params) == 1
    assert lambda_expr.params[0].lexeme == "x"


def test_variadic():
    program = get_tree("(lambda xs (cdr xs))")

    lambda_expr = program.exprs[0]
    assert isinstance(lambda_expr, ast.Lambda)
    assert len(lambda_expr.params) == 1
    assert lambda_expr.params[0].lexeme == "xs"
    assert lambda_expr.variadic

    program = get_tree("(lambda (str . format) (display str format))")

    lambda_expr = program.exprs[0]
    assert isinstance(lambda_expr, ast.Lambda)
    assert len(lambda_expr.params) == 2
    assert lambda_expr.params[0].lexeme == "str"
    assert lambda_expr.params[1].lexeme == "format"
    assert lambda_expr.variadic

    program = get_tree("(define (f . xs) (+ (car xs) (f (cdr xs))))")

    definition = program.exprs[0]
    assert isinstance(definition, ast.Definition)

    lambda_expr = definition.expr
    assert isinstance(lambda_expr, ast.Lambda)
    assert len(lambda_expr.params) == 1
    assert lambda_expr.params[0].lexeme == "xs"
    assert lambda_expr.variadic


def test_if():
    program = get_tree("(if #t 1 0)")

    if_expr = program.exprs[0]
    assert isinstance(if_expr, ast.If)
    assert isinstance(if_expr.cond, ast.BooleanLiteral)
    assert isinstance(if_expr.then_expr, ast.IntLiteral)
    assert isinstance(if_expr.else_expr, ast.IntLiteral)


def test_cond():
    program = get_tree("(cond (a 1) (b 2) (else 3))")

    cond = program.exprs[0]
    assert isinstance(cond, ast.Cond)
    assert isinstance(cond.arms[0][0], ast.Identifier)
    assert isinstance(cond.arms[0][1], ast.IntLiteral)
    assert isinstance(cond.arms[1][0], ast.Identifier)
    assert isinstance(cond.arms[1][1], ast.IntLiteral)
    assert isinstance(cond.else_expr, ast.IntLiteral)


def test_begin():
    program = get_tree("(begin (set! a 1) a)")

    begin = program.exprs[0]
    assert isinstance(begin, ast.Begin)
    assert len(begin.expr_list) == 2
    assert isinstance(begin.expr_list[0], ast.Application)
    assert isinstance(begin.expr_list[1], ast.Identifier)


def test_let():
    program = get_tree("(let ((a 1) (b 2)) (+ a b))")

    let = program.exprs[0]
    assert isinstance(let, ast.Let)
    assert let.defs[0][0].lexeme == "a"
    assert isinstance(let.defs[0][1], ast.IntLiteral)
    assert let.defs[1][0].lexeme == "b"
    assert isinstance(let.defs[1][1], ast.IntLiteral)
    assert isinstance(let.body, ast.Begin)
    assert isinstance(let.body.expr_list[0], ast.Application)


