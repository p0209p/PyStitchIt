from pattern_extract import *
# Function to create stitch sequence

'''
    Each pixel increment is read as 0.1mm in each of x and y directions.
    Based on this calculation, for 1024x1024 image, the software gives a
    102.4mm X 102.4mm pattern, which will fit in the limits (200mm x 200mm) of the sewing machine
'''
# Reads the points for each of Red, Green, Blue, Yellow and Custom Text repectively


# Returns steps if the point difference exceeds the expected value of < 128 for positive integers
def get_step(current_pos,target_pos):
    xc = current_pos[0]
    yc = current_pos[1]
    xt = target_pos[0]
    yt = target_pos[1]

    x = []
    y = []

    xdiff = abs(xt - xc)
    ydiff = abs(yt - yc)

    if xdiff < 128 and ydiff < 128:
        x.append(xdiff)
        y.append(ydiff)
    elif xdiff >= 128 and ydiff < 128:
        steps = xdiff // 127
        for i in range(steps):
            x.append(128)
            y.append(2)
            x.append(127)
            if i == 0:
                y.append(ydiff)
            else:
                y.append(0)
        x.append(xdiff - steps*127)
        y.append(0)
    elif xdiff < 128 and ydiff >= 128:
        steps = (ydiff) // 127
        for i in range(steps):
            x.append(128)
            y.append(2)
            y.append(127)
            if i == 0:
                x.append(xdiff)
            else:
                x.append(0)
        y.append(ydiff - steps*127)
        x.append(0)
    else:
        steps_x = (xdiff) // 127
        steps_y = (ydiff) // 127
        for i in range(steps_y):
            x.append(128)
            y.append(2)
            y.append(127)
            x.append(0)
        for i in range(steps_x):
            x.append(128)
            y.append(2)
            x.append(127)
            y.append(0)

        y.append(ydiff - steps_y*127)
        x.append(xdiff - steps_x*127)

    if target_pos[0] - current_pos[0] < 0:
        for i in range(len(x)):
            if x[i]!=0:
                x[i] = 256 - x[i]
    
    for i in range(len(x)):
        if target_pos[1] - current_pos[1] < 0 and x[i] != 128 and y[i]!=0:
            y[i] = 256 - y[i]  
    return x,y

def getStitchSequence(filename,custom_text="Piyush"):
    height,width,r_points,g_points,b_points,y_points,k_points = generate_points(filename,custom_text)
    stitches = [128, 2] 	# 128 = escape_character , 2=Move 
    stitches += [0, 0]		# followed by 8 bit displacement X,Y
    current_pos = [0,0]
    # Stitch using Red Thread
    for i in range(np.shape(r_points)[0]):
        x,y = get_step(current_pos, [r_points[i,0],r_points[i,1]])
        current_pos =  [r_points[i,0],r_points[i,1]]
        for j in range(len(x)):
            stitches += [x[j], y[j]]
    # Note: Displacements are in 0.1mm units. If number is greater than 128, then it represents
    # a negative distance calculated by subtravcting the number from 256 and multiplying by 0.1mm
    
    # Change thread to Green
    stitches += [128, 1] # 128 = escape_character -> 1 = Change to next thread in list

    for i in range(np.shape(g_points)[0]):
        x,y = get_step(current_pos, [g_points[i,0],g_points[i,1]])
        current_pos =  [g_points[i,0],g_points[i,1]]
        for j in range(len(x)):
            stitches += [x[j], y[j]]

    # Change thread to Blue
    stitches += [128, 1] # 128 = escape_character -> 1 = Change to next thread in list

    for i in range(np.shape(b_points)[0]):
        x,y = get_step(current_pos, [b_points[i,0],b_points[i,1]])
        current_pos =  [b_points[i,0],b_points[i,1]]
        for j in range(len(x)):
            stitches += [x[j], y[j]]

    # Change thread to Yellow
    stitches += [128, 1] # 128 = escape_character -> 1 = Change to next thread in list

    for i in range(np.shape(y_points)[0]):
        x,y = get_step(current_pos, [y_points[i,0],y_points[i,1]])
        current_pos =  [y_points[i,0],y_points[i,1]]
        for j in range(len(x)):
            stitches += [x[j], y[j]]

    # Change thread to Black for Custom Text
    stitches += [128, 1] # 128 = escape_character -> 1 = Change to next thread in list

    for i in range(np.shape(k_points)[0]):
        x,y = get_step(current_pos, [k_points[i,0],k_points[i,1]])
        current_pos =  [k_points[i,0],k_points[i,1]]
        for j in range(len(x)):
            stitches += [x[j], y[j]]

    stitches += [128, 16]   # 128 = escape_character , 16=last_stitch 
    return height,width,stitches


