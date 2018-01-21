from decimal import Decimal, getcontext
from copy import deepcopy

from vector import Vector
from plane import Plane


getcontext().prec = 30


class LinearSystem(object):

    ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG = 'All planes in the system should live in the same dimension'
    NO_SOLUTIONS_MSG = 'No solutions'
    INF_SOLUTIONS_MSG = 'Infinitely many solutions'
    CAN_MSG = 'cant msg'
    OUT_OF_RANGE_MSG = 'Out of range'

    def __init__(self, planes):
        try:
            d = planes[0].dimension
            for p in planes:
                assert p.dimension == d

            self.planes = planes
            self.dimension = d
            self.num_of_planes = len(planes)

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)

    # --------------row--------------------
    def swap_rows(self, row1, row2):
        try:
            self.planes[row1], self.planes[row2] = self.planes[row2], self.planes[row1]
        except IndexError:
            raise Exception(self.OUT_OF_RANGE_MSG)

    def multiply_coefficient_and_row(self, coefficient, row):
        try:
            assert coefficient != 0
            line_normal_vector = self[row].normal_vector.times_scalar(Decimal(str(coefficient)))
            line_constant_term = self[row].constant_term * MyDecimal(str(coefficient))
            self.planes[row] = Plane(line_normal_vector, line_constant_term)
        except AssertionError:
            raise Exception(self.CANT_MSG)

    def add_multiple_times_row_to_row(self, coefficient, row_to_add, row_to_be_added_to):
        v = self[row_to_add].normal_vector.times_scalar(str(coefficient))
        c = self[row_to_add].constant_term * MyDecimal(str(coefficient))
        line_normal_vector = self.planes[row_to_be_added_to].normal_vector.plus(v)
        line_constant_term = self.planes[row_to_be_added_to].constant_term + c
        self.planes[row_to_be_added_to] = Plane(line_normal_vector, line_constant_term)

    # -------------- my triangle form--------------------
    # def compute_triangular_form(self):
    #     system = deepcopy(self)
    #
    #     #swap the first plane which the first coefficient of variables to top
    #     indices = system.indices_of_first_nonzero_terms_in_each_row()
    #     idx = 0
    #     while idx < len(indices):
    #         if indices[idx] == 0:
    #             if idx == 0:
    #                 break
    #             else:
    #                 system.swap_rows(0, idx)
    #                 break
    #         idx += 1
    #
    #     #
    #     dimension = min(system.num_of_planes, system.planes[0].dimension)
    #     #print system.dimension, system.planes[0].dimension, dimension
    #     for idx in range(0, dimension - 1):
    #         n = system.planes[idx].normal_vector.coordinates
    #         for i in range(idx+1, system.num_of_planes):
    #             #print i
    #             n1 = system.planes[i].normal_vector.coordinates
    #             #print n1
    #             if n1[idx] == 0:
    #
    #                 continue
    #             else:
    #                 coefficient = -n1[idx] / n[idx]
    #                 system.add_multiple_times_row_to_row(coefficient, idx, i)
    #
    #     #clear some no-used planes
    #     #print dimension, system.num_of_planes
    #     if dimension < system.num_of_planes:
    #         for i in range(dimension, system.num_of_planes):
    #             #print i
    #             system.planes[i] = Plane()
    #             #print system.planes[i]
    #
    #     return system

    #-----------------triangle form-----------------------
    def compute_triangular_form(self):
        system = deepcopy(self)

        num_equations = len(system)
        num_variables = system.dimension

        j = 0
        for i in range(num_equations):
            while j < num_variables:
                c = MyDecimal(system[i].normal_vector[j])
                #print c
                if c.is_zero():
                    swap_succeeded = system.swap_with_row_below_for_nonezero_coefficient_is_able(i, j)
                    if not swap_succeeded:
                        j += 1
                        continue
                system.clear_coefficients_below(i, j)
                j += 1
                break

        return system

    def clear_coefficients_below(self, row, col):
        num_equations = len(self)
        beta = MyDecimal(self[row].normal_vector[col])

        for k in range(row+1, num_equations):
            n = self[k].normal_vector
            gamma = n[col]
            alpha = -gamma/beta
            self.add_multiple_times_row_to_row(alpha, row, k)

    def swap_with_row_below_for_nonezero_coefficient_is_able(self, row, col):
        num_equations = len(self)

        for k in range(row + 1, num_equations):
            coefficient = MyDecimal(self[k].normal_vector[col])
            if not coefficient.is_zero():
                self.swap_rows(row, k)
                return True

        return False

    #----------------compute rref--------------------------
    def compute_rref(self):
        tf = self.compute_triangular_form()

        num_equations = len(tf)
        pivot_indices = tf.indices_of_first_nonzero_terms_in_each_row()

        for i in range(num_equations)[::-1]:
            j = pivot_indices[i]
            if j < 0:
                continue
            tf.scale_row_to_make_coefficient_equal_one(i, j)
            tf.clear_coefficients_above(i, j)

        return tf

    def scale_row_to_make_coefficient_equal_one(self, row, col):
        n = self[row].normal_vector
        #print n[col]
        beta = Decimal('1.0') / n[col]
        #print "bata = ", beta
        self.multiply_coefficient_and_row(beta, row)

    def clear_coefficients_above(self, row, col):
        for k in range(row)[::-1]:
            n = self[k].normal_vector
            alpha = -(n[col])
            self.add_multiple_times_row_to_row(alpha, row, k)

    #------------------compute solution-----------------
    def compute_solution(self):
        try:
            self.do_gaussian_elimination_and_extract_solution()

        except Exception as e:
            if (str(e) == self.NO_SOLUTIONS_MSG or
                        str(e) == self.INF_SOLUTIONS_MSG):
                return str(e)
            else:
                raise e

    def do_gaussian_elimination_and_extract_solution(self):
        rref = self.compute_rref()
        #print rref

        rref.raise_exception_if_contradictory_equation()
        rref.raise_exception_if_too_few_pivots()

        num_variables = rref.dimension
        #print rref
        solution_coordinates = [rref.planes[i].constant_term for i in
                                range(num_variables)]

        return Vector(solution_coordinates)

    def raise_exception_if_contradictory_equation(self):
        for p in self.planes:
            try:
                p.first_nonzero_index(p.normal_vector)

            except Exception as e:
                if str(e) == 'No nonzero elements found':

                    constant_term = MyDecimal(p.constant_term)
                    print "plane:", p, " constant_term: ", p.constant_term
                    print type(p.constant_term)
                    if not constant_term.is_zero():
                        raise Exception(self.NO_SOLUTIONS_MSG)
                else:
                    raise e

    def raise_exception_if_too_few_pivots(self):
        pivot_indices = self.indices_of_first_nonzero_terms_in_each_row()
        num_pivots = sum([1 if index >= 0 else 0 for index in pivot_indices])
        num_variables = self.dimension

        if num_pivots < num_variables:
            raise Exception(self.NO_SOLUTIONS_MSG)

    def indices_of_first_nonzero_terms_in_each_row(self):
        num_equations = len(self)
        num_variables = self.dimension

        indices = [-1] * num_equations

        for i, p in enumerate(self.planes):
            try:
                indices[i] = p.first_nonzero_index(p.normal_vector.coordinates)#bug
            except Exception as e:
                if str(e) == Plane.NO_NONZERO_ELTS_FOUND_MSG:
                    continue
                else:
                    raise e

        return indices


    def __len__(self):
        return len(self.planes)


    def __getitem__(self, i):
        return self.planes[i]


    def __setitem__(self, i, x):
        try:
            assert x.dimension == self.dimension
            self.planes[i] = x

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)


    def __str__(self):
        ret = 'Linear System:\n'
        temp = ['Equation {}: {}'.format(i+1, p) for i, p in enumerate(self.planes)]
        ret += '\n'.join(temp)
        return ret


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps

