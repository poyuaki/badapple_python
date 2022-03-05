import copy
import cv2
import numpy as np


def make_frame_c(cap_file):

  width = int(cap_file.get(cv2.CAP_PROP_FRAME_WIDTH))
  height = int(cap_file.get(cv2.CAP_PROP_FRAME_HEIGHT))

  count = 0

  message_count = 0

  dots_array = []

  beta_array = []

  test_array = []

  while True:

    ret, frame = cap_file.read()

    if ret == False:
      break

    bairitu = 0.2
    frame = cv2.resize(frame , (int(width*bairitu), int(height*bairitu)))
    im_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    thresh = 128
    im_bool = im_gray > thresh # 2値化
    text = ""

    y_count = 0
    x_count = 0

    frame_array = []

    for y in im_bool:
      for x in y:
        x = int(x)
        judge_x = abs(x - 1)
        if count == 0 or (count > 0 and [x_count, y_count, judge_x] in test_array):
          frame_array.append([x_count, y_count, x])
          if count > 0:
            index = test_array.index([x_count, y_count, judge_x])
            test_array[index] = [x_count, y_count, x]
        x_count += 1
      x_count = 0
      y_count += 1

    beta_array.append(frame_array)

    if count == 0:
      test_array = copy.copy(beta_array[0])
  
    count += 1
  
    check_percent = round(count / cap_file.get(cv2.CAP_PROP_FRAME_COUNT) * 100)
    if check_percent % 2 == 0 and check_percent != 0 and check_percent != message_count:
      message_count = check_percent
      print("{}%".format(check_percent))

  dots_array = beta_array

  return dots_array