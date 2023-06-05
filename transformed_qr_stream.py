import cv2

import numpy as np
from calibration.QRTracker import Tracker
from subs.Camera import Camera
from subs.Pather import Pather
from subs.VideoInterface import Streamer


def transform(point, af_mat, trans_mat):

    af_mat = np.array(af_mat)
    trans_mat = np.array(trans_mat)
    trans_mat = trans_mat.reshape((-1,1))
    tr = np.concatenate((af_mat, trans_mat), axis = 1)
    tr = np.vstack((tr, [0,0,0,0]))


    point = np.matmul(tr, point)

    point = np.delete(point, -1)
    return point, tr



def calculate_matrices(cam_points, rob_points):
    out = np.array(rob_points)

    B = np.concatenate(cam_points, axis = 1)

    D = 1.0/np.linalg.det(B)
    entry = lambda r,d: np.linalg.det(np.delete(np.vstack([r, B]), (d+1), axis=0))
    M = [[(-1)**i * D * entry(R, i) for i in range(4)] for R in np.transpose(out)]
    A, t = np.hsplit(np.array(M), [4-1])
    t = np.transpose(t)[0]
    # output
    print("Affine transformation matrix:\n", A)
    print("Affine transformation translation vector:\n", t)
    # unittests

    return A, t

def test():
    p_1_c = [1,1,2,1]
    p_2_c = [2,3,0,1]
    p_3_c = [3,2,-2,1]
    p_4_c = [-2,2,3,1]


    point_cam_1 = np.array(p_1_c).reshape((-1,1))
    point_cam_2 = np.array(p_2_c).reshape((-1,1))
    point_cam_3 = np.array(p_3_c).reshape((-1,1))
    point_cam_4 = np.array(p_4_c).reshape((-1,1))

    affine_mat = [[4,6,1], [6,98,8], [35,1,5]]
    trans_mat = [5,4,0]

    point_rob_1, _= transform(point_cam_1,affine_mat, trans_mat)
    point_rob_2, _ = transform(point_cam_2, affine_mat, trans_mat)
    point_rob_3, _ = transform(point_cam_3,affine_mat, trans_mat)
    point_rob_4, _ = transform(point_cam_4, affine_mat, trans_mat)

    cam_points = (point_cam_1, point_cam_2, point_cam_3, point_cam_4)
    rob_points = [point_rob_1, point_rob_2, point_rob_3, point_rob_4]
    A,t = calculate_matrices(cam_points, rob_points)




A = np.array([[-1.2121212121212195,2.424242424242439,-0.6060606060605876],
[-6.772727272727248,6.5454545454545325,-1.6363636363635936],
[5.530303030303041,-6.060606060606071,1.5151515151515067]])
t = np.array([80.00000000000159,-249.49999999999866,401.4999999999996])
camera = Camera()
tracker = Tracker(camera=camera)
camera.initCamera()
output = Streamer(ip='192.168.1.108')
output.initStreamer()

pather = Pather(min_lenght = 0, min_dist = 10000000)

while True:
    camera.getData()
    c = tracker.get_coordinate()
    if c is not None:
        cords = pather._transformIntoRobot(coord=c)
    else:
        cords = None
    print(cords)




