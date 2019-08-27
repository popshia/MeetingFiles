import numpy as np
from cv2 import cv2 as cv2
from matplotlib import pyplot as plt

originalImage = cv2.imread('flash.png')

imgRGB = cv2.cvtColor(originalImage, cv2.COLOR_BGR2RGB)
imgA = imgRGB.copy()
imgB = imgRGB.copy()
imgC = imgRGB.copy()

# 灰階化
imgRayB = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
# 二值化
ret, thresh = cv2.threshold(imgRayB, 127, 255, cv2.THRESH_BINARY)
'''
double threshold(InputArray src, OutputArray dst, double thresh, double maxval, int type)
→ src(imgRayB)：輸入圖，只能輸入單通道，8位元或32位元浮點數影像。
→ dst(*)：輸出圖，尺寸大小、深度會和輸入圖相同。
→ thresh(127)：閾值。
→ maxval(255)：二值化結果的最大值。
→ type(cv2.THRESH_BINARY)：二值化操作型態，共有THRESH_BINARY、THRESH_BINARY_INV、THRESH_TRUNC、THRESH_TOZERO、THRESH_TOZERO_INV五種。
    1. THRESH_BINARY：超過閾值的像素設為最大值(maxval)，小於閾值的設為0。
    2. THRESH_BINARY_INV：超過閾值的像素設為0，小於閾值的設為最大值(maxval)。
    3. THRESH_TRUNC：超過閾值的像素設為閾值，小於閾值的設為0。
    4. THRESH_TOZERO：超過閾值的像素值不變，小於閾值的設為0。
    5. THRESH_TOZERO_INV：超過閾值的像素值設為0，小於閾值的不變。
'''

# 找輪廓
img, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#    ⌃ contours is a list, stores every contour of the image, every contour is a Numpy array,
#      include the (x, y) of the object's boundary point
'''
void findContours(InputOutputArray image, OutputArrayOfArrays contours, OutputArray hierarchy, int mode, int method, Pointoffset=Point())
→ image(img, thresh)：輸入圖，使用八位元單通道圖，所有非零的像素都會列入考慮，通常為二極化後的圖。
→ contours(contours)：包含所有輪廓的容器(vector)，每個輪廓都是儲存點的容器(vector)，所以contours的資料結構為vector< vector>。
→ hierarchy(*)：可有可無的輸出向量，以階層的方式記錄所有輪廓。
→ mode(cv2.RETR_TREE)：取得輪廓的模式。
    1. CV_RETR_EXTERNAL：只取最外層的輪廓。
    2. CV_RETR_LIST：取得所有輪廓，不建立階層(hierarchy)。
    3. CV_RETR_CCOMP：取得所有輪廓，儲存成兩層的階層，首階層為物件外圍，第二階層為內部空心部分的輪廓，如果更內部有其餘物件，包含於首階層。
    4. CV_RETR_TREE：取得所有輪廓，以全階層的方式儲存。
→ method(cv2.CHAIN_APPROX_SIMPLE)：儲存輪廓點的方法。
    1. CV_CHAIN_APPROX_NONE：儲存所有輪廓點。
    2. CV_CHAIN_APPROX_SIMPLE：對水平、垂直、對角線留下頭尾點，所以假如輪廓為一矩形，只儲存對角的四個頂點。
'''

# 畫出輪廓
cv2.drawContours(imgA, contours, 0, (255, 0, 0), 5)  # -1:all contours
'''
void drawContours(InputOutputArray image, InputArrayOfArrays contours, int contourIdx, const Scalar& color, int thickness=1, int lineType=8, InputArray hierarchy=noArray(), int maxLevel=INT_MAX, Point offset=Point())
→ image(img_0)：輸入輸出圖，會將輪廓畫在此影像上。
→ contours(contours)：包含所有輪廓的容器(vector)，也就是findContours()所找到的contours。
→ contourIdx(0)：指定畫某個輪廓，通常同一張圖上找到的輪廓不只一個，所以有輪廓個別的索引值(-1: all contours)
→ color(255,0,0)：繪製的顏色。
→ thickness(3)：線條粗度（預設為1）
→ lineType(*)：繪製的線條型態。
→ hierarchy(*)：輪廓階層，也就是findContours()所找到的hierarchy。
→ maxLevel(*)：最大階層的輪廓，可以指定想要畫的輪廓，有輸入hierarchy時才會考慮，輸入的值代表繪製的層數。
    1. 0：繪製指定階層的輪廓。
    2. 1：繪製指定階層的輪廓，和他的一階子階層。
    3. 2：繪製指定階層的輪廓，和他的一階、二階子階層。剩下數字依此類推。
'''

# moments+
cntb = contours[0]  # cntb應該就是圖片的輪廓（？

