import sys
import matplotlib.pyplot as plt
import matplotlib.colors as mp_colors
import pymap3d
import japanmap
import math
import random

cs = []
for rgb in mp_colors.TABLEAU_COLORS.values():
    cs.append(rgb)

DEG2RAD = math.pi / 180.0

# See https://tjkendev.github.io/procon-library/python/convex_hull_trick/deque.html
def cross3(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])

def convex_hull(ps):
    qs = []
    N = len(ps)
    for p in ps:
        while len(qs) > 1 and cross3(qs[-1], qs[-2], p) > 0:
            qs.pop()
        qs.append(p)
    t = len(qs)
    for i in range(N-2, -1, -1):
        p = ps[i]
        while len(qs) > t and cross3(qs[-1], qs[-2], p) > 0:
            qs.pop()
        qs.append(p)
    return qs

def calc_area(ps):
    ret = 0.0
    for (x0, y0), (x1, y1) in zip(ps, ps[1:]):
        ret += x0 * y1 - x1 * y0
    ret *= 0.5
    return ret

qpqo = japanmap.get_data()
pnts = japanmap.pref_points(qpqo)

# We don't have to care for presice scalling
lat0 = pnts[20][0][1] * DEG2RAD
lon0 = pnts[20][0][0] * DEG2RAD

ranking = []
for i in range(47):
    x = []
    y = []
    enus = []
    for lon, lat in pnts[i]:
        lat *= DEG2RAD; lon *= DEG2RAD
        e, n, u = pymap3d.geodetic2enu(lat, lon, 0.0, lat0, lon0, 0.0)
        # values have to be distinct
        enus.append([e + random.random(), n + random.random()])
        x.append(e)
        y.append(n)
    
    original_area = abs(calc_area(enus))
    
    enus.sort()
    ret = convex_hull(enus)
    convex_area = abs(calc_area(ret))
    chx = []
    chy = []
    for nx, ny in ret:
        chx.append(nx)
        chy.append(ny)
    
    plt.plot(x, y, c="k", alpha=0.3)
    plt.plot(chx, chy, c=cs[(i + 1) % 9])
    plt.axis("equal")
    rate = original_area / convex_area * 100.0
    ranking.append((rate, japanmap.pref_names[i+1]))
    print(japanmap.pref_names[i+1], rate)
    plt.show()

ranking.sort(reverse=True)
for score, name in ranking:
    print(name, "{:.04f}".format(score) + "%")
