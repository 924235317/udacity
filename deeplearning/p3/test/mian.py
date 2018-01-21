import vector
from decimal import Decimal, getcontext

from fractions import Fraction

# s = [1, 2, 3]
# a = tuple([Decimal(x) for x in s])
# # print(type(a))
# print(Decimal('1.0')/Decimal(3.0))
#
# c = 10
# v = vector.Vector([1, 0, 0])
# v2 = vector.Vector([0, 1, 0])
# v1 = vector.Vector([1, 2, 3, 4])
# l = [c*x for x in v.coordinates]
# v_zero = vector.Vector([0, 0, 0])
# # print(type(v.dot(v)))
# v.normalized()
# print(v.angle_with(-v))
# print(v.is_parallel_to(v))
# print(v.is_orthogonal_to(v2))
# print(v.is_zero())
#
# # l = [1, 2, 3, 4]
# # l1 = [1, 2]
# # ll = zip(l, l, l)
# # print(v.angle_with(v))
# # print(type(v.dot(v)))
# #
# # print([x+y+z for x, y, z in ll])
#
#
# def swap(a, b):
#     a, b = b, a
# a = 1
# b = 2
# swap(a, b)
# print a, b

def compute(scalar_n, scalar_d, add_n, add_d, to_add_n, to_add_d):
    scalar = Fraction(scalar_n, scalar_d)
    add = Fraction(add_n, add_d)
    to_add = Fraction(to_add_n, to_add_d)
    res = Fraction(Fraction(scalar * add) + to_add)
    print '{} * {} + {} = {}'.format(add,scalar,to_add,res)


compute(-1, 2, 11, 65, -1, 10)

# class my_linsys():
#     def __init__(self, l, c):
#         if len(l) != c:
#             raise ValueError

