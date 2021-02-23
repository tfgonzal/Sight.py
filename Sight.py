# Author: Teofilo Gonzalez
# Usage:    
# python3 Sight.py test.jpg
# Output: outtest.jpg
# Green Dot: Mean of all red pixels
# Blue Dot: Mid point of both X and Y coordinates
# Blue Square: Box around the max and min of X and Y coordinates

from PIL import Image
import math
import numpy as np
import sys

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
    

im = Image.open(sys.argv[1], 'r')
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
for i in pixels:
    if x == im.size[0]-1:
        x = 0;
        y = y + 1;
    else:
        x = x + 1;
        
    if (i[0] >= i[1] + i[2] and i[0] > 100 and i[1] + i[2] < 250 and i[1] < i[2]):
        count = count + 1;
        meanx = meanx + x;
        meany = meany + y;
        #listx.append(x);
        #listy.append(y);
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

#sdx = 0;
#sdy = 0;

#for i in listx:
#    sdx = sdx + (listx[i]-meanx)*(listx[i]-meanx);
#    sdy = sdy + (listy[i]-meany)*(listy[i]-meany);
    
#sdx = sdx / count;
#sdy = sdy / count;

#sdx = math.sqrt(sdx);
#sdy = math.sqrt(sdy);

#sdx = round(sdx);
#sdy = round(sdy);

meanx = round(meanx);
meany = round(meany);

#lminx = meanx - 3*sdx;
#lmaxx = meanx + 3*sdx;
#lminy = meany - 3*sdy;
#lmaxy = meany + 3*sdy;
#if(lminx < 0):
#    lminx = 0;
#if(lminy < 0):
#    lminy = 0;
#if(lmaxx > im.size[0]):
#    lmaxx = im.size[0];
#if(lmaxy > im.size[1]):
#    lmaxy = im.size[1];
    
#box_draw(lminx, lmaxx, lminy, lmaxy, pixels2, (0, 255, 0))

point_draw(meanx, meany, pixels2, (0, 255, 0));

boundx = ((maxx-minx)/2)+minx;
boundy = ((maxy-miny)/2)+miny;

point_draw(round(boundx), round(boundy), pixels2, (0, 0, 255))

img.save("out"+sys.argv[1], "JPEG");

print("Bounds: X: ", minx, " -> ", maxx, "; Y:", miny, " -> ", maxy, ";"); 
print("Centering: ", ((((maxx - minx)/2)+minx)/im.size[0]) * 360 - 180);