def _test():
    p0 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
    p1 = Plane(normal_vector=Vector(['0', '1', '0']), constant_term='2')
    p2 = Plane(normal_vector=Vector(['1', '1', '-1']), constant_term='3')
    p3 = Plane(normal_vector=Vector(['1', '0', '-2']), constant_term='2')

    s = LinearSystem([p0,p1,p2,p3])
    # #s.swap_rows(2, 1)
    # s.multiply_coefficient_and_row(0.1, 0)
    # s.add_multiple_times_row_to_row(2, 0, 1)

    # print s.indices_of_first_nonzero_terms_in_each_row()
    # print '{},{},{},{}'.format(s[0],s[1],s[2],s[3])
    # print len(s)
    # print s

    s[0] = p1
    print s

    print MyDecimal('1e-9').is_near_zero()
    print MyDecimal('1e-11').is_near_zero()

def row_test():
    p0 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
    p1 = Plane(normal_vector=Vector(['0', '1', '0']), constant_term='2')
    p2 = Plane(normal_vector=Vector(['1', '1', '-1']), constant_term='3')
    p3 = Plane(normal_vector=Vector(['1', '0', '-2']), constant_term='2')

    s = LinearSystem([p0, p1, p2, p3])
    s.swap_rows(0, 1)
    # print s
    # print s[0] == p1
    # print s[1] == p0
    # print p0.normal_vector.angle_with(s[1].normal_vector)
    # print s[1].normal_vector
    # print p0.normal_vector
    if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
        print 'test case 1 failed'

    s.swap_rows(1, 3)
    if not (s[0] == p1 and s[1] == p3 and s[2] == p2 and s[3] == p0):
        print 'test case 2 failed'

    s.swap_rows(3, 1)
    if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
        print 'test case 3 failed'

    s.multiply_coefficient_and_row(1, 0)
    if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
        print 'test case 4 failed'

    s.multiply_coefficient_and_row(-1, 2)
    if not (s[0] == p1 and
                    s[1] == p0 and
                    s[2] == Plane(normal_vector=Vector(['-1', '-1', '1']), constant_term='-3') and
                    s[3] == p3):
        print 'test case 5 failed'

    s.multiply_coefficient_and_row(10, 1)
    if not (s[0] == p1 and
                    s[1] == Plane(normal_vector=Vector(['10', '10', '10']), constant_term='10') and
                    s[2] == Plane(normal_vector=Vector(['-1', '-1', '1']), constant_term='-3') and
                    s[3] == p3):
        print 'test case 6 failed'

    s.add_multiple_times_row_to_row(0, 0, 1)
    if not (s[0] == p1 and
                    s[1] == Plane(normal_vector=Vector(['10', '10', '10']), constant_term='10') and
                    s[2] == Plane(normal_vector=Vector(['-1', '-1', '1']), constant_term='-3') and
                    s[3] == p3):
        print 'test case 7 failed'

    s.add_multiple_times_row_to_row(1, 0, 1)
    if not (s[0] == p1 and
                    s[1] == Plane(normal_vector=Vector(['10', '11', '10']), constant_term='12') and
                    s[2] == Plane(normal_vector=Vector(['-1', '-1', '1']), constant_term='-3') and
                    s[3] == p3):
        print 'test case 8 failed'

    s.add_multiple_times_row_to_row(-1, 1, 0)
    if not (s[0] == Plane(normal_vector=Vector(['-10', '-10', '-10']), constant_term='-10') and
                    s[1] == Plane(normal_vector=Vector(['10', '11', '10']), constant_term='12') and
                    s[2] == Plane(normal_vector=Vector(['-1', '-1', '1']), constant_term='-3') and
                    s[3] == p3):
        print 'test case 9 failed'

