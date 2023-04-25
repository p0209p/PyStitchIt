# PyStitchIt
PyStitchIt is a Python-based software to generate Janome Embroidery File format (JEF) to stitch a user-specified image on a fabric. The software supports 5 colors: Red, Green, Blue, Yellow and Black. A user specified text can also be added at the bottom of the pattern !

## How does it work ?

The software reads the RGB channels of each pixel of an image and classifies them as Red, Green Blue and Yellow or Black. Once the pixel can be classified, the thread paths can be generated.

