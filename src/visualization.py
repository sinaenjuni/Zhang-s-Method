import numpy as np
import matplotlib.pyplot as plt
import pytransform3d.camera as pc
import pytransform3d.transformations as pt
from pytransform3d.plot_utils import make_3d_axis

class Visualizer:
    def __init__(self, K, image_size=(4032, 2268), cb_size=(7,9), square_size=20):
        # K = np.array([[3362.36309908,   11.94861188, 1921.85838599],
        #                 [   0.,         3363.78896905,  984.52116144],
        #                 [  -0.,            0.,            1.        ]])
        # R = np.array([[ 0.99809887, -0.06104853, 0.00846914,],
        #             [ 0.04577289, 0.82624237, 0.56145204,],
        #             [-0.04127338, -0.55999698, 0.82746594]])
        # t = np.array([-68.89861393, -57.46334559, 428.33907405])
        
        self.K = K
        self.virtual_image_distance = 100
        self.sensor_size = (K[0,2], K[1,2])
        self.image_size = image_size
        self.col, self.row = cb_size
        self.square_size = square_size

        self.fig = plt.figure(figsize=(12, 10))
        self.ax = make_3d_axis(1, unit="m")
        # self.ax = make_3d_axis(1, 111, unit="m")
        # ax = fig.add_subplot(projection='3d')
        self.ax.set_xlim(0,500)
        self.ax.set_ylim(0,500)
        self.ax.set_zlim(-500,0)
        self.ax.view_init(elev=-143, azim=-43)

        self.world_grid = pc.make_world_grid(
            n_lines=self.col+1, n_points_per_line=100, 
            xlim=(0, self.row*self.square_size), ylim=(0, self.col*square_size))
        self.ax.scatter(
            self.world_grid[:, 0], self.world_grid[:, 1], self.world_grid[:, 2], s=5, alpha=0.5)
        # ax.scatter(world_grid[-1, 0], world_grid[-1, 1], world_grid[-1, 2], color="r")

        pt.plot_transform(self.ax, s=50) # base axis

        

       
    def convert_cam2world(self, R, t):
        cam2world = np.eye(4)
        cam2world[:3, :3] = R.T
        cam2world[:3, -1] = -(R.T@t)
        return cam2world

    def add_camera(self, R, t, camera_name=None):
        cam2world = self.convert_cam2world(R, t)
        pt.plot_transform(self.ax, A2B=cam2world, s=50, name=camera_name if camera_name is not None else None)
        pc.plot_camera(self.ax, cam2world=cam2world, M=self.K, sensor_size=self.sensor_size,
                        virtual_image_distance=self.virtual_image_distance)
        # self.add_imageview(cam2world)
        
    def add_imageview(self, cam2world):
        image_grid = pc.world2image(self.world_grid, cam2world, self.sensor_size, self.image_size, focal_length=self.K[0,0], kappa=0.4)
        ax = plt.subplot(122, aspect="equal")
        ax.set_title("Camera image")
        ax.set_xlim(0, self.image_size[0])
        ax.set_ylim(0, self.image_size[1])
        ax.scatter(image_grid[:, 0], -(image_grid[:, 1] - self.image_size[1]))
        ax.scatter(image_grid[-1, 0], -(image_grid[-1, 1] - self.image_size[1]), color="r")

    def show(self):
        plt.show()


if __name__ == "__main__":
    K = np.array([[3362.36309908,   11.94861188, 1921.85838599],
                    [   0.,         3363.78896905,  984.52116144],
                    [  -0.,            0.,            1.        ]])
    R = np.array([[ 0.99809887, -0.06104853, 0.00846914,],
                [ 0.04577289, 0.82624237, 0.56145204,],
                [-0.04127338, -0.55999698, 0.82746594]])
    t = np.array([-68.89861393, -57.46334559, 428.33907405])
    vis=Visualizer(K)
    vis.add_camera(R, t)
    vis.show()





