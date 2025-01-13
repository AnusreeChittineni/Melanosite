#trying to use cv2 for the algorithm
import numpy as np
import cv2

def model(img):
  const = 255
  const = np.int8(const)

  #print(img)
  
  image = cv2.imread(img)

  ## convert to hsv
  hsv2 = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

  ## mask of greyish blue
  maskBlue = cv2.inRange(hsv2, (70, 50, 50), (170, 190, 249))

  ## mask of yellow (15,0,0) ~ (36, 255, 255)
  maskRed = cv2.inRange(hsv2, (80,10,10), (170, 120, 140))

  ## final mask and masked
  mask = cv2.bitwise_or(maskBlue, maskRed)
  #target = cv2.bitwise_and(img,img, mask=mask)

  #cv2.imwrite("target.png", target)

  #from google.colab.patches import cv2_imshow
  #cv2_imshow(mask)
  #how many white pixels there are, aka how many pixels are of the target color
  white = 0

  for col in mask:
    for item in col:
      if item == np.uint8(const):  
        white += 1

  percent = float(white)/mask.size * 9
  return (percent)
  