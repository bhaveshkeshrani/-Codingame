import sys
import math


def get(x=0, y=0):
    global food
    global w
    global h

    current = food[y][x]
    if x + 1 >= w:
        right = 0
    else:
        right = get(x + 1, y)
    if y + 1 >= h:
        down = 0
    else:
        down = get(x, y + 1)
    current += (right, down)[down > right]
    return current


food = []
w, h = [int(i) for i in input().split()]
for i in range(h):
    food.append([])
    for j in input().split():
        food[i].append(int(j))
print(food, file=sys.stderr)
# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)

print(get())