# 取得輪廓的「矩」（我到現在還是搞不懂輸出的那一大長串）
M = cv2.moments(cntb)
'''
Moments moments(InputArray array, bool binaryImage=false)
→ array(cntb)：來源圖，可以輸入8位元單通道圖、浮點數2維陣列，或1xN、Nx1的Point或Point2f陣列。
→ binaryImage(*)：影像設定，只有array為影像時才有效果，如果設定為true，所有非零的像素都列入計算。
* 可從Moments計算質心位置。
'''
print(M)
# 計算X軸重心
cx = int(M['m10'] / M['m00'])
# 計算Y軸重心
cy = int(M['m01'] / M['m00'])
print("重心=", cx, cy)

# 計算輪廓面積
area = cv2.contourArea(cntb)
'''
double contourArea(InputArray contour, bool oriented=false)
→ contour(cntb)：輸入輪廓，一個含有2維點的vector。
→ oriented(*)：輪廓方向，如果設為true的話除了面積還會記錄方向，順時鐘和逆時鐘會有正負號的差異，預設為false，不論輪廓方向都返回正的面積值。
'''
print("面積=", area)

# 計算輪廓周長
perimeter = cv2.arcLength(cntb, True)
'''
double arcLength(InputArray curve, bool closed)
→ curve(cntb)：輸入輪廓，一個含有2維點的vector。
→ closed(True)：輪廓封閉，指定curve是否封閉，
* 回傳曲線的長度或封閉輪廓的周長。
'''
print("周長=", perimeter)
# moments-

# 凸殼檢測
'''
凸殼(Convex Hull)是一個計算幾何中的概念
簡單的說，在給定二維平面上的點集合，「凸殼就是將最外層的點連接起來的凸多邊型」
它能包含點集合中的所有點，在影像處理中，通常是找到某個物件後，用來填補空隙，或者是進一步的進行物件辨識。
'''
hull = cv2.convexHull(cntb)
'''
void convexHull(InputArray points, OutputArray hull, bool clockwise=false, bool returnPoints=true)
→ points(cntb)：輸入資訊，可以為包含點的容器(vector)或是Mat。
→ hull(hull)：輸出資訊，包含點的容器(vector)。
→ clockwise(*)：方向旗標，如果true是順時針，false是逆時針。
'''
print("hull=", hull)
# 檢測輪廓是否為凸多邊形
k = cv2.isContourConvex(cntb)
print(k)

# 搞不清楚這邊是在畫什麼圓
for i in range(len(hull)):
    cv2.circle(imgA, tuple(hull[i][0]), 3, [0, 0, 255], -1)
    '''
    void circle(Mat& img, Point center, int radius, const Scalar& color, int thickness=1, int lineType=8, int shift=0)
    → img(imgA)：輸入圖，圓會畫在上面。
    → center(tuple(hull[i][0]))：圓心。
    → radius(3)：圓半徑。
    → color(0, 0, 255)：圓形的顏色。
    → thickness(-1)：圓形的邊線寬度，輸入負值或CV_FILLED代表填滿圓形。
    → lineType(*)：通道型態，可輸入8、4、CV_AA： 8->8通道連結。 4->4通道連結。 CV_AA->消除鋸齒(antialiased line)，消除顯示器畫面線邊緣的凹凸鋸齒。
    '''

# 畫矩形凸包
'''
當我們得到物件輪廓後，可用boundingRect()得到包覆此輪廓的最小正矩形，
minAreaRect()得到包覆輪廓的最小斜矩形，minEnclosingCircle()得到包覆此輪廓的最小圓形，
這些函式協助我們填補空隙，或者作進一步的物件辨識，boundingRect()函式返回的是正矩形，
所以如果物件有傾斜的情形，返回的可能不是我們想要的結果。
'''

x, y, w, h = cv2.boundingRect(cntb)
# w為長，h為寬
'''
Rect boundingRect(InputArray points)
→ points(cntb)：輸入資訊，可以為包含點的容器(vector)或是Mat。
* 返回包覆輸入資訊的最小正矩形。
'''

cv2.rectangle(originalImage, (x, y), (x + w, y + h), (0, 255, 0), 5)
'''
void rectangle(Mat& img, Point pt1, Point pt2, const Scalar& color, int thickness=1, int lineType=8, int shift=0)
→ img(originalImage)：輸入圖，矩形會畫在上面。
→ pt1(x, y)：矩形頂點。
→ pt2(x + w, y + h)：矩形頂點，pt1的對角邊
→ color(0, 255, 0)：矩形的顏色。
→ thickness(2)：矩形的邊線寬度，輸入負值或CV_FILLED代表填滿矩形。
→ lineType(*)：通道型態，可輸入8、4、CV_AA： 8->8通道連結。 4->4通道連結。 CV_AA->消除鋸齒(antialiased line)，消除顯示器畫面線邊緣的凹凸鋸齒。
'''

