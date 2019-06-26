import cv2



cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)
centerwidth = 512
centerheight = 384


# check file is opened
if not cap.isOpened():
  exit()

# initialize tracker
OPENCV_OBJECT_TRACKERS = {
  "csrt": cv2.TrackerCSRT_create,
  "kcf": cv2.TrackerKCF_create,
  "boosting": cv2.TrackerBoosting_create,
  "mil": cv2.TrackerMIL_create,
  "tld": cv2.TrackerTLD_create,
  "medianflow": cv2.TrackerMedianFlow_create,
  "mosse": cv2.TrackerMOSSE_create
}

tracker = OPENCV_OBJECT_TRACKERS['csrt']()


# main
ret, img = cap.read()

cv2.namedWindow('Select Window')
cv2.imshow('Select Window', img)

# select ROI
rect = cv2.selectROI('Select Window', img, fromCenter=False, showCrosshair=True)
cv2.destroyWindow('Select Window')

# initialize tracker
tracker.init(img, rect)

while True:

  # read frame from video
  ret, img = cap.read()



  # update tracker and get position from new frame
  success, box = tracker.update(img)
  # if success:
  left, top, w, h = [int(v) for v in box]
  right = left + w
  bottom = top + h

  pt1 = (int(left), int(top))
  pt2 = (int(right), int(bottom))
  cv2.rectangle(img, pt1, pt2, (255, 255, 255), 3)


  center_x = left + w /2
  center_y = top + h /2

  center = (int(center_x), int(center_y))

  img = cv2.circle(img, center, 3, (0,0,255), -1)
  img = cv2.circle(img, (centerwidth, centerheight), 5, (255,0,0), 5)

  if not success :
    #stop
    print("stop")
  elif(center_x < centerwidth):
    # 왼쪽으로 회전하는 모터
    print("Rotate Left")
  elif(center_x > centerwidth) :
    print("Rotate Right")

  cv2.imshow('img', img)

  key_in = cv2.waitKey(1)

  if key_in == ord('s'):
    #shoot
    print("shoot")

  elif key_in == ord('q'):
    break

# release everything
cap.release()
cv2.destroyAllWindows()