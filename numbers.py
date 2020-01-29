from expressions import Polynomial


class NumInfinite(Polynomial):
    # Number is:
    # sum(coefs[i] * inf**(i+offset))

    # Ex:
    # @**2 - 5@ + 2
    # coefs: [1, -5, 2]
    # offset: -2

    # Ex:
    # 3@ - 15 + 7I
    # coefs: [3, -15, 7]
    # offset: -1

    # Ex:
    # 8I + 2I**2
    # coefs: [8, 2]
    # offset: 1
    
    def resolve(self):
        self.clean()
        degree = self.degree()
        if degree < 0:
            return 0
        elif degree > 0:
            if self.coefs[-1] < 0:
                return -float('inf')
            else:
                return float('inf')
        else:
            return self.coefs[-self.offset]
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
            if n < 0:
                out += '@'
            elif n > 0:
                out += 'I'
            if abs(n) > 1:
                out += '^' + str(abs(n))
        if len(out) == 0:
            out = '0'
        return out
    def __int__(self):
        return int(self.resolve())
    def __float__(self):
        return float(self.resolve())
