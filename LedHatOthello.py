# coding: UTF-8

import time
import random

import unicornhat as unicorn
import sys
import termios

import my_util

unicorn.set_layout(unicorn.AUTO)
unicorn.rotation(0)
unicorn.brightness(0.5)
width,height=unicorn.get_shape()

#標準入力のファイルディスクリプタを取得
fd = sys.stdin.fileno()

#fdの端末属性をゲットする
#oldとnewには同じものが入る。
#newに変更を加えて、適応する
#oldは、後で元に戻すため
old = termios.tcgetattr(fd)
new = termios.tcgetattr(fd)

#new[3]はlflags
#ICANON(カノニカルモードのフラグ)を外す
new[3] &= ~termios.ICANON
#ECHO(入力された文字を表示するか否かのフラグ)を外す
new[3] &= ~termios.ECHO

# カーソル位置初期化
x=0
y=0
# カーソル処理化
myNumber = 1

#colorR = random.randint(1,255)
#colorG = random.randint(1,255)
#colorB = random.randint(1,255)
colorR = 0
colorG = 255
colorB = 0

colorR_1 = 255
colorG_1 = 0
colorB_1 = 0

colorR_2 = 0
colorG_2 = 0
colorB_2 = 255

myCursorColorR_1 = 255
myCursorColorG_1 = 51
myCursorColorB_1 = 153

myCursorColorR_2 = 51
myCursorColorG_2 = 204
myCursorColorB_2 = 255

print("red:" + str(colorR))
print("green:" + str(colorG))
print("blue:" + str(colorB))

unicorn.set_pixel(x, y, int(colorR_1), int(colorG_1), int(colorB_1))
#unicorn.set_pixel(x, y, colorR, colorG, colorB)
unicorn.show()

# 画面マップ作成
data_map = [[0 for x_count in range(width)] for y_count in range(height)]
data_map[3][3] = 1
data_map[3][4] = 2
data_map[4][3] = 2
data_map[4][4] = 1
print(data_map)


# 配列設定値に応じてLEDの表示変更
for y_count in range(height):
    for x_count in range(width):
        if data_map[y_count][x_count] == 1:
            unicorn.set_pixel(x_count, y_count, int(colorR_1*0.4), int(colorG_1*0.4), int(colorB_1*0.4))
        if data_map[y_count][x_count] == 2:
            unicorn.set_pixel(x_count, y_count, int(colorR_2*0.4), int(colorG_2*0.4), int(colorB_2*0.4))
unicorn.show()