def triangle_form_test():
    p1 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
    p2 = Plane(normal_vector=Vector(['0', '1', '1']), constant_term='2')
    s = LinearSystem([p1, p2])
    t = s.compute_triangular_form()
    print t
    if not (t[0] == p1 and
            t[1] == p2):
        print 'test case 1 failed'

    p1 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
    p2 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='2')
    s = LinearSystem([p1, p2])
    t = s.compute_triangular_form()
    print t
    if not (t[0] == p1 and
            t[1] == Plane(constant_term='1')):
        print 'test case 2 failed'

    p1 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
    p2 = Plane(normal_vector=Vector(['0', '1', '0']), constant_term='2')
    p3 = Plane(normal_vector=Vector(['1', '1', '-1']), constant_term='3')
    p4 = Plane(normal_vector=Vector(['1', '0', '-2']), constant_term='2')
    s = LinearSystem([p1, p2, p3, p4])
    t = s.compute_triangular_form()
    if not (t[0] == p1 and
            t[1] == p2 and
            t[2] == Plane(normal_vector=Vector(['0', '0', '-2']), constant_term='2') and
            t[3] == Plane()):
        print 'test case 3 failed'

    p1 = Plane(normal_vector=Vector(['0', '1', '1']), constant_term='1')
    p2 = Plane(normal_vector=Vector(['1', '-1', '1']), constant_term='2')
    p3 = Plane(normal_vector=Vector(['1', '2', '-5']), constant_term='3')
    s = LinearSystem([p1, p2, p3])
    t = s.compute_triangular_form()
    print t
    if not (t[0] == Plane(normal_vector=Vector(['1', '-1', '1']), constant_term='2') and
            t[1] == Plane(normal_vector=Vector(['0', '1', '1']), constant_term='1') and
            t[2] == Plane(normal_vector=Vector(['0', '0', '-9']), constant_term='-2')):
        print 'test case 4 failed'

