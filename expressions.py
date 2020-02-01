
def is_num(x):
    if type(x) in [int, float]:
        return True
    if hasattr(x, '__int__') and hasattr(x, '__float__'):
        return True
    return False

class Polynomial:
    def __init__(self, q = 0):
        if type(q) in [float, int]:
            self.offset = 0
            self.coefs = [q]
        elif type(q) == tuple:
            self.offset = q[0]
            self.coefs = q[1].copy()
            self.clean()
        elif type(q) == self.__class__:
            self.offset = q.offset
            self.coefs = q.coefs.copy()
            self.clean()
        assert hasattr(self, 'coefs')
        assert hasattr(self, 'offset')
    def clean(self):
        # remove uneeded coefficients
        while self.coefs[-1] == 0:
            if len(self.coefs) == 1:
                return
            self.coefs.pop()
        while self.coefs[0] == 0:
            if len(self.coefs) == 1:
                return
            self.coefs.pop(0)
            self.offset += 1
    def copy(self):
        return self.__class__(self)
    def degree(self):
        return self.offset + len(self.coefs) - 1
    def resolve(self, x):
        res = 0
        for i in range(len(self.coefs)):
            res += (x**(i + self.offset)) * self.coefs[i]
        return res
    def __str__(self):
        out = ''
        for n in range(self.offset, self.degree() + 1):
            i = n - self.offset
            if self.coefs[i] == 0:
                continue
            if len(out) > 0:
                if self.coefs[i] < 0:
                    out += ' - '
                else:
                    out += ' + '
            elif self.coefs[i] < 0:
                out += '-'
            if n == 0 or abs(self.coefs[i]) != 1:
                out += str(round(abs(self.coefs[i]), 3))
            if n != 0:
                out += 'x'
                if n != 1:
                    out += '^' + str(n)
        if len(out) == 0:
            out = '0'
        return out
    def __add__(self, other):
        degree = self.degree()
        coefs = self.coefs.copy()
        offset = self.offset
        if type(other) in [int, float]:
            if offset > 0:
                coefs = [other] + [0] * (self.offset - 1) + coefs
                offset = 0
            elif degree < 0:
                coefs += (-1 - degree) * [0] + [other]
            else:
                coefs[-self.offset] += other
        elif isinstance(other, Polynomial):
            ioff = other.offset
            icoef = other.coefs
            if offset > ioff:
                coefs = (offset - ioff) * [0] + coefs
                offset = ioff
            elif offset < ioff:
                icoef = (ioff - offset) * [0] + icoef
                ioff = offset
            diff = len(icoef) - len(coefs)
            if diff > 0:
                coefs += [0] * diff
            elif diff < 0:
                icoef += [0] * -diff
            for i in range(len(coefs)):
                coefs[i] += icoef[i]
        else:
            raise TypeError(other)
        return self.__class__((offset, coefs))
    def __sub__(self, other):
        return self.__add__(-other)
    def __mul__(self, other):
        coefs = self.coefs.copy()
        offset = self.offset
        if type(other) in [int, float]:
            for i in range(len(coefs)):
                coefs[i] *= other
        elif isinstance(other, Polynomial):
            offset = other.offset + offset
            coefs = [0] * (len(self.coefs) + len(other.coefs) - 1)
            for i in range(len(self.coefs)):
                for j in range(len(other.coefs)):
                    coefs[i + j] += self.coefs[i] * other.coefs[j]
        else:
            raise TypeError(other)
        return self.__class__((offset, coefs))
    def __truediv__(self, other):
        coefs = self.coefs.copy()
        offset = self.offset
        if type(other) in [int, float]:
            for i in range(len(coefs)):
                coefs[i] = coefs[i] / other
            # TODO: divide by polynomials
            '''elif isinstance(other, Polynomial):
                offset = other.offset + offset
                coefs = [0] * (len(self.coefs) + len(other.coefs) - 1)
                for i in range(len(self.coefs)):
                    for j in range(len(other.coefs)):
                        coefs[i + j] += self.coefs[i] * other.coefs[j]'''
        else:
            raise TypeError(other)
        return self.__class__((offset, coefs))
    def __neg__(self):
        coefs = self.coefs.copy()
        offset = self.offset
        for i in range(len(coefs)):
            coefs[i] *= -1
        return self.__class__((offset, coefs))
    def __radd__(self, other):
        return self.__add__(other)
    def __rsub__(self, other):
        return (-self).__add__(other)
    def __rmul__(self, other):
        return self.__mul__(other)
    def __pow__(self, other):
        out = self.copy()
        for i in range(other - 1):
            out *= self
        return out


