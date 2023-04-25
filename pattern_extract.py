import numpy as np
from PIL import Image
from letter_generate import generate_custom_text
import matplotlib.pyplot as plt


''' We know that the Janome machine has a tolerance of 0.1mm. So we scale our point cloud
    accordingly such that each point is at least 0.1mm away, both in X and Y directions.
    The thread color is directly read from the RGB values, choosing the appropriate value
    depending on the max color.
    1. To identify if a given pixel is a color pixel, the channel values are checked,
       using pre-defined filter values.
    2. Each pixel is identified as either Red, Yellow, Green or Blue
'''
def check_pixel(r,g,b):
    pixel_color = 'null' # 'r', 'g', 'b'
    if r >= 200 and g <= 70 and b <= 70:
        pixel_color = 'r'
    if r >= 200 and g >= 200 and b <= 120:
        pixel_color = 'y'
    if r <= 70 and g >= 100 and b <= 70:
        pixel_color = 'g'
    if r <= 70 and g <= 70 and b >= 100:
        pixel_color = 'b'
    return pixel_color

def generate_points(filename,custom_text):

    print("Reading image data...")
    img = np.asarray(Image.open(filename))
    height = np.shape(img)[0]
    width = np.shape(img)[1]
    channels = np.shape(img)[2]

    r_points = []
    g_points = []
    y_points = []
    b_points = []

    for i in range(0,height,2):
        for j in range(0,width,2):
            pixel_color = check_pixel(img[i,j,0], img[i,j,1], img[i,j,2])
            if pixel_color == 'r':
                r_points.append(i)
                r_points.append(j)
                continue
            if pixel_color == 'g':
                g_points.append(i)
                g_points.append(j)
                continue
            if pixel_color == 'b':
                b_points.append(i)
                b_points.append(j)
                continue
            if pixel_color == 'y':
                y_points.append(i)
                y_points.append(j)

    print("Image points generated")
    r_points = np.asarray(r_points,dtype=int).reshape(-1,2)
    g_points = np.asarray(g_points,dtype=int).reshape(-1,2)
    b_points = np.asarray(b_points,dtype=int).reshape(-1,2)
    y_points = np.asarray(y_points,dtype=int).reshape(-1,2)
    k_points = generate_custom_text(custom_text)
    k_points[:,0] = k_points[:,0] + (width/2) - 200
    k_points[:,1] = k_points[:,1] - 480

    plt.scatter(g_points[:,0],g_points[:,1],color='green',s=0.1)
    plt.scatter(r_points[:,0],r_points[:,1],color='red',s=0.1)
    plt.scatter(b_points[:,0],b_points[:,1],color='blue',s=0.1)
    plt.scatter(y_points[:,0],y_points[:,1],color='yellow',s=0.1)
    # plt.xlabel('X Displacement (0.1mm)')
    # plt.ylabel('Y Displacement (0.1mm)')
    # plt.title('Thread Paths')
    plt.scatter(k_points[:,0],k_points[:,1],color='black',s=0.1)
    plt.axis('off')
    plt.show()

    height = height + 480
    width = max(width,640)
    return height,width,r_points,g_points,b_points,y_points,k_points