def compute_rref_test():
    p1 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
    p2 = Plane(normal_vector=Vector(['0', '1', '1']), constant_term='2')
    s = LinearSystem([p1, p2])
    r = s.compute_rref()
    print r
    if not (r[0] == Plane(normal_vector=Vector(['1', '0', '0']), constant_term='-1') and
                    r[1] == p2):
        print 'test case 1 failed'

    p1 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
    p2 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='2')
    s = LinearSystem([p1, p2])
    r = s.compute_rref()
    print r
    if not (r[0] == p1 and
                    r[1] == Plane(constant_term='1')):
        print 'test case 2 failed'

    p1 = Plane(normal_vector=Vector(['1', '1', '1']), constant_term='1')
    p2 = Plane(normal_vector=Vector(['0', '1', '0']), constant_term='2')
    p3 = Plane(normal_vector=Vector(['1', '1', '-1']), constant_term='3')
    p4 = Plane(normal_vector=Vector(['1', '0', '-2']), constant_term='2')
    s = LinearSystem([p1, p2, p3, p4])
    r = s.compute_rref()
    print r
    if not (r[0] == Plane(normal_vector=Vector(['1', '0', '0']), constant_term='0') and
                    r[1] == p2 and
                    r[2] == Plane(normal_vector=Vector(['0', '0', '-2']), constant_term='2') and
                    r[3] == Plane()):
        print 'test case 3 failed'

    p1 = Plane(normal_vector=Vector(['0', '1', '1']), constant_term='1')
    p2 = Plane(normal_vector=Vector(['1', '-1', '1']), constant_term='2')
    p3 = Plane(normal_vector=Vector(['1', '2', '-5']), constant_term='3')
    s = LinearSystem([p1, p2, p3])
    r = s.compute_rref()
    print r
    if not (r[0] == Plane(normal_vector=Vector(['1', '0', '0']), constant_term=Decimal('23') / Decimal('9')) and
                    r[1] == Plane(normal_vector=Vector(['0', '1', '0']), constant_term=Decimal('7') / Decimal('9')) and
                    r[2] == Plane(normal_vector=Vector(['0', '0', '1']), constant_term=Decimal('2') / Decimal('9'))):
        print 'test case 4 failed'

if __name__ == '__main__':
    p1 = Plane(normal_vector=Vector(['7', '5', '3']), constant_term='1')
    p2 = Plane(normal_vector=Vector(['-5', '-4', '6']), constant_term='1')
    p3 = Plane(normal_vector=Vector(['2', '-2', '-9']), constant_term='1')
    p4 = Plane(normal_vector=Vector(['2.167', '-13.543', '-18.883']), constant_term='-10.567')
    s = LinearSystem([p1, p2, p3])
    print s.compute_solution()
    # # print Plane()
    #row_test()
    #triangle_form_test()
    # print s.compute_rref()
    # compute_rref_test()
    # print range(5)[::2]
