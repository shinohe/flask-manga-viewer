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

def updateBook(id, bookName, bookNameKana, thumbnailPath, path, category):
	conn = sqlite3.connect(dbname, timeout=10)
	c = conn.cursor()

	# idなかったらそもそも問題
	if id == ''
		raise Exception("id is not found")

	# 本のデータの挿入増えたら足してく
	update_sql = 'update set books(id, bookName, kana, thumbnailPath, path, category, updateDate, createDate) values (?,?,?,?,?,?,?,?)'
	books = [
	    (insId, bookName, bookNameKana,thumbnailPath, path, category, datetime.now().strftime("%Y/%m/%d %H:%M:%S"), datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
	]
	c.executemany(insert_sql, books)
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
