from . import expressions as ex
from . import calculus as calc
from . import mnumbers as num

def test_is_num():
    assert ex.is_num(2)
    assert ex.is_num(float('inf'))
    assert ex.is_num(num.NumInfinite('1@'))
    assert not ex.is_num(ex.Polynomial((0,[1,8,2,1])))
    assert not ex.is_num(ex.Expression('x', '*', 2))

def test_Polynomial():
    poly = ex.Polynomial((0, [1,-2,1]))

    assert poly.degree() == 2
    assert poly.resolve(0) == 1
    assert poly.resolve(1) == 0
    assert str(poly) == "1 - 2x + x^2"
    assert (poly + 2).resolve(0) == 3
    assert (poly * 2).resolve(0) == 2
    assert (poly ** 2).resolve(3) == 16
    
def test_Expression():
    expr = ex.Expression('x', '*', 'y')

    assert expr.evaluate(x=2,y=3) == 6
    ex2 = expr.insert('x', 2).insert('y', 4)
    assert ex2.evaluate(x=-1,y=22) == 8 # should no longer be based on variables
    assert str(ex2.simplify()) == '8'

    ex3 = ((expr + 2) * 88) ** .5
    ex3//=3
    ex3 = 2 * ex3

    ex3.simplify()

    assert type(ex3 + ex.Expression('x', '-')) == ex.Sum

def test_Sum():
    s = ex.Sum([3,2,1], 22)
    s += ex.Expression('x', '/', 2)
    assert str(s.simplify()) == '((x/2) + 28)'
    assert str(2**s) == '(2^(3 + 2 + 1 + (x/2) + 22))'
    s**=2
    s+=2
    s += ex.Expression('x','^', 2)
    assert str(s) == '(((3 + 2 + 1 + (x/2) + 22)^2) + (x^2) + 2)'
    ss = s.simplify()
    assert str(ss) == '((((x/2) + 28)^2) + (x^2) + 2)'
    
    assert s != ss
    assert s == ex.Sum(s.items, s.const)
