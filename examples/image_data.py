import cv2
import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt

import sys
sys.path.append("./src")
import files
from homography import compute_homography
from intrinsic import compute_intrinsic
from misc import get_world_point, get_image_point

def get_image(path):
    return cv2.imread(path, cv2.IMREAD_COLOR)

if __name__ == "__main__":
    np.set_printoptions(suppress=True, linewidth=1000)
    VIS = True

    col, row = 7, 9 # checkboard patterns are 9 row and 7 col.
    # col, row = 9, 7 # checkboard patterns are 9 row and 7 col.
    square_size = 20 # 20mm
    world_point = get_world_point(col, row, square_size)

    image_paths = files.get_img_paths("./data/data0/")
    images = list(map(get_image, image_paths))
    image_size = images[0].shape[:2]

    image_points = list(map(get_image_point, images, [col]*len(images), [row]*len(images)))
    image_points = [image_point[1] for image_point in image_points if image_point[0] == True]
    world_points = world_point[None, :].repeat(len(image_points), 0)
        
    Hs = np.stack(list(map(compute_homography, image_points, world_points)))
    K, Kinv = compute_intrinsic(Hs)
    print(K)

    Rs = []
    ts = []
    for i, H in enumerate(Hs):
        # print(f"{'='*15} image {i} {'='*15}")
        r1 = Kinv@H[:, 0]
        r2 = Kinv@H[:, 1]
        r3 = np.cross(r1, r2)
        t = (1/la.norm(r1)) * Kinv@H[:, 2]

        U,D,V = la.svd(np.column_stack([r1, r2, r3]))
        R = U@V
        Rs += [R]
        ts += [t]
    Rs = np.reshape(Rs, (-1, 3,3))
    ts = np.reshape(ts, (-1, 3))


    rms, intrinsics, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(world_points, image_points, image_size, None, None)
    print(intrinsics)
    Rs_gt = np.reshape([cv2.Rodrigues(rvec)[0] for rvec in rvecs], (-1, 3,3) )
    ts_gt = np.reshape(tvecs,(-1,3))

    # compare openCV lib.
    if VIS:
        from visualization import Visualizer
        vis=Visualizer(K, image_size, (col, row), 20)
        for i, (R, t) in enumerate(zip(Rs, ts)):
            vis.add_camera(R, t, i, 'r')
        for i, (R, t) in enumerate(zip(Rs_gt, ts_gt)):
            vis.add_camera(R, t, i, 'b')
        # plt.savefig('out_fig.png', dpi=300)
        vis.show()

