#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Flask などの必要なライブラリをインポートする
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
import numpy as np
from flask_httpauth import HTTPDigestAuth
import os
import json
import PIL.Image
import sqlite3
import math
import logs
import kanaUtils
import re
import zipfile
import shutil
from db import insertDb
from dist import dist
from datetime import datetime

import sys  
sys.path.append('SOME_PATH\python\Lib\encodings');  

import codecs  
import encodings.utf_8

codecs.register(lambda encoding: utf_8.getregentry()) 

currentDir = os.path.dirname(os.path.abspath(__file__))
dbpath = currentDir + os.sep + 'db' + os.sep
dbname = 'database.db'
tablename = 'books'

# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)
app.register_blueprint(dist.app)
app.config['SECRET_KEY'] = 'secret key here'
auth = HTTPDigestAuth()

users = {
	"jdragon1": "jdragon1"
}

class InvalidUsage(Exception):
	status_code = 400

	def __init__(self, message, status_code=None, payload=None):
		Exception.__init__(self)
		self.message = message
		if status_code is not None:
			self.status_code = status_code
		self.payload = payload
		
	def to_dict(self):
		rv = dict(self.payload or ())
		rv['message'] = self.message
		return rv

class PageList:
	list = []
	pageSize = 8
	page = 1
	maxSize = 0
	def __init__(self,list, pageSize, maxSize, page):
		self.list = list
		self.pageSize = pageSize
		self.maxSize = maxSize
		self.page = page
	def serialize(self):
		return {
		'list':ViewerImageJSONEncoder().encode(self.list),
		'pageSize':self.pageSize,
		'maxSize':self.maxSize,
		'page':self.page
		}

class Thumbnail:
	id = ''
	name = ''
	folderName = ''
	thumbnailPath = ''
	category = ''
	description = ''
	updateDate = ''
	createDate = ''
	width = 0
	height = 0
	def __init__( self, id, name, folderName, thumbnailPath, width=None, height=None,description=None, category=None, updateDate=None, createDate=None):
		self.id = id
		self.name = name
		self.folderName = folderName
		self.thumbnailPath = thumbnailPath
		self.width = width
		self.height = height
		self.description = description
		self.category = category
		self.updateDate = updateDate
		self.createDate = createDate
	def serialize(self):
		return {
		'id': self.id,
		'name': self.name, 
		'folderName': self.folderName, 
		'thumbnailPath': self.thumbnailPath, 
		'description': self.description, 
		'category': self.category, 
		'updateDate': self.updateDate, 
		'createDate': self.createDate, 
		'width': self.width,
		'height': self.height		 
		}

class ViewerImage:
	fileName = ''
	width = 0
	height = 0
	def __init__(self, fileName, width=None, height=None):
		self.fileName = fileName
		self.width = width
		self.height = height
	
	def serialize(self):
		return {
		'fileName': self.fileName, 
		'width': self.width,
		'height': self.height		 
		}

class ViewerImageJSONEncoder(json.JSONEncoder):
	def default(self, o):
		if isinstance(o, PageList):
			return o.serialize()
		if isinstance(o, ViewerImage):
			return o.serialize()
		if isinstance(o, Thumbnail):
			return o.serialize()
		return super(ViewerImageJSONEncoder, self).default(o)
		
app.json_encoder = ViewerImageJSONEncoder

# メソッド
def thumbnnailListNoKana(page, pageSize):
	return thumbnnailList(page, pageSize, None)

