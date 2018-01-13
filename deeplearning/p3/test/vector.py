from math import sqrt, acos, pi
from decimal import Decimal, getcontext


class Vector(object):
    '''my vector objcet'''

    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = "Cannot normalize the zero vector"

    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(self.coordinates)
            getcontext().prec = 5

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')

    def plus(self, v):
        return Vector(self + v)

    def minus(self, v):
        return Vector(self - v)

    def times_scalar(self, c):
        return Vector([c*x for x in self.coordinates])

    def length(self):
        return len(self.coordinates)

    def magnitude(self):
        coordinates_squared = [x**2 for x in self.coordinates]
        return sqrt(sum(coordinates_squared))

    def normalized(self):
        try:
            magnitude = self.magnitude()
            return self.times_scalar(1.0/magnitude)
        except ZeroDivisionError:
            raise Exception(self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG)

    def dot(self, v):
        return sum([x * y for x, y in zip(self.coordinates, v.coordinates)])

    def angle_with(self, v, in_degrees=False):
        try:
            u1 = self.normalized()
            u2 = v.normalized()
            print(type(u1), type(u2))
            angle_in_radians = acos(u1.dot(u2))
            print "a"
            print angle_in_radians

            if in_degrees:
                degrees_per_radian = 180. / pi
                return angle_in_radians * degrees_per_radian
            else:
                return angle_in_radians

        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception('Cannot compute an angle with the zero vector')
            else:
                raise e

    def __sub__(self, v):
        if not self.dimension == v.dimension:
            raise ValueError

        return [x-y for x, y in zip(self.coordinates, v.coordinates)]

    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def __len__(self):
        return self.dimension

    def __add__(self, v):
        if not self.dimension == v.dimension:
            raise ValueError

        return [x + y for x, y in zip(self.coordinates, v.coordinates)]

    def __mul__(self, v):
        '''Inner product'''
        return sum([x * y for x, y in zip(self.coordinates, v.coordinates)])

    def __div__(self, v):
        return [x / y for x, y in zip(self.coordinates, v.coordinates)]