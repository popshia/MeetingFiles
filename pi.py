import math
import numpy as np
from matplotlib import pyplot as plt
from decimal import *


def circle(x):
	if x <= 1:
		y = math.sqrt(1.0 - math.pow(x, 2))
	return y


N = 100000
pei_count = 0
px = np.random.rand(N)
py = np.random.rand(N)

sx = np.linspace(0.0, 1, 100)
sg = np.array([circle(t) for t in sx])

for i in range(N):
	if math.pow(px[i], 2) + math.pow(py[i], 2) <= 1:
		pei_count += 1

print("在圓內的點數有", pei_count)
pei = 4 * pei_count / N
print("圓周率=", pei)
Pei_msg = "Pei=" + str(pei)

# 畫出circle函數
plt.subplot(1, 1, 1)
plt.plot(sx, sg, 'b-', linewidth=2.0)
plt.axis([0, 1.5, 0, 1.5])  # 分別設定X,Y軸的最小最大值
plt.title(' circle ', fontsize=10)
plt.ylabel('Y')
plt.xlabel('x')
plt.grid(True)

plt.scatter(px, py, c="green", alpha=0.9)
plt.text(0.5, 1.2, Pei_msg)

plt.show()
