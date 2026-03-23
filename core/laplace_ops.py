import sympy as sp

t = sp.Symbol('t', positive=True)
s = sp.Symbol('s')


def laplace_transform(expr_str):
    """Compute Laplace transform of f(t)."""
    expr = sp.sympify(expr_str, locals={'t': t, 's': s})
    result = sp.laplace_transform(expr, t, s, noconds=True)
    return result


def inverse_laplace_transform(expr_str):
    """Compute inverse Laplace transform of F(s)."""
    expr = sp.sympify(expr_str, locals={'t': t, 's': s})
    result = sp.inverse_laplace_transform(expr, s, t)
    return result
