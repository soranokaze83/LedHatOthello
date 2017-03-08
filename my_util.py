# coding: UTF-8
import unicornhat as unicorn
import random
import time

# global変数宣言
# カーソルマップ作成
cursor_map_x = [[0 for cursor_y_count in range(3)] for cursor_x_count in range(3)]
cursor_map_x[0][0] = -1
cursor_map_x[0][1] = 0
cursor_map_x[0][2] = +1
cursor_map_x[1][0] = -1
cursor_map_x[1][1] = 0
cursor_map_x[1][2] = +1
cursor_map_x[2][0] = -1
cursor_map_x[2][1] = 0
cursor_map_x[2][2] = +1
cursor_map_y = [[0 for cursor_y_count in range(3)] for cursor_x_count in range(3)]
cursor_map_y[0][0] = -1
cursor_map_y[0][1] = -1
cursor_map_y[0][2] = -1
cursor_map_y[1][0] = 0
cursor_map_y[1][1] = 0
cursor_map_y[1][2] = 0
cursor_map_y[2][0] = +1
cursor_map_y[2][1] = +1
cursor_map_y[2][2] = +1

# マップ位置に対する得点を設定する
map_data_score = [
[9,0,7,7,7,7,0,9],
[0,0,2,2,2,2,0,0],
[7,2,6,5,5,6,2,7],
[7,2,5,0,0,5,2,7],
[7,2,5,0,0,5,2,7],
[7,2,6,5,5,6,2,7],
[0,0,2,2,2,2,0,0],
[9,0,7,7,7,7,0,9]
]
print(map_data_score)

def check_map_point( x, y ):
#    print("x=" + str(x) + " y=" + str(y))
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

def check_map_minmax( data_size, size_min, size_max ):
    if data_size == size_max:
        return size_min
    if data_size == size_min -1:
        return size_max -1
    return data_size

#def view_map_data( data_map, myNumber ):

# ２次元配列をチェックしコマが置けるか判定する。
def check_map_data( data_map, myNumber, x_point, y_point ):
    #print('list1の長さは{}です'.format(length))
    print(len(data_map))     #y
    print(len(data_map[0]))  #x

    count_y = len(data_map)     #y
    count_x = len(data_map[0])  #x
    
    # コマの色変えフラグを初期化
    mycolor_change_flag = 0

    # ひっくり返せるコマ数最大値を初期化
    max_color_change_count = 0
    x_big_point = 0
    y_big_point = 0

    for y in range(count_y):
        for x in range(count_x):
            # ひっくり返せるコマの数を初期化
            color_change_count = 0

            #if data_map[y][x] == 0:
            #    unicorn.set_pixel(x, y, 0,0,0)
            #    unicorn.show()

            for cursor_y_count in range(3):
                for cursor_x_count in range(3):
                    # フィールドの外に出る場合は、スキップする
                    cursor_point_x = check_cursor_x_point( cursor_x_count, cursor_y_count )
                    cursor_point_y = check_cursor_y_point( cursor_x_count, cursor_y_count )
                    if check_map_point(x + cursor_point_x,y + cursor_point_y) == -1:
                    	continue

                    if data_map[y + cursor_point_y][x + cursor_point_x] == myNumber:
                        # 何もしない。
                        pass
                    # カーソルの周りに空のマスを見つけた場合
                    elif data_map[y + cursor_point_y][x + cursor_point_x] == 0:
                        # 何もしない。
                        pass
                    else:

                        if data_map[y][x] == 0:
                            #print("x:" + str(x) + " y:"+ str(y) + " data:" + str(data_map[y][x]))

                            # コマ入れ替えフラグ初期化
                            color_change_flag = 0
                            # チェック回数のカウント初期化
                            data_check_count = 1
                            # 画面端までループ
                            while 1:
                                # サイズセット
                                check_x = cursor_point_x * data_check_count
                                check_y = cursor_point_y * data_check_count
                                #print("check_x=" + str(x + check_x) +" check_y=" + str(y + check_y))
                                # フィールドの外に出る場合は、対象なしで終了
                                if check_map_point(x + check_x, y + check_y) == -1:
		                        	break
                                # 終端のマスが空の場合、対象なしで終了
                                if data_map[y + check_y][x + check_x] == 0:
                                    break
                                # 自身と同じ色のコマが存在する場合
                                if data_map[y + check_y][x + check_x] == myNumber:
                                    # 対象有りのフラグを立てて終了
                                    color_change_flag = 1
                                    # ひっくり返せるコマの数を合算
                                    color_change_count = color_change_count + data_check_count - 1
                                    break
                                # 上記以外の場合(自身と異なる色のコマが存在する場合)
                                # 更に次のコマを確認するため、ループ続行する
    
                                # チェックカウントを更新
                                data_check_count = data_check_count + 1
                            
                            # コマ入れ替えフラグが有効の場合
                            if color_change_flag == 1:
                                # コマ設置有無フラグを有効に変更
                                mycolor_change_flag = 1
                                #return data_check_count
                                
                                # 設置箇所のコマの色を設定
                                #unicorn.set_pixel(x, y, set_anime_colorR,set_anime_colorG,set_anime_colorB)
                                unicorn.set_pixel(x, y, 255,150,80)
                                # はさんだ対象コマの色も変更する
                                # unicorn.set_pixel(x + cursor_point_x * data_check_count, y + cursor_point_y * data_check_count, set_anime_colorR,set_anime_colorG,set_anime_colorB)
                                # 黄色色変え

                                unicorn.show()
                                time.sleep(0.1)
                            else:
                                pass
                                #return 0
            if mycolor_change_flag != 0:
                if color_change_count != 0:
                    print(color_change_count)
                    # ひっくり返せるコマにマスに対するスコアを加算する
                    color_change_count = color_change_count + map_data_score[y][x]
                    print(color_change_count)
                    # 最大カウントを超えるかチェック。
                    if color_change_count > max_color_change_count:
                        # 最大カウントを超えた場合は、最大値を記録し、x、yを更新する。
                        max_color_change_count = color_change_count
                        print("x = " + str(x) + " y = " + str(y))
                        x_big_point = x
                        y_big_point = y
                    # 最大カウントと同じ場合。
                    if color_change_count == max_color_change_count:
                        # 最大と同じ値の場合は、置き換えるを実施するかをランダムで決める。
                        if random.randint(0,1) == 1:
                            print("random!")
                            # 最大カウントを超えた場合は、最大値を記録し、x、yを更新する。
                            max_color_change_count = color_change_count
                            print("x = " + str(x) + " y = " + str(y))
                            x_big_point = x
                            y_big_point = y
                        else:
                            print("not random!!")

    # コマ置きが有効な場合、コマが一番ひっくり返せる位置にコマを置く。
    if mycolor_change_flag != 0:
        #data_map[y_big_point][x_big_point] = myNumber
        x_point = x_big_point
        y_point = y_big_point
        print("x_point = " + str(x_point) + " y_point = " + str(y_point))

    # コマの色変えフラグを戻り値に設定
    print(mycolor_change_flag)
    return mycolor_change_flag, x_point, y_point



# カーソルの周りチェック
def check_cursor_x_point( cursor_x, cursor_y ):
    return cursor_map_x[cursor_y][cursor_x]

def check_cursor_y_point( cursor_x, cursor_y ):
    return cursor_map_y[cursor_y][cursor_x]

if(__name__ == '__main__'):
    print('my_util.py: loaded as script file')
