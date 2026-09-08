# Flesh Script: Faeiz's Lisp Expression SHell Script in python

It's not really a shell, but well, if i had the time i would make it into an actual shell.
But for now, its really just a scripting language for my portofolio thingy.

flesh is a kind of lisp, its inspired by Scheme (probably almost a subset of it), but i'm not really following the Scheme specification that much.

Flesh doesnt dictate anything in its runtime: how it stores values, what are the truthyness of values, even the implementation of `cons`, `car`, `list`, even `+` operator is not defined. The plan is, you can integrate this into anything and hook it up to your environment. For now, flesh only dictates the grammar, and these special forms. (Grammar spec is TODO)

## Language capabilities

### Primitives

theres 5 main primitives: Int, Float, String, Boolean, Nil

```flesh
1       ; Int
1.2     ; Float
"abc"   ; String
#t, #f  ; Boolean
nil, () ; Nil
```
It can lex these and make their corresponding AST, but theres no dictating whats the truthyness of each values.

### Definitions

with the `define` keyword, it creates a Definition AST.

```flesh
(define num 10)
(define name "zie")
```

### Application

Its a fancy word for function call. To call a function wrap it in parentheses.

```flesh
(func-name arg0 arg1 arg2)
(+ 1 2 3) ; invokes the + function with the argument 1 2 3, returns 6 assumedly
```

### Lambdas

The good 'ol lambda, cant not have them in a functional language can we?

```flesh
(lambda (x) x)    ; this is a lambda expression
(define (id x) x) ; this is a named function

(define id (lambda (x) x)) ; this is equivalent to the named function
```

It can also have variadics, how these collection is implemented is not dictated

```flesh
; these two are equivalent
(define (sum . xs) (summer (flat xs)))
(define sum (lambda xs (summer (flat xs))))

(sum 1 2 3) ; xs is a collection of int 1 2 3

; multiple params before variadic
(define (f x y . zs))
(define f (lambda (x y . zs)))

(f 1 2 3 4) ; x = 1, y = 2, zs = 3 4

(define (f x . y z)) ; error, variadic can only be 1

(define (pipe x . fs)
    (define (recurse x fs)
        (if (nil? fs) 
            x
            (recurse ((car fs) x) (cdr fs))))
    (recurse x fs))
```

### Begin

Flesh is could be a purely functional language, could be not. So theres a `begin` expression, which computes a series of expressions but only returns the last one.

```flesh
(begin (set! a 10) (+ a a))
```

of course, `set!` function is undefined, its up to the extender.

By default, any functions, lambda or named, will automatically have `begin` as its function body.

```flesh
(define (one) 1)
; is actually
(define one (lambda () (begin 1)))
```

### Conditionals

Flesh has these special forms as conditionals

```flesh
(if condition then-expr else-expr)

(cond (condition-1 then-expr-1)
      (condition-2 then-expr-2)
      (condition-n then-expr-n) ; can be extended into n conditions
      (else else-expr))         ; optional else catchall
```

### Let

For defining local variables, theres `let` expression

```flesh
(let ((local-var-1 expr-1)
      (local-var-2 expr-2))
      expr)
```

### Thats it...