class Expression:
    def _load_real_val(val, kwargs):
        if isinstance(val, Expression):
            return val.evaluate(**kwargs)
        elif type(val) == str:
            return kwargs[val]
        # TODO: good polynomial support
        #elif type(self.a) == tuple:
        #    a = self.a.resolve(
        else:
            return val
    def __init__(self, a, op, b = None):
        self.a = a
        self.op = op
        self.b = b
    def evaluate(self, **kwargs):
        a = Expression._load_real_val(self.a, kwargs)
        if self.b != None:
            b = Expression._load_real_val(self.b, kwargs)

        op = self.op

        if op == '+':
            return a + b
        elif op == '-':
            if self.b != None:
                return a - b
            else:
                return -a
        elif op == '*':
            return a * b
        elif op == '/':
            return a / b
        elif op == '//':
            return a // b
        elif op == '^':
            return a ** b
        elif op == 'floor' or op == 'int':
            return int(a)
        elif op == 'float':
            return float(a)
        elif op == 'literal':
            return a
        else:
            raise Exception("Invalid operator encounterd in Expression.eval()")
    def insert(self, var, val):
        a = self.a
        if a == var:
            a = val
        elif isinstance(a, Expression):
            a = a.insert(var, val)
        b = self.b
        if b == var:
            b = val
        elif isinstance(b, Expression):
            b = b.insert(var, val)
        if a != self.a or b != self.b:
            return Expression(a, self.op, b)
        else:
            return self
    def copy(self):
        'Deep copy of this object'
        a = self.a
        if hasattr(a, 'copy'):
            a = a.copy()
        b = self.b
        if hasattr(b, 'copy'):
            b = b.copy()
        return self.__class__(a, self.op, b)
    def __add__(self, b):
        if isinstance(b, Expression):
            return Sum([self, b], 0)
        else:
            return Sum([self], b)
    def __radd__(self, b):
        if isinstance(b, Expression):
            return Sum([self, b], 0)
        else:
            return Sum([self], b)
    def __sub__(self, b):
        if isinstance(b, Expression):
            return Sum([self, -b], 0)
        else:
            return Sum([self], -b)
    def __rsub__(self, b):
        if isinstance(b, Expression):
            return -Sum([self, -b], 0)
        else:
            return -Sum([self], -b)
    def __mul__(self, b):
        return Expression(self, '*', b)
    def __rmul__(self, b):
        return Expression(b, '*', self)
    def __truediv__(self, b):
        return Expression(self, '/', b)
    def __rtruediv__(self, b):
        return Expression(b, '/', self)
    def __floordiv__(self, b):
        return Expression(self, '//', b)
    def __rfloordiv__(self, b):
        return Expression(b, '//', self)
    def __pow__(self, b):
        return Expression(self, '^', b)
    def __rpow__(self, b):
        return Expression(b, '^', self)
    def __neg__(self):
        return Expression(self, '-')
    def floor(self):
        return Expression(self, 'floor')
    def castfloat(self):
        return Expression(self, 'float')
    def __eq__(self, other):
        if type(other) != self.__class__:
            return False
        return (self.a == other.a and
                self.b == other.b and
                self.op == other.op)
    def __str__(self):
        if self.b == None:
            if self.op == 'literal':
                return str(self.a)
            return self.op + str(self.a)
        else:
            return '(' + str(self.a) + self.op + str(self.b) + ')'
    def simplify(self, gen_num = False):
        a = self.a
        b = self.b
        if isinstance(a, Expression):
            a = a.simplify(True)
        if isinstance(b, Expression):
            b = b.simplify(True)
        if is_num(a) and is_num(b):
            if gen_num:
                return self.evaluate()
            else:
                return Expression(self.evaluate(), 'literal')

        # a and b are fully simplified at this point

        if self.op == '^':
            # Power rules
            if b == 0:
                if gen_num:
                    return 1
                else:
                    return Expression(1, 'literal')
            elif b == 1:
                if gen_num or not is_num(b):
                    return b
                else:
                    return Expression(b, 'literal')
            elif type(b) == int and (is_num(a) or isinstance(a, Expression)):
                # can only roll out if int is power
                # roll it out for further simplification
                expr = a
                for i in range(b - 1):
                    expr *= a
                expr2 = expr.simplify()
                if expr2 != expr:
                    # only return the expression if it's more simple then what we have now
                    return expr2
        elif self.op == '*':
            # Multiplication rules
            if b == 0 or a == 0:
                if gen_num:
                    return 0
                else:
                    return Expression(0, 'literal')
            elif b == 1:
                if gen_num or not is_num(a):
                    return a
                else:
                    return Expression(a, 'literal')
            elif a == 1:
                if gen_num or not is_num(b):
                    return b
                else:
                    return Expression(b, 'literal')
            # try a complex multiplication of everything, then attempt simplification
            # we know that at least a or b is an expression with a variable because constants
            # have already been simplified.
            
        elif self.op == '+':
            # Addition rules
            if b == 1:
                if gen_num or not is_num(a):
                    return a
                else:
                    return Expression(a, 'literal')
            elif a == 1:
                if gen_num or not is_num(b):
                    return b
                else:
                    return Expression(b, 'literal')
        elif self.op == '-':
            # Subtraction rules
            if b == 1:
                if gen_num or not is_num(a):
                    return a
                else:
                    return Expression(a, 'literal')
            elif a == 1:
                if gen_num or not is_num(b):
                    return b
                else:
                    return Expression(b, 'literal')
        elif self.op == '/':
            # Division rules
            if a == 0:
                if gen_num:
                    return 0
                else:
                    return Expression(0, 'literal')
            elif b == 1:
                if gen_num or not is_num(a):
                    return a
                else:
                    return Expression(a, 'literal')

        
        # Generate final output
        if a != self.a or b != self.b:
            return Expression(a, self.op, b)
        else:
            return self
