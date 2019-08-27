import cv2
import numpy as np

global cxx, cyy, cxx_last, cyy_last
cxx = 0
cyy = 0
cap = cv2.VideoCapture('1.mp4')
point = 100
cxx_m = np.zeros(point)
cyy_m = np.zeros(point)
count = 0

Green = np.uint8([[[0, 255, 0]]])
hsv_Green = cv2.cvtColor(Green, cv2.COLOR_BGR2HSV)
print(hsv_Green)

ret = cap.set(3, 640)  # Default is 640X480
# ret = cap.set(4, 480)  # change to 320X240

'''
cap.set(propId,value)
propId可以是0到46之間的任何数，每一個數代表一个個屬性，自己可以嘗試一下
'''

while 1:
	# Take each frame
	_, frame = cap.read()
	frame = cv2.flip(frame, 1)  # 0:inves up/down 1:mirror (right/left)  -1:inves up/down ,right/left

	# Convert BGR to HSV
	frame2 = frame.copy()
	frame = cv2.GaussianBlur(frame, (77, 77), 0)

	"""
	cv2.GaussianBlur(src, kSize, sigmaX[, dst[, sigmaY[, borderType]]])  
	src: 影象矩陣 
	kSize: 濾波視窗尺寸 ，高斯卷積大小且寬高均為奇數但可以不相等
	sigmaX: 水平方向上的標準差
	sigmaY: 垂直方向的標準差預設為0表示與水平方向相同
	borderType: 邊界填充型別
	
	"""
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	# define range of green color in HSV
	lower_green = np.array([60, 50, 50])
	upper_green = np.array([80, 255, 255])
	# Threshold the HSV image to get only green colors
	mask = cv2.inRange(hsv, lower_green, upper_green)

	"""
	hsv指的是原圖
	lower_green指的是圖像中低於這個lower_green的值，圖像值變為0
	upper_green指的是圖像中高於這個upper_green的值，圖像值變為0
	"""

	mask_org = mask.copy()

	# Bitwise-AND mask and original image
	res = cv2.bitwise_and(frame, frame, mask=mask)
	# 不知道mask = mask意思

	"""
	cv2.bitwise_and(src1, src2[, dst[, mask]])
	bitwise_and是對二進位制資料進行“與”操作，即對影象（灰度影象或彩色影象均可）每個畫素值進行二進位制
	src1 – first input array or a scalar.
	src2 – second input array or a scalar.
	src – single input array.
	dst – output array that has the same size and type as the input arrays.
	mask – optional operation mask, 8-bit single channel array, that specifies elements of the output array to be changed.
	"""

	# =================================
	img2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	# 版本問題原本cv2.findContours會回傳三個參數但是較新版本只回兩個

	cx = np.zeros(len(contours))
	cy = np.zeros(len(contours))
	# global cxx,cyy,cxx_last,cyy_last,count,cxx_m,cyy_m
	# 下面應該就是找圓跟畫圓，但是我看不太懂
	if len(contours) > 0:
		cxx_last = cxx
		cyy_last = cyy
		if count > 1:
			cxx_m[count] = cxx
			cyy_m[count] = cyy
			count = count + 1
		else:
			count = 0
			cxx_m = np.zeros(point)
			cyy_m = np.zeros(point)

		cxx = 0
		cyy = 0

		print(len(contours))
		cnt = contours[0]
		M = cv2.moments(cnt)
		# print (M)
		if M['m00'] > 1:

			for i in range(len(contours)):
				# global cxx,cyy
				cx[i] = int(M['m10'] / M['m00'])
				cy[i] = int(M['m01'] / M['m00'])
				cxx = cxx + cx[i]
				cyy = cyy + cy[i]

		# global cxx,cyy
		cxx = cxx / (len(contours))
		cyy = cyy / (len(contours))

		if cxx > 1:
			print("Center=", cxx, cyy)
			# area = cv2.contourArea(cnt)
			# print("Area",area)
			# perimeter = cv2.arcLength(cnt,True)
			# print("perimeter=",perimeter)
			if cxx_last > 1:
				cv2.circle(res, (int(cxx_last), int(cyy_last)), 5, (0, 0, 255), -1)
				cv2.circle(frame, (int(cxx_last), int(cyy_last)), 5, (0, 0, 255), -1)
			if count < (point - 1):
				for j in range(0, (point - 1), 1):
					if int(cxx_m[j + 1]) > 0:
						cv2.line(res, (int(cxx_m[j]), int(cyy_m[j])), (int(cxx_m[j + 1]), int(cyy_m[j + 1])), (255, 0, 255), 3)
						cv2.circle(res, (int(cxx_m[j]), int(cyy_m[j])), 10, (0, 255, 0), 0)
						cv2.line(frame, (int(cxx_m[j]), int(cyy_m[j])), (int(cxx_m[j + 1]), int(cyy_m[j + 1])), (255, 0, 255), 3)
						cv2.circle(frame, (int(cxx_m[j]), int(cyy_m[j])), 10, (0, 255, 0), 0)
						# print(j,cxx_m[j],cyy_m[j])

	# =================================

	cv2.drawContours(res, contours, -1, (255, 0, 0), 2)
	cv2.imshow('Frame', frame)
	# cv2.imshow('mask',mask_org)
	cv2.imshow('contours:', res)
	# cv2.imshow('res',res)
	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		break

cv2.destroyAllWindows()
