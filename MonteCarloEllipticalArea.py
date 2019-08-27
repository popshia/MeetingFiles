#coding:utf-8
import math
import numpy as np
from matplotlib import pyplot as plt
from decimal import *
 
 
def circle(x):
 y = math.sqrt(1.0-math.pow(x,2)/4) # y = ( 1 - x的2次方/4 )開根號
 return y
  
N = 100000
Es_count=0
px = np.random.randint(2000, size=N) # 隨機產生N個 0 - 1999的實數  https://docs.scipy.org/doc/numpy-1.15.1/reference/generated/numpy.random.randint.html
pd=np.mat([1000.0]*N) # N個[1000.0]
px=np.divide(px, pd) # px / pd
px=px.reshape(N,-1) # 形状维度是-1時，从數組的長度和其餘維度推斷該值。
py = np.random.rand(N) # 生成一維的N個0-1之間的數
 
sx=np.linspace(-2, 2, 100) # 產生 -2 到 2 的等差數列，要求元素為100個
sg=np.array([circle(t) for t in sx])  #目的猜想是調整sx的數據，全部調整
sg2=-sg
 
for i in range(N):
 if (math.pow(px[i],2)/4)+math.pow(py[i],2)<=1: #如果在橢圓內
  Es_count+=1 # 橢圓計數器+1
  
print("在圓內的點數有",Es_count)
Es_area=4*(2.0*Es_count/N) 
"""
如下圖三，產生亂數0~2之間的實數對應於x軸， 產生亂數
0~1之間的實數對應於y軸，其產生的亂數點應分布於2x1的
長方形內。如同上述求圓周率π，假設分布於1/4橢圓內的亂
數數量為a，1/4橢圓面積為s，全部分布於長方形內的亂數
總數為N，
那麼根據面積比關係： S = 4 x 2a/N
"""
print("面積=",Es_area)
Area_msg="Ellipse Area="+str(Es_area)
 
#畫出ellipse函數 
plt.subplot(1,1,1)    
plt.plot(sx, sg, 'b-',linewidth=2.0)   
plt.plot(sx, sg2, 'b-',linewidth=2.0)  
plt.axis([-2.0,2.0, -1.5,1.5])   #分別設定X,Y軸的最小最大值
plt.title(' ellipse ',fontsize=10)
plt.ylabel('Y')
plt.xlabel('x')
plt.grid(True)
 
px = np.array(px) 
plt.scatter(px, py, c="green", alpha=0.9) 
#plt.scatter(px.tolist(), py, c="green", alpha=0.9)
"""
px的type==<class 'numpy.matrix'>不是一维（1-D）的
scatter前兩個參數需要ndarray性別
解決方式：直接加.tolist()或px=np.array(px)
"""

plt.text(0.5, 1.2,Area_msg)
 
plt.show()
