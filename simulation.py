import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import numpy as np
import random
from itertools import combinations
import math

class space_object:
    def __init__(self, p0, v0):
        self.p0 = p0
        self.p = p0
        self.v = v0

    def update(self, sec):
        self.p = p0 + sec * self.v0 

class satellite(space_object):
    def __init__(self, p0, v0, is_multipassed=False):
        super(satellite, self).__init__(p0, v0)
        self.is_multipassed = is_multipassed

class rover(space_object):
    def __init__(self, p0, v0, d_rho):
        super(rover, self).__init__(p0, v0)
        self.d_rho = d_rho

def get_range(r, s, is_pseudo=False):
    if s.is_multipassed:
        return np.linalg.norm(r.p - s.p * np.array([1.0, -1.0, 1.0])) + is_pseudo * r.d_rho
    else:
        return np.linalg.norm(r.p - s.p) + is_pseudo * r.d_rho

def calc_spp(satellites, meas, itr=3):
    p = np.zeros(3)
    for _ in range(itr):
        H = np.zeros((len(satellites), 4)) + 1.0
        dp = []
        for i, s in enumerate(satellites):
            rhoi = np.linalg.norm(s.p - p)
            dpi = meas[i] - rhoi
            dp.append(dpi)
            hi = -1.0 / rhoi * (s.p - p)
            H[i][0:3] = hi
        S = np.dot(H.T, H)
        try:
            S_inv = np.linalg.inv(S)
        except Exception as e:
            print("bad positioning")
            return None
        rho = np.array([dp]).T
        dx = np.dot(S_inv, np.dot(H.T, rho))
        p += dx.flatten()[:3]
    bias = dx[3][0]
    return p, bias

def calc_comb_spp(satellites, meas, r=4):
    n = len(satellites)
    h = math.factorial(n) // math.factorial(r) // math.factorial(n - r)
    ret = np.zeros((h, r))
    for i, comb in enumerate(combinations(zip(satellites, meas), r)):
        s_comb = []
        m_comb = []
        for s, m in comb:
            s_comb.append(s)
            m_comb.append(m)
        r = calc_spp(s_comb, m_comb)
        if r is not None:
            ret[i][0:3] = r[0]
            ret[i][3] = r[1]
    return ret
    
satellites = []
multipassset = set([0, 1, 2, 3])
# multipassset = set([])
for i in range(10):
    p0 = np.array([0.0, 0.0, 2000000.0]) 
    v0 = np.array([0.0, 0.0, 0.0])
    p_noise = np.array([random.random() for _ in range(2)] + [0.0]) * 2000000.0
    s = satellite(p0 + p_noise, v0, i in multipassset)
    satellites.append(s)

p0 = np.array([1.0, 2.0, 3.0]) 
v0 = np.array([0.0, 0.0, 0.0])
r = rover(p0, v0, 0.0)

meas = []
for s in satellites:
    m_noise = random.random() * 0.0
    meas.append(get_range(r, s, is_pseudo=True) + m_noise)

result = calc_comb_spp(satellites, meas, 4)
print(result)

fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot("111", projection="3d")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
ax.scatter(result[:, 0], result[:, 1], result[:, 2])
plt.tight_layout()
plt.show()