class Sum(Expression):
    def __init__(self, items, const = 0):
        self.items = items.copy()
        self.const = const
    def resolve(self, **kwargs):
        total = 0
        for i in self.items:
            if isinstance(i, Expression):
                total += i.resolve()
            else:
                total += i
        return total
    def __add__(self, b):
        if isinstance(b, Expression):
            return Sum(self.items + [b], self.const)
        else:
            return Sum(self.items, self.const + b)
    def __radd__(self, b):
        if isinstance(b, Expression):
            return Sum(self.items + [b], self.const)
        else:
            return Sum(self.items, self.const + b)
    def __sub__(self, b):
        if isinstance(b, Expression):
            return Sum(self.items + [-b], self.const)
        else:
            return Sum(self.items, self.const - b)
    def __rsub__(self, b):
        if isinstance(b, Expression):
            return -Sum(self.items + [-b], self.const)
        else:
            return -Sum(self.items, self.const - b)
    def __neg__(self):
        return Expression(self, '-')
    def __eq__(self, other):
        if type(other) != self.__class__:
            return False
        if self.const != other.const:
            return False
        if len(self.items) != other.items:
            return False
        for i in range(len(self.items)):
            if self.items[i] != other.items[i]:
                return False
        return True
    def __str__(self):
        s = '('
        for i in self.items:
            s += str(i) + ' + '
        return s + str(self.const) + ')'
    def simplify(self, gen_num = False):
        const = self.const
        items = []
        for i in self.items:
            if isinstance(i, Expression):
                i = i.simplify(True)
            if is_num(i):
                const += i
            else:
                items.append(i)
        if len(items) == 0:
            if gen_num:
                return const
            else:
                return Expression(const, 'literal')
        else:
            return Sum(items, const)
    