try:
    # 書き換えたnewをfdに適応する
    termios.tcsetattr(fd, termios.TCSANOW, new)

	# 無限ループ
    while 1:
    	#print("ループ開始")
    	# CPU対戦機能を実装する場合、この位置にて分岐処理を追加する
    	# 青色ならCPU側の処理を実施しchにスペースをセット、
    	# else側にキーボード入力受付を作成する。
    	# 将来的には、目的のマスまで移動する処理も追加する。
    	
    	# コンピュータにて処理する内容は、盤面全体の内容を確認し、
    	# それぞれのマスに得点を付ける。その後、得点の最も多いマスに対して、コマを置く。
    	# コマが置けない場所は、0点とし、コマを置く場所が全て0点の場合、PASSする。
    	
		# PASS処理は、赤、青関係なく先に実施する必要がある。
		# どちらもPASSになるような場合はそこで試合終了ですよ。    	
    	
    	# もう少し具体的に。
    	# 8x8マス全部に対してチェックを行う。
    	# コマが既に配置されているマスは、スキップ。
    	# マスに対して、８方向チェック＋何コマ取れるかチェックを実施(通常の配置確認)して、
    	# 配置不可ならスキップ、配置可能なら取れるコマを得点として記録する。
    	# 最終的に得点が一番多いマスにコマを置く。
    	# 最初は、記録するのが面倒なので得点が多いところで更新(マスだけ覚える)で良いかも。
		
        # 位置情報が更新完了時点でLEDを点灯する。
        print("x:" + str(x) + " y:" + str(y))
        if data_map[y][x] == 0:
            if myNumber == 1:
                unicorn.set_pixel(x,y,colorR_1,colorG_1,colorB_1)
            if myNumber == 2:
                unicorn.set_pixel(x,y,colorR_2,colorG_2,colorB_2)
        if data_map[y][x] == 1:
            if myNumber == 1:
                unicorn.set_pixel(x,y,int(colorR_1*0.7), int(colorG_1*0.7), int(colorB_1*0.7))
            else:
                unicorn.set_pixel(x, y, myCursorColorR_1, myCursorColorG_1, myCursorColorB_1)
        if data_map[y][x] == 2:
            if myNumber == 2:
                unicorn.set_pixel(x,y,int(colorR_2*0.7), int(colorG_2*0.7), int(colorB_2*0.7))
            else:
                unicorn.set_pixel(x, y, myCursorColorR_2, myCursorColorG_2, myCursorColorB_2)
        unicorn.show()

        # キーボードから入力を受ける。
        # lfalgsが書き換えられているので、エンターを押さなくても次に進む。echoもしない
        ch = sys.stdin.read(1)

        # キーボードから入力受付完了のタイミングで現在のLEDを消灯する。
        unicorn.set_pixel(x , y, 0, 0, 0)
        unicorn.show()
    
        # WASZキー押下時の処理
        if ch =='w' or ch =='8':
            sys.stdout.write("↑ ")
            y =y-1
    
        if ch =='a' or ch =='4':
            sys.stdout.write("← ")
            x=x-1
    
        if ch =='s' or ch =='6':
            sys.stdout.write("→ ")
            x=x+1
    
        if ch =='z' or ch =='2':
            sys.stdout.write("↓ ")
            y=y+1

        # スペースキー押下時の処理
        if ch ==' ' or ch =='5':
            print('!')
            # カーソルの場所が空の場合
            if data_map[y][x] == 0:
                # コマ配置有無フラグ初期化
                data_set_flag = 0
                
                # カーソルの周りサーチ
                for cursor_y_count in range(3):
                    for cursor_x_count in range(3):
                        # フィールドの外に出る場合は、スキップする
                        #cursor_point_x = cursor_map_x[cursor_y_count][cursor_x_count]
                        #cursor_point_y = cursor_map_y[cursor_y_count][cursor_x_count]
                        cursor_point_x = my_util.check_cursor_x_point( cursor_x_count, cursor_y_count )
                        cursor_point_y = my_util.check_cursor_y_point( cursor_x_count, cursor_y_count )
                        if my_util.check_map_point(x + cursor_point_x,y + cursor_point_y) == -1:
                        	continue

                        sys.stdout.write(str(data_map[y + cursor_point_y][x + cursor_point_x]))
                        # カーソルの周りに自身と同じ色のコマを見つけた場合
                        if data_map[y + cursor_point_y][x + cursor_point_x] == myNumber:
                            # 何もしない。
                            pass
                        # カーソルの周りに空のマスを見つけた場合
                        elif data_map[y + cursor_point_y][x + cursor_point_x] == 0:
                            # 何もしない。
                            pass
                        # カーソルの周りに上記以外のマスを見つけた場合(色の異なるマスの場合)
                        else:                    
                            # 対象のマスからチェック方向に向かって同じ色が続くか確認する
                            # 盤面の最後まで到達するか空のマスが出てきたら終了
                            # 自身のコマと同じ色のコマが出てきたら間のコマは自身のコマの色に変更
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
                                if my_util.check_map_point(x + check_x, y + check_y) == -1:
		                        	break
                                # 終端のマスが空の場合、対象なしで終了
                                if data_map[y + check_y][x + check_x] == 0:
                                    break
                                # 自身と同じ色のコマが存在する場合
                                if data_map[y + check_y][x + check_x] == myNumber:
                                    # 対象有りのフラグを立てて終了
                                    color_change_flag = 1
                                    break
                                # 上記以外の場合(自身と異なる色のコマが存在する場合)
                                # 更に次のコマを確認するため、ループ続行する
    
                                # チェックカウントを更新
                                data_check_count = data_check_count + 1
                            
                            # コマ入れ替えフラグが有効の場合
                            if color_change_flag == 1:
                                # コマ設置有無フラグを有効に変更
                                data_set_flag = 1

                                # 色変えをリアルタイムで実施する
                                if myNumber == 1:
                                    set_anime_colorR = myCursorColorR_1
                                    set_anime_colorG = myCursorColorG_1
                                    set_anime_colorB = myCursorColorB_1
                                if myNumber == 2:
                                    set_anime_colorR = myCursorColorR_2
                                    set_anime_colorG = myCursorColorG_2
                                    set_anime_colorB = myCursorColorB_2
                                # 設置箇所のコマの色を設定
                                unicorn.set_pixel(x, y, set_anime_colorR,set_anime_colorG,set_anime_colorB)
                                # はさんだ対象コマの色も変更する
                                # unicorn.set_pixel(x + cursor_point_x * data_check_count, y + cursor_point_y * data_check_count, set_anime_colorR,set_anime_colorG,set_anime_colorB)
                                unicorn.show()
                                
                                # チェックカウント数分入れ替えを行う
                                for i in range(data_check_count+1):
                                	#for i in range(data_check_count):
                                    # 0回目は不要
                                    if i == 0:
                                        continue
                                    print("data_check_count=" + str(i))
                                    check_x = cursor_point_x * i
                                    check_y = cursor_point_y * i
                                    data_map[y + check_y][x + check_x] = myNumber
                                    
                                    # 色変えをリアルタイムで実施する
                                    unicorn.set_pixel(x + check_x,y + check_y, set_anime_colorR,set_anime_colorG,set_anime_colorB)
                                    unicorn.show()
                                    time.sleep(0.1)
                                time.sleep(0.2)
                            
    
                            # 設定値を置き換える
                            #data_map[y + cursor_point_y][x + cursor_point_x] = myNumber
                            sys.stdout.write("*")

                # コマ設置有無フラグを判定
                if data_set_flag == 1:
                    # コマを置けると判定されたため配置する
                    data_map[y][x] = myNumber

                    # コマの色を変更
                    if myNumber == 1:
                        myNumber = 2
                    else:
                        myNumber = 1

                    if my_util.check_map_data(data_map, myNumber, x, y) == 0:
	                    # passする
	                    unicorn.set_pixel(0, 0, 90,150,80)
	                    unicorn.set_pixel(0, 1, 90,150,80)
	                    unicorn.set_pixel(0, 2, 90,150,80)
	                    unicorn.set_pixel(0, 3, 90,150,80)
	                    unicorn.set_pixel(1, 0, 90,150,80)
	                    unicorn.set_pixel(1, 2, 90,150,80)
	                    unicorn.set_pixel(2, 0, 90,150,80)
	                    unicorn.set_pixel(2, 1, 90,150,80)
	                    unicorn.set_pixel(2, 2, 90,150,80)
	                    unicorn.show()
	                    time.sleep(0.5)
	                    unicorn.set_pixel(4, 0, 90,150,80)
	                    unicorn.set_pixel(4, 1, 90,150,80)
	                    unicorn.set_pixel(4, 2, 90,150,80)
	                    unicorn.set_pixel(4, 3, 90,150,80)
	                    unicorn.set_pixel(5, 0, 90,150,80)
	                    unicorn.set_pixel(5, 2, 90,150,80)
	                    unicorn.set_pixel(6, 0, 90,150,80)
	                    unicorn.set_pixel(6, 1, 90,150,80)
	                    unicorn.set_pixel(6, 2, 90,150,80)
	                    unicorn.set_pixel(6, 3, 90,150,80)
	                    unicorn.show()
	                    time.sleep(0.5)
	                    unicorn.set_pixel(1, 4, 90,150,80)
	                    unicorn.set_pixel(1, 5, 90,150,80)
	                    unicorn.set_pixel(1, 7, 90,150,80)
	                    unicorn.set_pixel(2, 4, 90,150,80)
	                    unicorn.set_pixel(2, 5, 90,150,80)
	                    unicorn.set_pixel(2, 7, 90,150,80)
	                    unicorn.set_pixel(3, 4, 90,150,80)
	                    unicorn.set_pixel(3, 6, 90,150,80)
	                    unicorn.set_pixel(3, 7, 90,150,80)
	                    unicorn.show()
	                    time.sleep(0.5)
	                    unicorn.set_pixel(5, 4, 90,150,80)
	                    unicorn.set_pixel(5, 5, 90,150,80)
	                    unicorn.set_pixel(5, 7, 90,150,80)
	                    unicorn.set_pixel(6, 4, 90,150,80)
	                    unicorn.set_pixel(6, 5, 90,150,80)
	                    unicorn.set_pixel(6, 7, 90,150,80)
	                    unicorn.set_pixel(7, 4, 90,150,80)
	                    unicorn.set_pixel(7, 6, 90,150,80)
	                    unicorn.set_pixel(7, 7, 90,150,80)
	                    print("pass")
	                    unicorn.show()
	                    time.sleep(0.5)

	                    # コマの色を変更
	                    if myNumber == 1:
	                        myNumber = 2
	                    else:
	                        myNumber = 1

	                    #if my_util.check_map_data(data_map, myNumber) == 0:
	                    	# 両方とも置けなくなったので終了する。（処理を作成する）
	                    #	print("end")

                    time.sleep(0.2)


        # 強制終了キー押下時の処理
        if ch =='0':
            print('?')
            break

        # 最大値超え→最小値　最小値未満→最大値変換
        x = my_util.check_map_minmax( x, 0, width )
        y = my_util.check_map_minmax( y, 0, height )

        # 配列設定値に応じてLEDの表示変更
        for y_count in range(height):
            for x_count in range(width):
                if data_map[y_count][x_count] == 0:
                    unicorn.set_pixel(x_count, y_count, 0, 0, 0)
                if data_map[y_count][x_count] == 1:
                    unicorn.set_pixel(x_count, y_count, int(colorR_1*0.4), int(colorG_1*0.4), int(colorB_1*0.4))
                if data_map[y_count][x_count] == 2:
                    unicorn.set_pixel(x_count, y_count, int(colorR_2*0.4), int(colorG_2*0.4), int(colorB_2*0.4))
        unicorn.show()


finally:
    # fdの属性を元に戻す
    # 具体的にはICANONとECHOが元に戻る
    termios.tcsetattr(fd, termios.TCSANOW, old)

print(ch)
