
from fleshpy.error import FleshRuntimeError
from inspect import signature
from typing import Callable, Dict, List, get_type_hints
from fleshpy.runtime.value import Boolean, BuiltInFunction, Float, Integer, String, Value, Nil


def flesh_function(*args: type):
    """
    Decorates a type-annotated python function into a valid Flesh function.

    The parameters of the 'func' function must be a subclass of T, and
    they all must be a concrete class.

    The decorated function will have the type of Callable[[List[T]], T],
    the arguments of the decorated function will then be type-checked at
    runtime with isinstance().
    """

    def wrapper[T](func: Callable[..., T]) -> BuiltInFunction[T]:
        params: List[type | None] = list(args)

        if len(params) == 0:
            sig = signature(func)
            type_hint = get_type_hints(func)

            def get_type(key: str) -> type:
                res = type_hint.get(key)
                if res is None:
                    raise FleshRuntimeError(
                        "No type annotations exist for '" + key +
                        "' parameter, cannot typecheck at runtime."
                    )
                return res

            params = list(map(get_type, sig.parameters.keys()))

        def inner(args: List[T]) -> T:
            if len(args) != len(params):
                raise FleshRuntimeError(
                    "Arity mismatch, expected " +
                    str(len(params)) +
                    " got " + str(len(args))
                )

            for i, (arg, param_type) in enumerate(zip(args, params)):
                assert param_type is not None

                if not isinstance(arg, param_type):
                    raise FleshRuntimeError(
                        "Mismatched type arguments at index " + str(i) +
                        ", expected '" + param_type.__name__ +
                        "' type, got '" + arg.__class__.__name__ + "' type"
                    )

            return func(*args)

        return BuiltInFunction(inner)
    return wrapper


@flesh_function()
def gt(a: Integer | Float, b: Integer | Float) -> Value:
    return Boolean(a.data > b.data)


@flesh_function()
def lt(a: Integer | Float, b: Integer | Float) -> Value:
    return Boolean(a.data < b.data)


@flesh_function()
def plus(a: Integer | Float | String, b: Integer | Float | String) -> Value:
    if isinstance(a, String) and isinstance(b, String):
        return a.__add__(b)
    elif isinstance(a, String) or isinstance(b, String):
        return Nil()
    return a + b


@flesh_function()
def mult(a: Integer | Float, b: Integer | Float) -> Value:
    return a * b


@flesh_function()
def minus(a: Integer | Float, b: Integer | Float) -> Value:
    return a - b


@flesh_function()
def display(a: Value) -> Value:
    print(a)
    return Nil()

default_flesh_functions: Dict[str, Value] = {
    ">": gt,
    "<": lt,
    "+": plus,
    "*": mult,
    "-": minus,
    "display": display,
}
