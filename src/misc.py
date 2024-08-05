import numpy as np
def get_world_point(col, row, square_size):
    y, x = np.meshgrid(np.arange(col), np.arange(row))
    x, y = x.reshape(-1, 1), y.reshape(-1, 1)
    z = np.zeros_like(x)
    ret = np.hstack((x, y, z)) * square_size
    return ret.astype(np.float32)

import cv2
def get_image_point(img, col, row, use_subpix=True):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    gray_img = cv2.equalizeHist(gray_img)

    ret, corners = cv2.findChessboardCorners(gray_img, (col, row), None)

    corners = corners.reshape(-1, 2)
    if use_subpix:
        corners = cv2.cornerSubPix(gray_img,corners, (col, row), (-1,-1), criteria=criteria)
    return ret, corners