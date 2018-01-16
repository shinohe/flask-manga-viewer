# -*- coding: utf-8 -*-

import sqlite3
from datetime import datetime
dbname = 'db/database.db'

def findBooks(id):
	conn = sqlite3.connect(dbname, timeout=10)
	c = conn.cursor()

	select_sql = 'select * from books where id = ?'
	bookParam = (int(id),)
	c.execute(select_sql, bookParam)
	for row in c:
		book = row
	
	conn.close()
	return book

def insertBooks(bookName, bookNameKana, thumbnailPath, path, category):
	conn = sqlite3.connect(dbname, timeout=10)
	c = conn.cursor()

	insId = 0
	select_sql = 'select count(id) from books'
	c.execute(select_sql)
	for row in c:
		print(row[0])
		insId = int(row[0]) + 1

	# 本のデータの挿入増えたら足してく
	insert_sql = 'insert into books(id, bookName, kana, thumbnailPath, path, category, updateDate, createDate) values (?,?,?,?,?,?,?,?)'
	books = [
	    (insId, bookName, bookNameKana,thumbnailPath, path, category, datetime.now().strftime("%Y/%m/%d %H:%M:%S"), datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
	]
	c.executemany(insert_sql, books)
	conn.commit()
	conn.close()

def updateBook(id, bookName=None, bookNameKana=None, thumbnailPath=None, path=None, category=None):
	conn = sqlite3.connect(dbname, timeout=10)
	c = conn.cursor()
	updateDate = datetime.now().strftime("%Y/%m/%d %H:%M:%S");

	# idなかったらそもそも問題
	if not id:
		conn.close()
		raise Exception("id is not found")

	# 本のデータの挿入増えたら足してく
	# 空たぷる生成
	param = ()
	update_sql = 'update books set '
	param = param + (updateDate,)
	update_sql = update_sql + ' updateDate=?'
	
	if bookName:
		param = param + (bookName,)
		update_sql = update_sql + ', bookName=?'
	if bookNameKana:
		param = param + (bookNameKana,)
		update_sql = update_sql + ', kana=?'
	if thumbnailPath:
		param = param + (thumbnailPath,)
		update_sql = update_sql + ', thumbnailPath=?'
	if path:
		param = param + (path,)
		update_sql = update_sql + ', path=?'
	if category:
		param = param + (category,)
		update_sql = update_sql + ', category=?'
		
	param = param + (id,)
	update_sql = update_sql + ' where id=?'
	print(update_sql)
	print(param)
	
	c.execute(update_sql, param)
	conn.commit()
	conn.close()

def deleteBook(id):
	conn = sqlite3.connect(dbname, timeout=10)
	c = conn.cursor()

	# 削除
	delete_sql = 'delete from books where id = ?'
	bookParam = (id,)
	c.execute(delete_sql, bookParam)
	conn.commit()
	conn.close()
