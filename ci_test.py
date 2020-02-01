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
    