def thumbnnailList(page, pageSize, searchText):
	imageList = []
	params =(pageSize, page*pageSize)
	
	# FIXME LIMIT OFFSETでページネーションしてるのでチューニングは必要	
	conn = sqlite3.connect(dbpath+dbname)
	c = conn.cursor()

	count_sql = 'select count(*) from books'
	select_sql = 'select * from books order by createDate desc limit ? offset ?'
	if searchText:
		if (kanaUtils.ishira(searchText)):
			searchText = kanaUtils.hira_to_kata(searchText)
		count_sql = 'select count(*) from books where bookName like ? or kana like ? or category like ?'
		select_sql = 'select * from books where bookName like ? or kana like ? or category like ? order by createDate desc limit ? offset ?'
		kana = u"%{}%".format(searchText)
		params =(kana, kana, kana, pageSize, page*pageSize)
		count_params = (kana, kana, kana)
		c.execute(count_sql, count_params)
	else:
		c.execute(count_sql)
	maxSize = c.fetchone()
	
	for row in c.execute(select_sql, params):
		id = row[0]
		name = row[1]
		path = row[3]
		folderName = row[4]
		category = row[5]
		updateDate = row[6]
		createDate = row[7]
		try:
			fileImage = PIL.Image.open(path)
		except:
			# エラーの場合は飛ばす
			path = 'static' + os.sep + 'images' + os.sep + '404' + os.sep + '404error.png'
			fileImage = PIL.Image.open(path)
		viewer = Thumbnail(id, name, folderName, path, width=fileImage.size[0], height=fileImage.size[1], category=category, updateDate=updateDate, createDate=createDate)
		imageList.append(viewer)
	conn.close
	
	pageList = PageList(imageList, pageSize, math.ceil(maxSize[0]/pageSize), page)
	return jsonify(pageList)


# Digest認証
@auth.get_password
def get_pw(username):
	if username in users:
		return users.get(username)
	return None


# ここからウェブアプリケーション用のルーティングを記述
# index にアクセスしたときの処理
@app.route('/')
def index():
	title = "flaskMangaViewer"
	page = 1
	# index.html をレンダリングする
	return render_template('index.html', title=title, page=page)

@app.route('/Search/list', methods=['POST'])
def searchList():
	page = 0
	pageSize = 8
	searchText = ''
	if request.data:
		content_body_dict = json.loads(request.data)
	
		if 'page' in content_body_dict:
			page = request.json.get('page')
			page = int(page) - 1
			if page < 0:
				page = 0

		if 'pageSize' in content_body_dict:
			pageSize = request.json.get('pageSize')
			
		if 'searchText' in content_body_dict:
			searchText = request.json.get('searchText')
	return thumbnnailList(page, pageSize, searchText)

@app.route('/Latest/list', methods=['POST'])
def latestList():
	
	page = 0
	pageSize = 8
	if request.data:
		content_body_dict = json.loads(request.data)
	
		if 'page' in content_body_dict:
			page = request.json.get('page')
			page = int(page) - 1
			if page < 0:
				page = 0

		if 'pageSize' in content_body_dict:
			pageSize = request.json.get('pageSize')
		
	return thumbnnailListNoKana(page, pageSize)

@app.route('/Viewer')
def viewer():
	title = "flask-manga-viewer"
	# viewer.html をレンダリングする
	page = request.args.get('page')
	return render_template('viewer.html', title=title, page=page)
	
@app.route('/Viewer/list', methods=['POST'])
def viewList():
	content_body_dict = json.loads(request.data)
	if request.headers['Content-Type'] != 'application/json':
		return jsonify(res='error'), 400
	page = request.json.get('page')
	try:
		fileList = os.listdir(currentDir + os.sep + 'static' + os.sep + 'images' + os.sep + page)
	except FileNotFoundError:
		PIL.Image
		raise InvalidUsage('ファイル、またはフォルダがありません path=static/images/'+page, status_code=404)
		
	# 画像ファイルを基に
	imageList = []
	for file in fileList:
		path = currentDir + os.sep + 'static' + os.sep + 'images' + os.sep + page + os.sep + file
		fileImage = PIL.Image.open(path)
		viewer = ViewerImage(file, width=fileImage.size[0], height=fileImage.size[1])
		imageList.append(viewer)
		
	return jsonify(imageList)


# 管理画面
@app.route('/menu', methods=['GET', 'POST'])
@auth.login_required
def menu():
	title = u"flask-manga-viewer"
	if request.method == 'GET':
		return render_template('menu.html', title=title)
	else:
		return redirect(url_for('/menu'))


# ファイル追加
@app.route('/inputFile', methods=['GET', 'POST'])
@auth.login_required
def inputFile():
	title = u"flask-manga-viewer"
	if request.method == 'GET':
		return render_template('input.html', title=title)
	else:
		return redirect(url_for('inputFile'))

