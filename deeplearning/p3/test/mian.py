import vector
from decimal import Decimal, getcontext

s = [1, 2, 3]
a = tuple([Decimal(x) for x in s])
print(type(a))
print Decimal(1) * 2

v = vector.Vector([1, 2, 3])
v1 = vector.Vector([1, 2, 3, 4])

print(v.normalized())

l = [1, 2, 3, 4]
l1 = [1, 2]
ll = zip(l, l, l)
print(v.angle_with(v))
print(type(v.dot(v)))

print([x+y+z for x, y, z in ll])
