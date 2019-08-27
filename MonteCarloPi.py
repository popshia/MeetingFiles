import math
import numpy as np
from matplotlib import pyplot as plt
from decimal import*


def circle(x):
	if x <= 1:
		y = math.sqrt(1.0 - math.pow(x, 2))  # sqrt() 返回數字x的平方根，pow() 方法返回 xy（x的y次方） 的值
		# 即y = (1 - x²)開根號，因為x² + y² = 1
		return y


N = 100000
pei_count = 0
px = np.random.rand(N)  # 根據給定維度生成[0,1)之间的數據，包含0，不包含1
# 即生成一維100000個0-1之間的數
py = np.random.rand(N)

sx = np.linspace(0.0, 1, 100)  # 產生 0 - 1 的等差數列，要求元素為100個 （默认情况下，linspace函数可以生成元素为50的等间隔数列）
sg = np.array([circle(t) for t in sx])  # 目的猜想是調整sx的數據，<= 1 的調整，>1的不調整

for i in range(N):  # for 0 - 99999
	if math.pow(px[i], 2) + math.pow(py[i], 2) <= 1:  # 如果在圓內
		pei_count += 1  # 在圓內的計數器+1

print("在圓內的點數有", pei_count)
pei = 4 * pei_count / N

"""
那麼產生分布於0~1 之間的亂數，應當會均勻的分布於正方形之內，如下圖綠點所示，
而分布於1/4圓內的數量假設為a ，分布於圓外的數量為b，N則是所產生的亂數總數為
N=a+b。
那麼其亂數分布數量a與N的比值應與1/4圓面積及正方形面積成正比，即pei = 4a/N
"""

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
