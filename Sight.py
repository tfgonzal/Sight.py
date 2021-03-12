# Author: Teofilo Gonzalez
# Usage:    
# python3 Sight.py test.jpg
# Output: outtest.jpg
# Green Dot: Mean of all red pixels
# Blue Dot: Mid point of both X and Y coordinates
# Green Square: Bounding box estimate for the shirt or red clothing of the user
# Blue Square: Box around the max and min of X and Y coordinates
# Important use information: 
# 1: While the program could work on more than just jpg, only use jpg due to how the output file is saved.
# 2: To use with the camera, uncomment lines 23-28


from PIL import Image
import math
import numpy as np
import sys

from time import sleep
from picamera import PiCamera

imageload = sys.argv[1];

# camera = PiCamera()
# camera.resolution = (400,400)
# camera.start_preview()
# sleep(5)
# camera.capture(imageload)
# camera.stop_preview()

def point_draw(x, y, pixel, color):
    pixel[x, y] = color;
    pixel[x+1, y+1] = color;
    pixel[x-1, y-1] = color;
    pixel[x, y-1] = color;
    pixel[x, y-2] = color;
    pixel[x, y+1] = color;
    pixel[x, y+2] = color;
    pixel[x-1, y] = color;
    pixel[x-2, y] = color;
    pixel[x+1, y] = color;
    pixel[x+2, y] = color;
    pixel[x+1, y-1] = color;
    pixel[x-1, y+1] = color;
    
def box_draw(x1, x2, y1, y2, pixel, color):
    x = x1;
    for y in range(y1, y2):
        pixel[x, y] = color;
        
    x = x2;
    for y in range(y1, y2):
        pixel[x, y] = color;
        
    y = y1;
    for x in range(x1, x2):
        pixel[x, y] = color;

    y = y2;
    for x in range(x1, x2):
        pixel[x, y] = color;
    

im = Image.open(imageload, 'r')
pixels = list(im.getdata())
print(im.size);

img = Image.new( 'RGB', (im.size[0]+1, im.size[1]+1), "black")
pixels2 = img.load()

x = 0;
y = 0;
j = 0;
maxy = 0;
maxx = 0;
miny = 0;
minx = 0;
meanx = 0;
meany = 0;
count = 0;
densityx = [];
densityy = [];

for i in range(im.size[0]+1):
    densityy.append(0);
    
for i in range(im.size[1]+1):
    densityx.append(0);

maxdx = 0;
maxdy = 0;
maxdenx = 0;
mindenx = 0;
maxdeny = 0;
mindeny = 0;

for i in pixels:
    if x == im.size[0]-1:
        x = 0;
        y = y + 1;
    else:
        x = x + 1;
        
    if (i[0]+(i[0] / 5) >= i[1] + i[2] and i[0] > 10 and i[1] + i[2] < 250 and i[1] < i[2]):
        count = count + 1;
        meanx = meanx + x;
        meany = meany + y;
        densityx[y] = densityx[y] + 1;
        densityy[x] = densityy[x] + 1;
        pixels2[x, y] = (255, 255, 0);
        if (minx == 0 and x > 0):
            minx = x;
        if (miny == 0 and y > 0):
            miny = y;
        if (x > maxx):
            maxx = x;
        if (x < minx):
            minx = x;
        if (y > maxy):
            maxy = y;
        if (y < miny):
            miny = y;
    else:
        pixels2[x, y] = i;
    
    j = j + 1;


box_draw(minx, maxx, miny, maxy, pixels2, (0, 0, 255))
    
meanx = meanx / count;
meany = meany / count;

meanx = round(meanx);
meany = round(meany);

for i in range(len(densityx)):
    if(densityx[i] > maxdx):
        maxdx = densityx[i];

j = 0;
maxboundx = 0;
y = im.size[1]+1;
for i in range(len(densityx)):
    
    if(densityx[i] > maxdx / 3):
        j = j + 1;
        if(j > maxboundx):
            maxboundx = j;
    else:
        j = 0;
        
j = 0;
for i in range(len(densityx)):
    if(densityx[i] > maxdx / 3):
        j = 0;
        if(maxdenx == 0 and mindenx == 0):
            mindenx = i;
        else:
            maxdenx = i;
    else:
        j = j+1;
        if(j > maxboundx and maxdenx != 0 and mindenx != 0):
            break;
            
for i in range(len(densityy)):
    if(densityy[i] > maxdy):
        maxdy = densityy[i];
            
j = 0;
maxboundy = 0;print(len(densityy))
for i in range(len(densityy)):
    if(densityy[i] > maxdy / 3):
        j = j + 1;
        if(j > maxboundy):
            maxboundy = j;
    else:
        j = 0;
        
j = 0;
for i in range(len(densityy)):
    if(densityy[i] > maxdy / 3):
        j = 0;
        if(maxdeny == 0 and mindeny == 0):
            mindeny = i;
        else:
            maxdeny = i;
    else:
        j = j+1;
        if(j > maxboundy and maxdeny != 0 and mindeny != 0):
            break;
            
print("min: ", mindenx, " max: ", maxdenx);
    
box_draw(mindeny, maxdeny, mindenx, maxdenx, pixels2, (0, 255, 0))

point_draw(meanx, meany, pixels2, (0, 255, 0));

boundx = ((maxx-minx)/2)+minx;
boundy = ((maxy-miny)/2)+miny;

point_draw(round(boundx), round(boundy), pixels2, (0, 0, 255))

img.save("out"+sys.argv[1], "JPEG");

print("Bounds: X: ", mindenx, " -> ", maxdenx, "; Y:", mindeny, " -> ", maxdeny, ";"); 
print("Centering: ", ((((maxdenx - mindenx)/2)+mindenx)/im.size[0]) * 360 - 180);
print("Area: ", (count/((im.size[0]+1)*(im.size[1]+1)))/(0.32080024), " Height: ", (maxdeny-mindeny)/212, " Width: ", (maxdenx-mindenx)/262);
