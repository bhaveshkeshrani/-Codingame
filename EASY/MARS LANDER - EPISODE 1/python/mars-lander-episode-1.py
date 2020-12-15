# https://www.codingame.com/ide/puzzle/mars-lander-episode-1
surface_n = int(raw_input())
land_x_prev = land_y_prev = 0
landing_start = 0
landing_end = 7000
landing_height = 0
for i in range(surface_n):
    land_x, land_y = [int(j) for j in raw_input().split()]
    if(land_x_prev != 0 and land_y_prev == land_y):
        landing_height = land_y
        landing_start = land_x_prev
        landing_end = land_x
    land_x_prev, land_y_prev = land_x, land_y
while True:
    # h_speed: the horizontal speed (in m/s), can be negative.
    # v_speed: the vertical speed (in m/s), can be negative.
    # fuel: the quantity of remaining fuel in liters.
    # rotate: the rotation angle in degrees (-90 to 90).
    # power: the thrust power (0 to 4).
    x, y, h_speed, v_speed, fuel, rotate, power = [int(i) for i in raw_input().split()]
    if(landing_start<x<landing_end):
        dist = y-landing_height
        if v_speed<-35:
            power = 4
        else:
            power = 3
        if(dist>1200 and v_speed>-45):
            power = int(power*(1-dist/3000))
    # 2 integers: rotate power. rotate is the desired rotation angle (should be 0 for level 1), power is the desired thrust power (0 to 4).
    print("0 "+str(power))

