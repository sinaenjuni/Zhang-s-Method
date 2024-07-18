import cv2
import numpy as np
from glob import glob

paths = glob("./data/data0/*.jpeg")

imgs = []
T = []
for i in range(12):
    imgs += [cv2.imread(paths[i], cv2.IMREAD_COLOR)]
imgs = np.array(imgs)
splited = np.split(imgs,3,0); print(np.shape(splited))
merged = np.hstack(splited)
merged = np.hstack(merged)
# print(np.shape(merged))
# print(np.hstack())
cv2.imwrite("./output.jpeg", merged)

cv2.imshow("", merged)
cv2.waitKey()