# Function to create JEF file header

def getJefHeader(num_stitches,height,width):
    jefBytes = [    128, 0, 0, 0,   # The byte offset of the first stitch
                    10, 0, 0, 0,   # unknown command
                    ord("2"), ord("0"), ord("2"), ord("3"), #YYYY
                    ord("0"), ord("3"), ord("1"), ord("3"), #MMDD
                    ord("1"), ord("5"), ord("3"), ord("9"), #HHMM
                    ord("0"), ord("0"), 99, 0, #SS00
                     7, 0, 0, 0,   # Thread count nr. (nr of thread changes)
                    (num_stitches) & 0xff, (num_stitches) >> 8 & 0xff, 0, 0, # Number of stitches
                      3, 0, 0, 0, # Sewing machine Hoop
                    # Extent 1
                     127, 0, 0, 0, # Left boundary dist from center (in 0.1mm)
                     127, 0, 0, 0, # Top boundary dist from center (in 0.1mm)
                     127, 0, 0, 0, # Right boundary dist from center (in 0.1mm)
                     127, 0, 0, 0, # Bottom boundary dist from center (in 0.1mm)
                    # Extent 2
                     127, 0, 0, 0, # Left boundary dist from center (in 0.1mm)
                     127, 0, 0, 0, # Top boundary dist from center (in 0.1mm)
                     127, 0, 0, 0, # Right boundary dist from center (in 0.1mm)
                     127, 0, 0, 0, # Bottom boundary dist from center (in 0.1mm)
                    # Extent 3
                     127, 0, 0, 0, # Left boundary dist from center (in 0.1mm)
                     127, 0, 0, 0, # Top boundary dist from center (in 0.1mm)
                     127, 0, 0, 0, # Right boundary dist from center (in 0.1mm)
                     127, 0, 0, 0, # Bottom boundary dist from center (in 0.1mm)
                    # Extent 4
                     127, 0, 0, 0, # Left boundary dist from center (in 0.1mm)
                     127, 0, 0, 0, # Top boundary dist from center (in 0.1mm)
                     127, 0, 0, 0, # Right boundary dist from center (in 0.1mm)
                     127, 0, 0, 0, # Bottom boundary dist from center (in 0.1mm)
                    # Extent 5
                     127, 0, 0, 0, # Left boundary dist from center (in 0.1mm)
                     127, 0, 0, 0, # Top boundary dist from center (in 0.1mm)
                     127, 0, 0, 0, # Right boundary dist from center (in 0.1mm)
                     127, 0, 0, 0, # Bottom boundary dist from center (in 0.1mm)
                     29, 0, 0, 0, # Thread Color (Red)
                     5, 0, 0, 0, # Thread Color (Green)
                     26, 0, 0, 0, # Thread Color (Blue)
                     48, 0, 0, 0, # Thread Color (Yellow)
                     1, 0, 0, 0, # Thread Color (Black)
                     13, 0, 0, 0, # Thread type (unknown)
                ]
    return jefBytes

#Main program combines headers and stich sequence

def main():
    filename = input("Enter the file name of the image: ") #white_background/Rangoli_design_7_modified.png"
    custom_text = input("Enter the custom text to be entered: ")
    height,width,stitchseq = getStitchSequence(filename,custom_text)
    #print(len(stitchseq)//2)
    #print(np.max(np.asarray(stitchseq)))
    header = getJefHeader(len(stitchseq)//2,height,width)
    data = bytes(header) + bytes(stitchseq)
    with open("Pattern.jef", "wb") as f:
        f.write(data)
    print("File generated. Saved as Pattern.jef")

if __name__ == '__main__':
    main()
