# coding: UTF-8
def check_map_point( x, y ):
    print("x=" + str(x) + " y=" + str(y))
	# エラー条件と一致する場合、異常終了
    if x <= -1:
    	return -1
    if x >= 8:
    	return -1
    if y <= -1:
    	return -1
    if y >= 8:
    	return -1
	# エラー条件以外の場合、正常終了
    return 0

if(__name__ == '__main__'):
    print('my_util.py: loaded as script file')
