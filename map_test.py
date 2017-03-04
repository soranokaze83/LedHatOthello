# coding: UTF-8
import my_util

if my_util.check_map_point(-1,4) == 0:
    print("OK")
else:
    print("NG")

if my_util.check_map_point(0,7) == 0:
    print("OK")
else:
    print("NG")

if my_util.check_map_point(2,9) == 0:
    print("OK")
else:
    print("NG")

data_map = [[0 for x_count in range(8)] for y_count in range(9)]
data_map[3][3] = 1
data_map[3][4] = 2
data_map[4][3] = 2
data_map[4][4] = 1
print(data_map)

print("put check="+str(my_util.check_map_data(data_map, 1)))

