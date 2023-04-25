
# Function to create stitch sequence

def getStitchSequence():
    stitches = [128, 2] 	# 128 = escape_character , 2=Move 
    stitches += [0, 0]		# followed by 8 bit displacement X,Y
    #stitches += [206, 206]	# followed by another 8 bit displacement X,Y 
    # Note: Displacements are in 0.1mm units. If number is greater than 128, then it represents
    # a negative distance calculated by subtravcting the number from 256 and multiplying by 0.1mm
 
    for i in range(0,20):
        stitches += [ 10, 0,]   #add ten 1mm stiches going right
    
    stitches += [128, 2]
    stitches += [256-127,0]
    stitches += [128, 2]
    stitches += [256-(200-127),0]

    for i in range(0,20):
        stitches += [0, 246,]   #add ten 1mm stiches going down

    stitches += [128, 16]   # 128 = escape_character , 16=last_stitch 
    return stitches


# Function to create JEF file header

def getJefHeader(num_stitches):
    jefBytes = [    128, 0, 0, 0,   # The byte offset of the first stitch
                    10, 0, 0, 0,   # unknown command
                    ord("2"), ord("0"), ord("2"), ord("1"), #YYYY
                    ord("0"), ord("2"), ord("2"), ord("4"), #MMDD
                    ord("1"), ord("5"), ord("2"), ord("1"), #HHMM
                    ord("0"), ord("0"), 99, 0, #SS00
                      1, 0, 0, 0,   # Thread count nr. (nr of thread changes)
                    (num_stitches) & 0xff, (num_stitches) >> 8 & 0xff, 0, 0, # Number of stitches
                      3, 0, 0, 0, # Sewing machine Hoop
                    # Extent 1
                     50, 0, 0, 0, # Left boundary dist from center (in 0.1mm)
                     50, 0, 0, 0, # Top boundary dist from center (in 0.1mm)
                     50, 0, 0, 0, # Right boundary dist from center (in 0.1mm)
                     50, 0, 0, 0, # Bottom boundary dist from center (in 0.1mm)
                    # Extent 2
                     50, 0, 0, 0, # Left boundary dist from center (in 0.1mm)
                     50, 0, 0, 0, # Top boundary dist from center (in 0.1mm)
                     50, 0, 0, 0, # Right boundary dist from center (in 0.1mm)
                     50, 0, 0, 0, # Bottom boundary dist from center (in 0.1mm)
                    # Extent 3
                     50, 0, 0, 0, # Left boundary dist from center (in 0.1mm)
                     50, 0, 0, 0, # Top boundary dist from center (in 0.1mm)
                     50, 0, 0, 0, # Right boundary dist from center (in 0.1mm)
                     50, 0, 0, 0, # Bottom boundary dist from center (in 0.1mm)
                    # Extent 4
                     50, 0, 0, 0, # Left boundary dist from center (in 0.1mm)
                     50, 0, 0, 0, # Top boundary dist from center (in 0.1mm)
                     50, 0, 0, 0, # Right boundary dist from center (in 0.1mm)
                     50, 0, 0, 0, # Bottom boundary dist from center (in 0.1mm)
                    # Extent 5
                     50, 0, 0, 0, # Left boundary dist from center (in 0.1mm)
                     50, 0, 0, 0, # Top boundary dist from center (in 0.1mm)
                     50, 0, 0, 0, # Right boundary dist from center (in 0.1mm)
                     50, 0, 0, 0, # Bottom boundary dist from center (in 0.1mm)
                      29, 0, 0, 0, # Thread Color (Red)
                     13, 0, 0, 0, # Thread type (unknown)
                ]
    return jefBytes

#Main program combines headers and stich sequence

def main():
    stitchseq = getStitchSequence()
    header = getJefHeader(len(stitchseq)//2)
    data = bytes(header) + bytes(stitchseq)
    with open("square7.jef", "wb") as f:
        f.write(data)

if __name__ == '__main__':
    main()
