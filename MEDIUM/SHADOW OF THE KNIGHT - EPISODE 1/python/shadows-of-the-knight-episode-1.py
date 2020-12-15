# https://www.codingame.com/ide/puzzle/shadows-of-the-knight-episode-1
import sys
import math
# w: width of the building.
# h: height of the building.
w, h = [int(i) for i in raw_input().split()]
n = int(raw_input())  # maximum number of turns before game over.
x0, y0 = [int(i) for i in raw_input().split()]
minx = miny  = 0
maxx = w - 1 
maxy = h - 1

while True:
    bomb_dir = raw_input()  # the direction of the bombs from batman's current location (U, UR, R, DR, D, DL, L or UL)
    if bomb_dir.find("U")>-1:
        maxy = y0 - 1
    elif bomb_dir.find("D")>-1:
        miny = y0 + 1
    if bomb_dir.find("L")>-1:
        maxx = x0 - 1
    elif bomb_dir.find("R")>-1:
        minx =x0 + 1
    x0 = minx + math.ceil((maxx  - minx)/2)
    y0 = miny + math.ceil((maxy  - miny)/2)
    # the location of the next window Batman should jump to.
    print("{0} {1}".format(int(x0), int(y0)))
