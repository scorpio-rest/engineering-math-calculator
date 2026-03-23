import sympy as sp

x = sp.Symbol('x')


def differentiate(expr_str, var_str='x', order=1):
    var = sp.Symbol(var_str)
    expr = sp.sympify(expr_str)
    result = sp.diff(expr, var, order)
    return result


def integrate_indefinite(expr_str, var_str='x'):
    var = sp.Symbol(var_str)
    expr = sp.sympify(expr_str)
    result = sp.integrate(expr, var)
    return result


def integrate_definite(expr_str, var_str='x', lower=None, upper=None):
    var = sp.Symbol(var_str)
    expr = sp.sympify(expr_str)
    a = sp.sympify(lower)
    b = sp.sympify(upper)
    result = sp.integrate(expr, (var, a, b))
    return result


def limit(expr_str, var_str='x', point_str='0', direction=''):
    var = sp.Symbol(var_str)
    expr = sp.sympify(expr_str)
    point = sp.sympify(point_str)
    if direction in ('+', '-'):
        result = sp.limit(expr, var, point, direction)
    else:
        result = sp.limit(expr, var, point)
    return result


def taylor_expand(expr_str, var_str='x', point_str='0', order=5):
    var = sp.Symbol(var_str)
    expr = sp.sympify(expr_str)
    point = sp.sympify(point_str)
    result = sp.series(expr, var, point, order + 1).removeO()
    return result
