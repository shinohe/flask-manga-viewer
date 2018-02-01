#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import zipfile
import os
import kanaUtils
import shutil
from db import insertDb



directorypath = '.'+os.sep+'crawler'+os.sep+'download'+os.sep
displayFlag = 0

zipFileNameListBk = os.listdir(directorypath+'bk')
zipFileNameList = os.listdir(directorypath)

for bkFile in zipFileNameListBk:
	i = 0
	for zipFileName in zipFileNameList:
		if bkFile == zipFileName:
			print(zipFileNameList.pop(i))
			print('duplicate filename :'+bkFile)
			shutil.move(directorypath+zipFileName, directorypath + 'bk' + os.sep + zipFileName)
			break
		i = i + 1
			

for zipFileName in zipFileNameList:
	pattern = re.compile(u'.*\.zip', re.IGNORECASE)
	m = pattern.match(zipFileName)
	if m is None:
		if zipFileName == 'error':
			continue
		if zipFileName == 'bk':
			continue
		print(directorypath+zipFileName)
		print(directorypath + 'error' + os.sep + zipFileName)
		shutil.move(directorypath+zipFileName, directorypath + 'error' + os.sep + zipFileName)
		continue
	if not os.path.exists('crawler'+os.sep+'download'+os.sep):
		os.makedirs('crawler'+os.sep+'download'+os.sep)
	
	
	while True:
		# 新しいディレクトリを作成
		randamAlphaDir = kanaUtils.randamAlphaStr(10)
		openPath = 'static' + os.sep + 'images' + os.sep + randamAlphaDir
		if not os.path.exists(openPath):
			os.makedirs(openPath)
			break
	
	fileNameList = []
	with zipfile.ZipFile(directorypath+zipFileName, 'r') as zf:
		pattern = re.compile(u'.*\.jpg')
		for f in zf.namelist():
			fileMuch = pattern.match(f)
			if fileMuch is None:
				print('foldername :'+f)
			else:
				d = openPath+os.sep+os.path.basename(f)
				fileNameList.append(d)
				print('filename :'+d)
				with open(d, 'wb') as uzf:
					uzf.write(zf.read(f))
					uzf.close()
	fileNameList.sort()
	firstFilePath = fileNameList[0]
	
	insertDb.insertBooks('', '', firstFilePath, randamAlphaDir, '', displayFlag)
	shutil.move(directorypath+zipFileName, directorypath + 'bk' + os.sep + zipFileName)
	print("directorypath: " + directorypath)
	print("file backup: " + directorypath + 'bk' + os.sep + zipFileName)
