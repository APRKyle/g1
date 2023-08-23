import os.path

import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import json
import struct
import socket
import cv2
matplotlib.use('TkAgg')

def get_angles(data):
    centroid = np.mean(data, axis=0)
    # centroid = data[0]

    translated_points = data - centroid
    covariance_matrix = np.cov(translated_points, rowvar=False)
    eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)
    dominant_eigenvector = eigenvectors[:, np.argmax(eigenvalues)]
    dominant_eigenvector /= np.linalg.norm(dominant_eigenvector)
    pitch = np.arcsin(dominant_eigenvector[2])
    yaw = np.arctan2(dominant_eigenvector[1], dominant_eigenvector[0])
    roll = 0

    pitch_deg = np.degrees(pitch).astype(int)
    yaw_deg = np.degrees(yaw).astype(int)
    roll_deg = np.degrees(roll).astype(int)
    return pitch_deg, yaw_deg, roll_deg

font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.8
font_color = (255, 255, 255)  # White color
thickness = 2
def receive_frame(sock):
    # Receive the size of the data
    size_data = b''
    while len(size_data) < 4:
        size_data += sock.recv(4 - len(size_data))
    size = struct.unpack('<L', size_data)[0]

    # Receive the JSON data
    json_data = b''
    while len(json_data) < size:
        json_data += sock.recv(size - len(json_data))

    # Deserialize the JSON data to retrieve the image and additional data
    data = json.loads(json_data.decode('utf-8'))
    frame = cv2.imdecode(np.frombuffer(data['image'].encode('latin1'), dtype=np.uint8), cv2.IMREAD_COLOR)
    data_array = data['data_array']



    return frame, data_array



receiver_ip = '0.0.0.0'  # Listen on all available interfaces
receiver_port = 5000

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((receiver_ip, receiver_port))
sock.listen(1)


conn, addr = sock.accept()


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Set labels for each axis
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

# Set initial limits for the x, y, and z axes
ax.set_xlim(-50, 30)
ax.set_ylim(-100, 60)
ax.set_zlim(200, 300)

elevation = 90  # Set the elevation angle (default is 30 degrees)
azimuth = 90    # Set the azimuthal angle (default is 45 degrees)
ax.view_init(elevation, azimuth)
plt.ion()  # Turn on interactive mode
import datetime
data_path = r'C:\Users\Andrii\PycharmProjects\GUS\outputs'
dt = datetime.datetime.now()
dir_name = dt.strftime('%Y_%m_%d_%H_%M_%S')
dir_name = os.path.join(data_path, dir_name)

if os.path.exists(os.path.join(data_path, dir_name)):
    pass
else:
    os.mkdir(dir_name)

    video_dir = os.path.join(dir_name, 'video')
    data_dir = os.path.join(dir_name, 'data')

    os.mkdir(video_dir)
    os.mkdir(data_dir)


try:
    with open(os.path.join(data_dir, 'data.json'), 'r') as json_file:
        data_json = json.load(json_file)
except FileNotFoundError:

    existing_data = []
json_file = open(os.path.join(data_dir, 'data.json'), 'w')
frame_id = -1
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec for AVI format
out = cv2.VideoWriter(os.path.join(video_dir, 'output.avi'), fourcc, 30.0, (640, 480))

num_points = 200

y_ground= 0  # Constant y value for all points

x_values = np.linspace(-200, 200, 50)
z_values = np.linspace(0, 400, 50)


# Create a meshgrid of x and z values
x_ground, z_ground = np.meshgrid(x_values, z_values)






try:
    while True:
        # Receive and display the frame, and get the additional data (data_array)

        frame, data = receive_frame(conn)

        frame_id +=1
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        out.write(frame)
        existing_data.append(data)


        ax.cla()
        for id, d in data.items():
            skeleton_3d = np.array(d['skeleton3d'])
            pitch_deg = d['pitch']
            roll_deg = d['roll']
            yaw_def = d['yaw']
            x = skeleton_3d[:, 0]
            y = skeleton_3d[:, 1]
            z = skeleton_3d[:, 2]
            cv2.putText(frame, f'pitch : {pitch_deg}', (50, 50), font, font_scale, font_color, thickness)
            cv2.putText(frame, f'yaw : {yaw_deg}', (50, 100), font, font_scale, font_color, thickness)
            cv2.putText(frame, f'roll : {roll_deg}', (50, 150), font, font_scale, font_color, thickness)
            # b = np.array(d['box']).astype(int)
            # cv2.rectangle(frame, tuple([b[0], b[1]]), tuple([b[2], b[3]]), (0,255,0), 2)
            frame[d['mask'][0], d['mask'][1], :] = (0,90,0)
            for c in d['skeleton']:
                cv2.circle(frame, tuple([int(c[0]), int(c[1])]),3, (0,0,220), 2)
            cv2.circle(frame, tuple([d['top_point'][0], d['top_point'][1]]), 3, (0,255,255)) #top point
            cv2.circle(frame, tuple([d['bot_point'][0], d['bot_point'][1]]), 3, (0,255,255)) #bot point


            ax.scatter(x, y, z, c='r', marker='x')
            ax.scatter(d['top_3d'][0], d['top_3d'][1], d['top_3d'][2],  c = [(1,1,0)], marker = 'o')
            ax.scatter(d['bot_3d'][0], d['bot_3d'][1], d['bot_3d'][2],  c = [(1,1,0)], marker = 'o')
            y_ground = d['bot_3d'][1]


        ax.plot_surface(x_ground, y_ground, z_ground, color='brown', alpha=0.7)

        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.imshow('Received Stream', frame)


        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')

        # Set limits for the x, y, and z axes (you can choose to set them only once outside the loop if they don't change)
        ax.set_xlim(-200, 200)
        ax.set_ylim(-200, 200)
        ax.set_zlim(0, 400)

        plt.draw()
        plt.pause(0.01)  # Pause for 0.5 seconds before the next iteration
        cv2.waitKey(1)
except KeyboardInterrupt:

    with open(os.path.join(data_dir, 'data.json'), 'w') as json_file:
        json.dump(existing_data, json_file, indent=4, separators=(',', ':'))
    conn.close()
    sock.close()
    out.release()
    cv2.destroyAllWindows()


