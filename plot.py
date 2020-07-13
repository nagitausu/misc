import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import math

d = 2
p = 0 
q = 0 
r = -3 

def f(x, y):
    d2 = d**2
    r2 = r**2
    q2 = q**2
    base = 8 * (d2 - r2)
    mid = 4 * (-d2 + p**2 - 2*p * x + q2 - 2*q * y + r2)
    h1 = -d**4 + 2 * d2 * p**2 - 4 * d2 * p * x + 2 * d2 * q2 - 4 * d2 * q * y + 2 * d2 * r2 + 4 * d2 * x**2 + 4 * d2 * y**2 - p**4 + 4 * p**3 * x - 2 * p**2 * q2 + 4 * p**2 * q * y - 2 * p**2 * r2 - 4 * p**2 * x**2 + 4 * p * q2 * x - 8 * p * q * x * y + 4 * p * r2 * x - q**4 + 4 * q**3 * y - 2 * q2 * r2 - 4 * q2 * y**2 + 4 * q * r2 * y - r**4
    h2 = r2 * (-4 * d2 + 4 * p**2 - 8*p * x + 4*q2 - 8*q * y + 4*r2)**2 - 16 * (d2 - r2) * h1
    if h2 < 0 or base == 0:
        return None, None
    z1 = (math.sqrt(h2) - r * mid) / base
    z2 = (-math.sqrt(h2) - r * mid) / base
    return z1, z2


n = 10
dots = []
for i in range(-n, n+1):
    for j in range(-n, n+1):
        dots.append((i, j))

result = [[] for _ in range(3)]
for x, y in dots:
    z1, z2 = f(x, y)
    if z1 is not None:
        result[0].append(x)
        result[1].append(y)
        result[2].append(z1)
        result[0].append(x)
        result[1].append(y)
        result[2].append(z2)

fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot("111", projection="3d")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
ax.scatter(result[0], result[1], result[2])
plt.tight_layout()
plt.show()