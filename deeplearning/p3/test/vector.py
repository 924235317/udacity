from math import sqrt, acos, pi
from decimal import Decimal, getcontext


getcontext().prec = 5


class Vector(object):
    '''my vector objcet'''
    #EXCEPTION
    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = "Cannot normalize the zero vector"
    NO_UNIQUE_PARALLEL_COMPONENT_MSG = "No unique parallel component"
    NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG = "No unique orthogonal component"
    CANNOT_GET_CROSS_PRODUCT_MSG = "Cannot get cross product"
    ONLY_DEFINED_IN_TWO_TRHEE_DIMS_MSG = "Only defined in two or three dimensions"

    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(self.coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')

    def plus(self, v):
        return Vector([x + y for x, y in zip(self.coordinates, v.coordinates)])

    def minus(self, v):
        return Vector([x - y for x, y in zip(self.coordinates, v.coordinates)])

    # ----------------inner product-----------------------------
    def times_scalar(self, c):
        return Vector([Decimal(c)*x for x in self.coordinates])

    def length(self):
        return len(self.coordinates)

    def magnitude(self):
        coordinates_squared = [x**2 for x in self.coordinates]
        return sqrt(sum(coordinates_squared))

    def normalized(self):
        try:
            magnitude = self.magnitude()
            return self.times_scalar(Decimal(1.0/magnitude))
        except ZeroDivisionError:
            raise Exception(self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG)
        # except TypeError:
        #     raise Exception("hehe")

    def dot(self, v):
        return sum([x * y for x, y in zip(self.coordinates, v.coordinates)])

    def angle_with(self, v, in_degrees=False):
        try:
            u1 = self.normalized()
            u2 = v.normalized()
            angle_in_radians = acos(u1.dot(u2))

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

    #----------------projecting vector-----------------------------
    def is_orthogonal_to(self, v, tolerance=1e-10):
        return abs(self.dot(v)) < tolerance

    def is_parallel_to(self, v, tolerance=1e-10):
        # print tolerance
        # print self.is_zero()
        # print v.is_zero()
        # print self.angle_with(v) < tolerance
        # print self.angle_with(v) - pi < tolerance
        # print abs(self.angle_with(v) - pi)
        # print(pi)
        return (self.is_zero() or
                v.is_zero() or
                abs(self.angle_with(v) < tolerance) or
                abs(self.angle_with(v) - pi) < tolerance)

    def is_zero(self, tolerance=1e-10):
        return self.magnitude() < tolerance

    def component_parallel_to(self, basis):
        try:
            u = basis.normalized()
            weight = self.dot(u)
            return u.times_scalar(weight)

        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e

    def component_orthogonal_to(self, v):
        try:
            projection = self.component_parallel_to(v)
            return self.minus(projection)

        except Exception as e:
            if str(e) == self.NO_UNIQUE_PARALLEL_COMPONENT_MSG:
                raise Exception(self.NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG)
            else:
                raise e

    # ----------------cross product-----------------------------
    def cross(self, v):
        try:
            x1, y1, z1 = self.coordinates
            x2, y2, z2 = v.coordinates
            cross_product = [
                y1 * z2 - y2 * z1,
                z1 * x2 - x1 * z2,
                x1 * y2 - x2 * y1
            ]
            return Vector(cross_product)

        except Exception as e:
            msg = str(e)
            if msg == "too many values to unpack" or \
                    msg == "need more than 1 value to unpack":
                raise Exception(self.ONLY_DEFINED_IN_TWO_TRHEE_DIMS_MSG)
            elif msg == "need more than 2 values to unpack":
                self_embedded_in_r3 = self
                v_embedded_in_r3 = v
                if self.length() == 2:
                    self_embedded_in_r3.coordinates += (0, )
                if v.length() == 2:
                    v_embedded_in_r3.coordinates += (0, )
                return self_embedded_in_r3.cross(v_embedded_in_r3)
            else:
                raise e

    def area_of_parallelogram(self, v):
        cross_product = self.cross(v)
        return cross_product.magnitude()

    def area_of_triangle(self, v):
        parallelogram_area = self.area_of_parallelogram(v)
        return 0.5 * parallelogram_area

    # ----------------some some some-----------------------------
    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    def __sub__(self, v):
        if not self.dimension == v.dimension:
            raise ValueError

        return [x - y for x, y in zip(self.coordinates, v.coordinates)]

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

    def __neg__(self):
        return Vector([-x for x in self.coordinates])


if __name__ == "__main__":
    print(pi)
    a = Vector([8.462, 7.893, -8.187])
    b = Vector([6.984, -5.975, 4.778])
    c = Vector([-8.987, -9.838, 5.031])
    d = Vector([-4.268, -1.861, -8.866])
    e = Vector([1.5, 9.547, 3.691])
    f = Vector([-6.007, 0.124, 5.772])
    print(type(a.dot(-a)))
    print(a.component_orthogonal_to(b))
    print(a.cross(b))
    print(c.area_of_parallelogram(d))
    print(e.area_of_triangle(f))
