#!/usr/bin/python
# -*- coding:utf-8 -*-


import PLI
import os, sys

#pragma mark -
# 画像を指定した場所から、指定したサイズに切り出して、PIL.imageオブジェクトにして返す
#
def pointSplitImage (image, point=(0,0), size=(300,300)):
	newimg = Image.new('RGB', size)
	
	imageFormat = image.format
	for x in range(0, size[0]):
		for y in range(0, size(1):
			px = point[0] + x
			py = point[1] + y
			
			newimg.putpixel((px,py), image.getpixel((px,py)))
	return newimg


# 指定した画像を、指定した個数に分割して、連番で保存する。
# 個数は、4,9,16,25,36... の数にする
# いずれの数でも無い場合、例外を出す
SPLITIMAGENUMBERERROR = 'SplitImageNumberError'
def splitImage (image, fname='fname', num=4):
	# 引数チェック
	bnum = 1
	kinnum = 1
	while (1):
		if kinnum*kinnum == num:
			break
		elif bnum*bnum < num < kinnum*kinnum:
			raise SPLITIMAGENUMBERERROR, {'msg':'SplitImageNumberError'}
		bnum = kinnum
		kinnum += 1
	
	(x,y) = image.size
	(spx, spy) = (x/num, y/num)
	spy
	

if __name__ == '__main__':
	
