import math
import numpy as np
from matplotlib import pyplot as plt
from decimal import *


def circle(x):
	y = math.sqrt(1.0 - math.pow(x, 2) / 4)
	return y


N = 100000
Es_count = 0
px = np.random.randint(2000, size=N)
pd = np.mat([1000.0] * N)
px = np.divide(px, pd)
px = px.reshape(N, -1)
py = np.random.rand(N)

sx = np.linspace(-2, 2, 100)
sg = np.array([circle(t) for t in sx])
sg2 = -sg

for i in range(N):
	if (math.pow(px[i], 2) / 4) + math.pow(py[i], 2) <= 1:
		Es_count += 1

print("在圓內的點數有", Es_count)
Es_area = 4 * (2.0 * Es_count / N)
print("面積=", Es_area)
Area_msg = "Ellipse Area=" + str(Es_area)

# 畫出ellipse函數
plt.subplot(1, 1, 1)
plt.plot(sx, sg, 'b-', linewidth=2.0)
plt.plot(sx, sg2, 'b-', linewidth=2.0)
plt.axis([-2.0, 2.0, -1.5, 1.5])  # 分別設定X,Y軸的最小最大值
plt.title(' ellipse ', fontsize=10)
plt.ylabel('Y')
plt.xlabel('x')
plt.grid(True)

plt.scatter(px, py, c="green", alpha=0.9)
plt.text(0.5, 1.2, Area_msg)

plt.show()
