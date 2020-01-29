#import numpy
from expressions import *
from numbers import *

def derive_x(expr, x, give_partial = False):
    """evaluate f'(x) where f(x) = expr
    if give_partial == True then a NumInfinite will be given instead of a float"""
    # f'(x) = (f(x + @) - f(x)) * infinity

    a = NumInfinite('1@')
    inf = NumInfinite('1I')

    val = inf * (expr.evaluate(x=(a+x)) - expr.evaluate(x=x))

    if not give_partial:
        val = val.resolve()

    return val
def derive_f(expr, give_partial = False):

    left = expr.insert('x', Expression('x', '+', NumInfinite('1@')))
    if not give_partial:
        return ((left - expr) * NumInfinite('1I')).__float__()
    else:
        return (left - expr) * NumInfinite('1I')
