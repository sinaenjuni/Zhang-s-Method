import cv2
import numpy as np
import numpy.linalg as la

def get_image(path):
    return cv2.imread(path, cv2.IMREAD_COLOR)

def get_image_point(img, ch, cw, use_subpix=True):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    ret, corners = cv2.findChessboardCorners(gray_img, (ch, cw), None)

    corners = corners.reshape(-1, 2)
    if use_subpix:
        corners = cv2.cornerSubPix(gray_img,corners, (ch, cw), (-1,-1), criteria=criteria)
    return corners

def get_A(src_point, dst_point): 
    xs, ys = src_point
    xd, yd = dst_point
    return np.array([[-xs, -ys, -1, 0, 0, 0, xs*xd, ys*xd, xd],
                     [0, 0, 0, -xs, -ys, -1, xs*yd, ys*yd, yd]])

def compute_homography(src_point, dst_point):
    assert len(src_point) == len(dst_point) >= 4, "require a minimum four pair-point"
    A = np.vstack(list(map(get_A, src_point, dst_point)))
    _, _, V = la.svd(A)
    H = (V[-1,...] / V[-1,-1]).reshape(3,3)
    return H

if __name__ == "__main__":
    ch, cw = 9, 7    # checkboard patterns are 9 row and 7 col.
    square_size = 20 # 20mm

    img0 = get_image("./data/board0.jpeg")
    img1 = get_image("./data/board1.jpeg")
    img_point0 = get_image_point(img0, ch, cw)
    img_point1 = get_image_point(img1, ch, cw)

    H = compute_homography(img_point0, img_point1)

    # H, _ = cv2.findHomography(img_point0, img_point1)
    # print(H)

    # img_point = get_image_point(img, ch, cw)

    # img = cv2.drawChessboardCorners(img, (ch, cw), img_point, True)

    # h, w, _ = img1.shape
    # img1_warped = cv2.warpPerspective(img1, H, (w, h))

    for point in img_point0:
        cv2.circle(img0, point.astype(np.uint16), 10, (255,0,0), -1, cv2.LINE_AA)

        print(point)
        point_homo = np.hstack((point, 1)) # change homogeneous coordinates
        point_homo = H@point_homo # projection
        point_homo /= point_homo[-1] # normalize
        point = point_homo[:2] # change non-homogeneous coordinates
        print(point)
    
        # exit()
        point = point.astype(np.uint16)
        cv2.circle(img1, point, 10, (255,0,0), -1, cv2.LINE_AA)


    img0 = cv2.drawChessboardCorners(img0, (ch, cw), img_point0, True)
    img1 = cv2.drawChessboardCorners(img1, (ch, cw), img_point1, True)

    merged_img = np.hstack((img0, img1))
    cv2.imshow("merged_img", merged_img)
    # cv2.imshow("img1_warped", img1_warped)
    cv2.waitKey()