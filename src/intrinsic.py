import numpy as np
import numpy.linalg as la

def compute_intrinsic(H:np.array)->np.array:
    def get_A(H):
        # [h1 h2 h3]
        # [h4 h5 h6]
        # [h7 h8 h9]
        h1 = H[0, 0]
        h2 = H[0, 1]
        h3 = H[0, 2]
        h4 = H[1, 0]
        h5 = H[1, 1]
        h6 = H[1, 2]
        h7 = H[2, 0]
        h8 = H[2, 1]
        h9 = H[2, 2]
        A = [[h1*h2, h1*h5 + h2*h4, h1*h8 + h2*h7, h4*h5, h4*h8 + h5*h7, h7*h8],
            [h1*h1 - h2*h2, 2*h1*h4 - 2*h2*h5, 2*h1*h7 - 2*h2*h8, h4*h4 - h5*h5, 2*h4*h7 - 2*h5*h8, h7*h7 - h8*h8]]
        return np.array(A)
    
    A = np.vstack(list(map(get_A, H)))
    _, _, V = la.svd(A)
    a0, a1, a2, a3, a4, a5 = V[-1,...] # get last row, nullspace 
    KtinvKinv = np.array([[a0, a1, a2],
                            [a1, a3, a4],
                            [a2, a4, a5]])
    # min_eigenvalue = np.min(la.eigvals(KtinvKinv))
    # if min_eigenvalue < 0:
        # KtinvKinv = KtinvKinv + np.eye(3) * (-min_eigenvalue + 1e-6)
    pseudoKinv = la.cholesky(KtinvKinv)
    K = la.inv(pseudoKinv).T
    K /= K[2,2]
    Kinv = la.inv(K)
    return K, Kinv
