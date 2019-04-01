import cv2 as cv
import numpy as np

def setLabel(image, str, contour):
    (text_width, text_height), baseline = cv.getTextSize(str, cv.FONT_HERSHEY_SIMPLEX, 0.7, 1)
    x,y,width,height = cv.boundingRect(contour)
    pt_x = x+int((width-text_width)/2)
    pt_y = y+int((height + text_height)/2)
    cv.rectangle(image, (pt_x, pt_y+baseline), (pt_x+text_width, pt_y-text_height), (200,200,200), cv.FILLED)
    cv.putText(image, str, (pt_x, pt_y), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 1, 8)

#Aim def
def tuple_add(x,y):
    return tuple(np.add(x,y))

def nothing(x):
    pass


# Aim Radius
radius = 10

#Aim location
centerwidth = 640
centerheight = 480

# Aim color = (b,g,r)
red = (0,0,255)
green = (0,255,0)
blue = (255, 0, 0)
white = (255, 255, 255)
yellow = (0, 255, 255)
cyan = (255, 255, 0)
magenta = (255, 0, 255)

hsv = 0
lower_blue1 = 0
upper_blue1 = 0
lower_blue2 = 0
upper_blue2 = 0
lower_blue3 = 0
upper_blue3 = 0

def mouse_callback(event, x, y, flags, param):
    global hsv, lower_blue1, upper_blue1, lower_blue2, upper_blue2, lower_blue3, upper_blue3

    # 마우스 왼쪽 버튼 누를시 위치에 있는 픽셀값을 읽어와서 HSV로 변환합니다.
    if event == cv.EVENT_LBUTTONDOWN:
        print(img_color[y, x])
        color = img_color[y, x]

        one_pixel = np.uint8([[color]])
        hsv = cv.cvtColor(one_pixel, cv.COLOR_BGR2HSV)
        hsv = hsv[0][0]

        threshold = cv.getTrackbarPos('threshold', 'img_result')
        # HSV 색공간에서 마우스 클릭으로 얻은 픽셀값과 유사한 필셀값의 범위를 정합니다.
        if hsv[0] < 10:
            print("case1")
            lower_blue1 = np.array([hsv[0]-10+180, threshold, threshold])
            upper_blue1 = np.array([180, 255, 255])
            lower_blue2 = np.array([0, threshold, threshold])
            upper_blue2 = np.array([hsv[0], 255, 255])
            lower_blue3 = np.array([hsv[0], threshold, threshold])
            upper_blue3 = np.array([hsv[0]+10, 255, 255])
            #     print(i-10+180, 180, 0, i)
            #     print(i, i+10)

        elif hsv[0] > 170:
            print("case2")
            lower_blue1 = np.array([hsv[0], threshold, threshold])
            upper_blue1 = np.array([180, 255, 255])
            lower_blue2 = np.array([0, threshold, threshold])
            upper_blue2 = np.array([hsv[0]+10-180, 255, 255])
            lower_blue3 = np.array([hsv[0]-10, threshold, threshold])
            upper_blue3 = np.array([hsv[0], 255, 255])
            #     print(i, 180, 0, i+10-180)
            #     print(i-10, i)
        else:
            print("case3")
            lower_blue1 = np.array([hsv[0], threshold, threshold])
            upper_blue1 = np.array([hsv[0]+10, 255, 255])
            lower_blue2 = np.array([hsv[0]-10, threshold, threshold])
            upper_blue2 = np.array([hsv[0], 255, 255])
            lower_blue3 = np.array([hsv[0]-10, threshold, threshold])
            upper_blue3 = np.array([hsv[0], 255, 255])
            #     print(i, i+10)
            #     print(i-10, i)

        print(hsv[0])
        print("@1", lower_blue1, "~", upper_blue1)
        print("@2", lower_blue2, "~", upper_blue2)
        print("@3", lower_blue3, "~", upper_blue3)


cv.namedWindow('img_color')
cv.setMouseCallback('img_color', mouse_callback)

cv.namedWindow('img_result')
cv.createTrackbar('threshold', 'img_result', 0, 255, nothing)
cv.setTrackbarPos('threshold', 'img_result', 30)
capture = cv.VideoCapture(0)


capture.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv.CAP_PROP_FRAME_HEIGHT, 960)


while (True):

    ret, img_color = capture.read()

    # 원본 영상을 HSV 영상으로 변환합니다.
    img_hsv = cv.cvtColor(img_color, cv.COLOR_BGR2HSV)

    # 범위 값으로 HSV 이미지에서 마스크를 생성합니다.
    img_mask1 = cv.inRange(img_hsv, lower_blue1, upper_blue1)
    img_mask2 = cv.inRange(img_hsv, lower_blue2, upper_blue2)
    img_mask3 = cv.inRange(img_hsv, lower_blue3, upper_blue3)
    img_mask = img_mask1 | img_mask2 | img_mask3

    kernel = np.ones((11, 11), np.uint8)
    img_mask = cv.morphologyEx(img_mask, cv.MORPH_OPEN, kernel)
    img_mask = cv.morphologyEx(img_mask, cv.MORPH_CLOSE, kernel)

    # 마스크 이미지로 원본 이미지에서 범위값에 해당되는 영상 부분을 획득합니다.
    img_result = cv.bitwise_and(img_color, img_color, mask=img_mask)

    num0fLabels, img_label, stats, centroids = cv.connectedComponentsWithStats(img_mask)

    for idx, centroid in enumerate(centroids):
        if stats[idx][0] == 0 and stats[idx][1] == 0:
            continue
        if np.any(np.isnan(centroid)):
            continue
        x, y, width, height, area = stats[idx]
        centerX, centerY = int(centroid[0]), int(centroid[1])

        if area > 50:
            cv.circle(img_color, (centerX, centerY), 10, (0, 0, 255), 10)
            cv.rectangle(img_color, (x, y), (x + width, y + height), (0, 0, 255))



    contours, hierarchy = cv.findContours(img_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        size = len(cnt)
        #print(size)

        epsilon = 0.005 * cv.arcLength(cnt, True)
        approx = cv.approxPolyDP(cnt, epsilon, True)

        size = len(approx)
        #print(size)

        cv.line(img_color, tuple(approx[0][0]), tuple(approx[size - 1][0]), (0, 255, 0), 3)
        for k in range(size - 1):
            cv.line(img_color, tuple(approx[k][0]), tuple(approx[k + 1][0]), (0, 255, 0), 3)

        if cv.isContourConvex(approx):
            if size == 3:
                setLabel(img_color, "triangle", cnt)
            elif size == 4:
                setLabel(img_color, "rectangle", cnt)
            elif size == 5:
                setLabel(img_color, "pentagon", cnt)
            elif size == 6:
                setLabel(img_color, "hexagon", cnt)
            elif size == 8:
                setLabel(img_color, "octagon", cnt)
            elif size == 10:
                setLabel(img_color, "decagon", cnt)
            else:
                setLabel(img_color, str(size), cnt)
        else:
            setLabel(img_color, str(size), cnt)
#Aim
    thickness = 1
    result = cv.circle(img_color, tuple_add((0, 0), (centerwidth, centerheight)), radius, red, thickness)



    cv.imshow('img_color', img_color)
    cv.imshow('img_mask', img_mask)
    cv.imshow('img_result', img_result)
    cv.imshow('result', img_color)

    if cv.waitKey(1) > 0: break