rect = cv2.minAreaRect(cntb)
'''
RotatedRect minAreaRect(InputArray points)
→ points(cntb)：輸入資訊，可以為包含點的容器(vector)或是Mat。
* 返回包覆輸入資訊的最小斜矩形
'''

# 取得矩形的四個頂點座標
box = cv2.boxPoints(rect)

# 轉換為整數，還是不太懂int0，網路上說int0=intp（？
box = np.int0(box)
cv2.drawContours(originalImage, [box], 0, (0, 0, 255), 5)

# 擬合橢圓的最小外接矩形
ellipse = cv2.fitEllipse(cntb)
'''
fitEllipse回傳5個值
→ xc : x coordinate of the center
→ yc : y coordinate of the center
→ a : major semi-axis
→ b : minor semi-axis
→ theta : rotation angle
'''

cv2.ellipse(imgB, ellipse, (255, 0, 255), 5)
'''
void ellipse(Mat& img, Point center, Size axes, double angle, double startAngle, double endAngle, const Scalar& color, int thickness=1, int lineType=8, int shift=0)
→ img(imgB)：輸入圖，橢圓會畫在上面。
→ center(ellipse)：圓心。
→ axes(ellipse)：橢圓軸的尺寸。
→ angle(ellipse)：旋轉角度，單位角度。
→ startAngle(ellipse)：橢圓弧度起始角度，單位角度。
→ endAngle(ellipse)：橢圓弧度結束角度，單位角度。
→ color(255, 0, 255)：橢圓的顏色。
→ thickness(2)：橢圓的邊線寬度，輸入負值或CV_FILLED代表填滿橢圓形 。
→ lineType(*)：通道型態，可輸入8、4、CV_AA： 8->8通道連結。 4->4通道連結。 CV_AA->消除鋸齒(antialiased line)，消除顯示器畫面線邊緣的凹凸鋸齒。
'''

# 擬合最小圓形外框
(x, y), radius = cv2.minEnclosingCircle(cntb)
'''
void minEnclosingCircle(InputArray points, OutputPoint2f& center, Outputfloat& radius)
→ points(cntb)：輸入資訊，可以為包含點的容器(vector)或是Mat。
→ center(x,y)：包覆圓形的圓心。
→ radius(radius)：包覆圓形的半徑。
'''
center = (int(x), int(y))
radius = int(radius)
cv2.circle(imgB, center, radius, (0, 255, 255), 5)

# 畫直線擬合
rows, cols = imgC.shape[:2]
#                 ⌃ shape returns the rows, columns and the color channel, but here we only take the rows and columns.
[vx, vy, x, y] = cv2.fitLine(cntb, cv2.DIST_L2, 0, 0.01, 0.01)
'''
void fitLine(InputArray points, OutputArray line, int distType, double param, double reps, double aeps)
→ points(cntb)：二為點的數組或vector。
→ line([vx, vy, x, y])：輸出直線。
→ distType(cv2.DIST_L2)：距離類型。
→ param(0)：距離參數。
→ reps(0.01)：徑向精度參數。
→ aeps(0.01)：角度精度參數。
'''
lefty = int((-x * vy / vx) + y)
righty = int(((cols - x) * vy / vx) + y)

cv2.line(imgC, (cols - 1, righty), (0, lefty), (255, 255, 0), 5)
'''
void line(Mat& img, Point pt1, Point pt2, const Scalar& color, int thickness=1, int lineType=8, int shift=0)
→ img(imgC)：輸入圖，線會畫在上面。
→ pt1(cols - 1, righty)：線的起點。
→ pt2(0, lefty)：線的終點。
→ color(255, 255, 0)：線的顏色。
→ thickness(5)：線的厚度。
→ lineType(*)：通道型態，可輸入8、4、CV_AA： 8->8通道連結。 4->4通道連結。 CV_AA->消除鋸齒(antialiased line)，消除顯示器畫面線邊緣的凹凸鋸齒。
'''

# 顯示圖片
plt.subplot(2, 2, 1), plt.imshow(originalImage)
plt.title("Flash_originalImage"), plt.xticks([]), plt.yticks([])
plt.subplot(2, 2, 2), plt.imshow(imgA)
plt.title("Flash_imgA(originalContours)"), plt.xticks([]), plt.yticks([])
plt.subplot(2, 2, 3), plt.imshow(imgB)
plt.title("Flash_imgB(fitEllipse)"), plt.xticks([]), plt.yticks([])
plt.subplot(2, 2, 4), plt.imshow(imgC)
plt.title("Flash_imgC(fitLine)"), plt.xticks([]), plt.yticks([])
plt.show()
