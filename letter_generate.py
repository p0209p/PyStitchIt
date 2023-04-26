from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import numpy as np
import matplotlib.pyplot as plt
import os

def generate_letters():
    print("Preprocessing............\n")
    print("Generating point map for characters using Arial font")
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    for letter in letters:
        img = Image.new('RGB', (220, 220), "white")
        d = ImageDraw.Draw(img)
        loc = os.getcwd()
        font = ImageFont.truetype("arial", 300)
        d.text((2, -55), letter, fill=(0, 0, 0),font=font)
        if letter.islower():
            fullpath = os.path.join(loc,'letters\\letter-lower%s.png' % letter)
            img.save(fullpath, 'png')
        elif letter.isupper():
            fullpath = os.path.join(loc,'letters\\letter-upper%s.png' % letter)
            img.save(fullpath, 'png')
        else:
            fullpath = os.path.join(loc,'letters\\letter-%s.png' % letter)
            img.save(fullpath, 'png')
    print("Done")

def check_black(r):
    if r > 10:
        return False
    else:
        return True

def read_points(letter):
    k_points = []
    if letter.isupper():
        filename = "letters/letter-upper%s.png" % letter
    elif letter.islower():
        filename = "letters/letter-lower%s.png" %letter
    else:
        filename = "letters/letter-%s.png" % letter
    
    img = Image.open(filename)
    img = img.rotate(-90)
    img = np.asarray(img)
    height = np.shape(img)[0]
    width = np.shape(img)[1]
    channels = np.shape(img)[2]

    for i in range(height):
        for j in range(width):
            is_black = check_black(img[i,j,0])
            if is_black:
                k_points.append(i)
                k_points.append(j)

    k_points = np.asarray(k_points,dtype=float).reshape(-1,2)
    return k_points

def generate_custom_text(text):
    print("Generating point map for characters using Arial font")
    img = Image.new('RGB', (480, 480), "white")
    d = ImageDraw.Draw(img)
    loc = os.getcwd()
    font = ImageFont.truetype("arial", 100) # "arial" etc ...
    d.text((2, -10), text, fill=(0, 0, 0),font=font)
    fullpath = os.path.join(loc,'letters/letter-custom.png')
    img.save(fullpath, 'png')

    k_points = []
    filename = "letters/letter-custom.png"

    img = Image.open(filename)
    img = img.rotate(-90)
    img = np.asarray(img)
    height = np.shape(img)[0]
    width = np.shape(img)[1]
    channels = np.shape(img)[2]

    for i in range(height):
        for j in range(width):
            is_black = check_black(img[i,j,0])
            if is_black:
                k_points.append(i)
                k_points.append(j)

    k_points = np.asarray(k_points,dtype=int).reshape(-1,2)
    print("Points generated")
    # plt.scatter(k_points[:,0],k_points[:,1],color='black',s=0.1)
    # plt.show()
    return k_points

#k = generate_custom_text("Piyush")
