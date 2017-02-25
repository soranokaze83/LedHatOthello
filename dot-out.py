#!/usr/bin/env python

import time
import random

import unicornhat as unicorn


print("""test

Turns each pixel on in turn and updates the display.
If you're using a Unicorn HAT and only half the screen lights up,
edit this example and  change 'unicorn.AUTO' to 'unicorn.HAT' below.
""")

unicorn.set_layout(unicorn.AUTO)
unicorn.rotation(0)
unicorn.brightness(0.5)
width,height=unicorn.get_shape()

x= random.randint(0,7)
y= random.randint(0,7)
w=1
h=1

rangesize = 30

for j in range( rangesize ):
	colorR = random.randint(50,255)
	colorG = random.randint(50,255)
	colorB = random.randint(50,255)
#	colorR = 255/rangesize*(j+1) + 255/rangesize
#	colorG = 100
#	colorB = 80

	print("---------------")
	print("Red   : " + str(colorR))
	print("Green : " + str(colorG))
	print("Blue  : " + str(colorB))
	print("---------------")

	for i in range(10):
	 unicorn.set_pixel(x, y, colorR, colorG, colorB)
	 unicorn.show()
	 time.sleep(0.1)
	 unicorn.set_pixel(x , y, 0, 0, 0)
	 unicorn.show()

	 x= x + w
	 y= y + h

	 if x >= width:
	  print(">")
	  x = width-1
	  w = -1 * random.randint(1,2)

	 if x < 0:
	  print("<")
	  x = 0
	  w = 1  * random.randint(1,2)

	 if y >= height:
	  print("_")
	  y = height-1
	  h = -1 * random.randint(1,2)

	 if y < 0:
	  print("^")
	  y = 0
	  h = 1 * random.randint(1,2)

for j in range(height):
    unicorn.set_pixel(x,j,colorR,colorG,colorB)
    unicorn.show()

for i in range(width):
    unicorn.set_pixel(i,y,colorR,colorG,colorB)
    unicorn.show()



time.sleep(3)
