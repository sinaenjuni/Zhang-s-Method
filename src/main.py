import cv2

def get_image(path):
    return cv2.imread(path, cv2.IMREAD_COLOR)

if __name__ == "__main__":
    ch, cw = 9, 7    # checkboard patterns are 9 row and 7 col.
    square_size = 20 # 20mm

    img = get_image("../data/board0.jpeg")

    cv2.imshow("img", img)
    cv2.waitKey()