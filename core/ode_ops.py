import sympy as sp


def solve_ode(ode_str, func_str='y', var_str='x', ics=None):
    """
    Solve an ODE symbolically.

    Parameters:
        ode_str: The ODE equation string, e.g. "y'' + y = 0" or "Eq(y'', -y)"
        func_str: The dependent variable name (default 'y')
        var_str: The independent variable name (default 'x')
        ics: dict of initial conditions, e.g. {y(0): 1, y'(0): 0}

    Returns:
        The solution from dsolve.
    """
    x = sp.Symbol(var_str)
    y = sp.Function(func_str)(x)

    # Replace shorthand notation with SymPy derivatives
    expr_str = ode_str
    # Handle up to 4th order derivatives
    for i in range(4, 0, -1):
        prime_notation = func_str + "'" * i
        expr_str = expr_str.replace(prime_notation, f"Derivative({func_str}({var_str}), {var_str}, {i})")
    # Replace standalone function name (not already handled)
    # Avoid replacing inside Derivative(...)
    import re
    expr_str = re.sub(
        rf'(?<![\w(]){func_str}(?!\(|\')',
        f'{func_str}({var_str})',
        expr_str
    )

    local_dict = {
        var_str: x,
        func_str: sp.Function(func_str),
    }

    parsed = sp.sympify(expr_str, locals=local_dict)

    if isinstance(parsed, sp.Equality):
        eq = sp.Eq(parsed.lhs - parsed.rhs, 0)
    else:
        eq = sp.Eq(parsed, 0)

    # Parse initial conditions
    ic_dict = {}
    if ics:
        for cond_str, val_str in ics.items():
            cond_str = cond_str.strip()
            val = sp.sympify(val_str)
            # Parse y(0), y'(0), y''(0)...
            match = re.match(rf"({func_str})('+)?\((.+)\)", cond_str)
            if match:
                order = len(match.group(2)) if match.group(2) else 0
                point = sp.sympify(match.group(3))
                f = sp.Function(func_str)
                if order == 0:
                    ic_dict[f(point)] = val
                else:
                    ic_dict[f(x).diff(x, order).subs(x, point)] = val

    if ic_dict:
        solution = sp.dsolve(eq, y, ics=ic_dict)
    else:
        solution = sp.dsolve(eq, y)

    return solution
