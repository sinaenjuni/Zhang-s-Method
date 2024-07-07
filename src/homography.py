import numpy as np
import numpy.linalg as la

def compute_homography(img_point:np.array, obj_point:np.array)->np.array:
    def get_A(img_point, obj_point):
        u, v = img_point
        X, Y, Z = obj_point
        Z = 1
        A = [[X, Y, Z, 0, 0, 0, -u*X, -u*Y, -u*Z],
             [0, 0, 0, X, Y, Z, -v*X, -v*Y, -v*Z]]
        return np.array(A)
    
    assert len(img_point) == len(obj_point) >= 4, "require a minimum four pair-point"
    A = np.stack(list(map(get_A, img_point, obj_point)))
    # A = []
    # for img_point, obj_point in zip(img_point, obj_point):
        # A += [get_A(img_point, obj_point)]
    # A = np.vstack(A)

    _, _, V = la.svd(A) # find nullspace
    H = (V[-1,...] / V[-1,-1]).reshape(3,3) # last row is parameters that we went
    return H

def apply_homography(H:np.array, point_homo:np.array)->np.array:
    homo_point = np.hstack((point_homo, np.ones((point_homo.shape[0], 1))))
    cvt_homo_point = (H@homo_point.T).T
    cvt_point = cvt_homo_point / cvt_homo_point[..., [-1]]
    return cvt_point[:,:2]