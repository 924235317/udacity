from decimal import Decimal, getcontext
from math import sqrt, acos, pi
from vector import Vector

getcontext().prec = 5


class Line(object):

    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    def __init__(self, normal_vector=None, constant_term=None):
        self.dimension = 2

        if not normal_vector:
            all_zeros = ['0']*self.dimension
            normal_vector = Vector(all_zeros)
        self.normal_vector = normal_vector

        if not constant_term:
            constant_term = Decimal('0')
        self.constant_term = Decimal(constant_term)

        self.set_basepoint()
    #--------------intersection--------------------
    def is_parallel_to(self, l):
        n0 = self.normal_vector
        n1 = l.normal_vector
        return n0.is_parallel_to(n1)

    def intersection_with(self, l):
        try:
            a, b = self.normal_vector.coordinates
            c, d = l.normal_vector.coordinates
            k1, k2 = self.constant_term, l.constant_term

            # bug decimal.InvalidOperation: 0 / 0
            # x = (k1*d - k2*b) / (a*d - b*c)
            # y = (k1*c - k2*a) / (b*c - a*d)
            x_numerator = k1*d - k2*b
            y_numerator = k2*a - k1*c
            one_over_demon = Decimal('1.0') / (a*d - b*c)

            return Vector([x_numerator, y_numerator]).times_scalar(one_over_demon)

        except ZeroDivisionError:
            if self == l:
                return self
            else:
                return None

    def __eq__(self, l):
        if self.normal_vector.is_zero():
            if not l.normal_vector.is_zero():
                return False
            else:
                diff = self.constant_term - l.constant_term
                return MyDecimal(diff).is_near_zero()
        elif l.normal_vector.is_zero():
            return False

        if not self.is_parallel_to(l):
            return False

        n0 = self.basepoint
        n1 = l.basepoint
        basepoint_difference = n0.minus(n1)
        return self.normal_vector.is_orthogonal_to(basepoint_difference)

    def set_basepoint(self):
        try:
            n = self.normal_vector.coordinates#bug
            c = self.constant_term
            basepoint_coords = ['0']*self.dimension

            initial_index = Line.first_nonzero_index(n)
            initial_coefficient = n[initial_index]

            basepoint_coords[initial_index] = c/initial_coefficient
            self.basepoint = Vector(basepoint_coords)

        except Exception as e:
            if str(e) == Line.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None
            else:
                raise e



    def __str__(self):

        num_decimal_places = 3

        def write_coefficient(coefficient, is_initial_term=False):
            coefficient = round(coefficient, num_decimal_places)
            if coefficient % 1 == 0:
                coefficient = int(coefficient)

            output = ''

            if coefficient < 0:
                output += '-'
            if coefficient > 0 and not is_initial_term:
                output += '+'

            if not is_initial_term:
                output += ' '

            if abs(coefficient) != 1:
                output += '{}'.format(abs(coefficient))

            return output

        n = self.normal_vector.coordinates#bug

        try:
            initial_index = Line.first_nonzero_index(n)
            terms = [write_coefficient(n[i], is_initial_term=(i==initial_index)) + 'x_{}'.format(i+1)
                     for i in range(self.dimension) if round(n[i], num_decimal_places) != 0]
            output = ' '.join(terms)

        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'
            else:
                raise e

        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)

        return output


    @staticmethod
    def first_nonzero_index(iterable):
        for k, item in enumerate(iterable):
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Line.NO_NONZERO_ELTS_FOUND_MSG)


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps


if __name__ == "__main__":
    n1 = Vector([1.182, 5.562])
    n2 = Vector([1.773, 8.343])
    c1 = 6.744
    c2 = 9.525
    line1 = Line(n1, c1)
    line2 = Line(n2, c2)
    print("equal? ", line1 == line2)
    print("parallel? ", line1.is_parallel_to(line2))

    print line1.intersection_with(line2)
    #print(acos(1.00000001000))