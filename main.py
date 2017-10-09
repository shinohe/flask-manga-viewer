# Flask などの必要なライブラリをインポートする
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
import numpy as np
from flask_httpauth import HTTPDigestAuth
import os
import json
import PIL.Image

# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key here'
auth = HTTPDigestAuth()

users = {
	"y-shinohe1": "y-shinohe1"
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
		if isinstance(o, ViewerImage):
			return o.serialize()
		return super(ViewerImageJSONEncoder, self).default(o)
		
app.json_encoder = ViewerImageJSONEncoder

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
	# index.html をレンダリングする
	return render_template('index.html', title=title)

@app.route('/Viewer')
def viewer():
	title = "ようこそ"
	page = request.args.get("page", default="sam")
	# viewer.html をレンダリングする
	# pageにページ番号を記載 jsonで
	return render_template('viewer.html', page=page, title=title)
	
@app.route('/Viewer/list', methods=['POST'])
def viewList():
	print("ビューリスト取得")
	print(request.data)
	content_body_dict = json.loads(request.data)
	print(content_body_dict.get('page'))
	if request.headers['Content-Type'] != 'application/json':
		print('jsonではない')
		print(request.headers['Content-Type'])
		return jsonify(res='error'), 400
	page = request.json.get('page')
	print('ページ='+page)
	try:
		fileList = os.listdir('static/images/'+page)
	except FileNotFoundError:
		print('ファイル、またはフォルダがありません path=static/images/'+page)
		PIL.Image
		raise InvalidUsage('ファイル、またはフォルダがありません path=static/images/'+page, status_code=404)
		
	# 画像ファイルを基に
	imageList = []
	for file in fileList:
		path = 'static/images/' + page + '/' + file
		fileImage = PIL.Image.open(path)
		viewer = ViewerImage(file, width=fileImage.size[0], height=fileImage.size[1])
		imageList.append(viewer)
		
	return jsonify(imageList)


# /post にアクセスしたときの処理
@app.route('/post', methods=['GET', 'POST'])
def post():
	title = "こんにちは"
	if request.method == 'POST':
		# リクエストフォームから「名前」を取得して
		name = request.form['name']
		# index.html をレンダリングする
		return render_template('index.html',
							   name=name, title=title)
	else:
		return redirect(url_for('index'))

# TODO ファイル追加画面
@app.route('/inputFile', methods=['GET', 'POST'])
@auth.login_required
def inputFile():
	title = u"flask-manga-viewer"
	if request.method == 'GET':
		return render_template('input.html', title=title)
	else:
		return redirect(url_for('input.html'))

@app.route('/upload', methods=['POST'])
def upload():
	the_file = request.files['the_file']
	if os.path.exists('/crawler/download/'+the_file.filename):
		error_message = the_file.filename + u"存在しています."
		title = u"ファイルアップロードエラー"
		return render_template('input.html', error_message=error_message, title=title)
	else:
		the_file.save("./" + the_file.filename)
	return ""
	
	
@app.errorhandler(InvalidUsage)
def error_handler(error):
	response = jsonify({ 'message': error.message, 'result': error.status_code })
	return response, error.status_code

if __name__ == '__main__':
	app.debug = True # デバッグモード有効化
	app.run(host='0.0.0.0') # どこからでもアクセス可能に