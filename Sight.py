from PIL import Image
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

x = maxx;
for y in range(miny, maxy):
    pixels2[x, y] = (0, 255, 0);
    
x = minx;
for y in range(miny, maxy):
    pixels2[x, y] = (0, 255, 0);
    
y = maxy;
for x in range(minx, maxx):
    pixels2[x, y] = (0, 255, 0);

y = miny;
for x in range(minx, maxx):
    pixels2[x, y] = (0, 255, 0);
    
meanx = meanx / count;
meany = meany / count;

round(meanx);
round(meany);

point_draw(meanx, meany, pixels2, (0, 255, 0));

boundx = ((maxx-minx)/2)+minx;
boundy = ((maxy-miny)/2)+miny;

point_draw(round(boundx), round(boundy), pixels2, (0, 0, 255))

img.save("out"+sys.argv[1], "JPEG");

print("Bounds: X: ", minx, " -> ", maxx, "; Y:", miny, " -> ", maxy, ";"); 
print("Centering: ", ((((maxx - minx)/2)+minx)/im.size[0]) * 360 - 180);
