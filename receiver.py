import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import json
import struct
import socket
import cv2
matplotlib.use('TkAgg')



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
    data_array = np.array(data['data_array'])
    print(data_array)
    # Display the image and use the additional data (data_array) as needed
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.imshow('Received Stream', frame)


    cv2.waitKey(1)

    return frame, data_array



receiver_ip = '0.0.0.0'  # Listen on all available interfaces
receiver_port = 5000

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((receiver_ip, receiver_port))
sock.listen(1)

# Accept incoming connection
conn, addr = sock.accept()

# Create a 3D plot
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

try:
    while True:
        # Receive and display the frame, and get the additional data (data_array)
        frame, data = receive_frame(conn)

        # Extract x, y, and z coordinates from the data_array
        ax.cla()  # Clear the previous plot
        for d in data:
            data_array = np.array(d)

            x = data_array[:, 0]
            y = data_array[:, 1]
            z = data_array[:, 2]



            # Plot the new data in 3D
            ax.scatter(x, y, z, c='r', marker='o')

            # Set labels for each axis (you can choose to set them only once outside the loop if they don't change)
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')

        # Set limits for the x, y, and z axes (you can choose to set them only once outside the loop if they don't change)
        ax.set_xlim(-200, 200)
        ax.set_ylim(-200, 200)
        ax.set_zlim(0, 400)

        plt.draw()
        plt.pause(0.01)  # Pause for 0.5 seconds before the next iteration

except KeyboardInterrupt:
    conn.close()
    sock.close()
    cv2.destroyAllWindows()