# 裏画面リスト表示
@app.route('/manageList', methods=['GET', 'POST'])
@auth.login_required
def manageList():
	title = u"flask-manga-viewer"
	if request.method == 'GET':
		return render_template('manageList.html', title=title)
	else:
		return redirect(url_for('/manageList'))

@app.route('/upload', methods=['POST'])
def upload():
	pattern = re.compile(u'.*\.zip')
	inputFile = request.files['inputFile']
	title =  request.form['title']
	titleKana =  request.form['titleKana']
	category =  request.form['category']

	# zipファイルのみ受け付ける
	m = pattern.match(inputFile.filename)
	if m is None:
		error_message = inputFile.filename + u" はzipファイルではありません"
		title = u"ファイルアップロードエラー"
		return render_template('input.html', error_message=error_message, title=title)
	if not os.path.exists('crawler'+os.sep+'download'+os.sep):
		os.makedirs('crawler'+os.sep+'download'+os.sep)
	
	directorypath = '.'+os.sep+'crawler'+os.sep+'download'+os.sep+inputFile.filename
#	if os.path.exists(directorypath):
#		error_message = inputFile.filename + u"存在しています."
#		title = u"ファイルアップロードエラー"
#		return render_template('input.html', error_message=error_message, title=title)
	
	inputFile.save(directorypath)
	print('saved file path: '+directorypath)
	while True:
		# 新しいディレクトリを作成
		randamAlphaDir = kanaUtils.randamAlphaStr(10)
		openPath = 'static' + os.sep + 'images' + os.sep + randamAlphaDir
		if not os.path.exists(openPath):
			os.makedirs(openPath)
			break

	fileNameList = []
	with zipfile.ZipFile(directorypath, 'r') as zf:
		pattern = re.compile(u'.*\.jpg')
		print(zf.namelist())
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
		
		

	# def insertBooks(bookName, bookNameKana, thumbnailPath, path, category):
	insertDb.insertBooks(title, titleKana, firstFilePath, randamAlphaDir, category)
	print("OK")

	return render_template('input.html', message=u'アップロードが正常に完了しました。')

@app.route('/delete', methods=['POST'])
def delete():
	if request.data:
		content_body_dict = json.loads(request.data)
	
		if 'id' in content_body_dict:
			id = request.json.get('id')
	
	row = insertDb.findBooks(id)
	name = row[1]
	folderName = row[4]

	insertDb.deleteBook(id)
	
	path = 'static' + os.sep + 'images' + os.sep + folderName
#	ファイルの物理削除は要検討
#	if os.path.exists(path):
#		shutil.rmtree(path)
	
	return jsonify(name + "の削除は成功しました。")


@app.route('/editView', methods=['POST','GET'])
def editView():
	if request.method == 'GET':
		# リクエストフォームから「id」を取得して
		id = request.args.get('id', '')
		if id == '':
			return redirect(url_for('manageList'))

		row = insertDb.findBooks(id)
		id = row[0]
		name = row[1]
		nameKana = row[2]
		path = row[3]
		folderName = row[4]
		category = row[5]
		updateDate = row[6]
		createDate = row[7]
		
		# editView.html をレンダリングする
		return render_template('editView.html', id=id, name=name, nameKana=nameKana, thumnailPath=path, folderName=folderName, category=category, updateDate=updateDate, createDate=createDate, title=u'編集' )
	else:
		id = request.form['id']
		return redirect(url_for('editView?id='+id))

@app.route('/update', methods=['POST'])
def update():
	print("update")
	id = request.form['id']
	title = request.form['title']
	titleKana =  request.form['titleKana']
	folderName =  request.form['folderName']
	category =  request.form['category']

	insertDb.updateBook(id, title, titleKana, path=folderName, category=category)
	
	return render_template('manageList.html', title=u'flask-manga-viewer 管理画面', message=u'更新は完了しました。')


@app.errorhandler(InvalidUsage)
def error_handler(error):
	response = jsonify({ 'message': error.message, 'result': error.status_code })
	return response, error.status_code

if __name__ == '__main__':
	logs.init_app(app)
	app.debug = True  #デバッグモード有効化
	app.run(host='0.0.0.0', threaded=True) # どこからでもアクセス可能に

