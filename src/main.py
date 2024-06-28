import cv2
import numpy as np

def get_image(path):
    return cv2.imread(path, cv2.IMREAD_COLOR)

def get_image_point(img, ch, cw):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    ret, corners = cv2.findChessboardCorners(gray_img, (ch, cw), None)

    corners = corners.reshape(-1, 2)
    corners = cv2.cornerSubPix(gray_img,corners, (ch, cw), (-1,-1), criteria=criteria)
    return corners

if __name__ == "__main__":
    ch, cw = 9, 7    # checkboard patterns are 9 row and 7 col.
    square_size = 20 # 20mm

    img0 = get_image("./data/board0.jpeg")
    img1 = get_image("./data/board1.jpeg")
    img_point0 = get_image_point(img0, ch, cw)
    img_point1 = get_image_point(img1, ch, cw)


    H, _ = cv2.findHomography(img_point0, img_point1, cv2.RANSAC)
    print(H)
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