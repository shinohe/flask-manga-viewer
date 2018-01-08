# -*- coding: utf-8 -*-

import sqlite3
from datetime import datetime
dbname = 'db/database.db'


def insertBooks(bookName, bookNameKana, thumbnailPath, path, category):
	conn = sqlite3.connect(dbname)
	c = conn.cursor()

	insId = 0
	select_sql = 'select count(id) from books'
	c.execute(select_sql)
	for row in c:
		print(row[0])
		insId = int(row[0]) + 1

	# 本のデータの挿入増えたら足してく
	insert_sql = 'insert into books(id, bookName, kana, thumbnailPath, path, category, updateDate) values (?,?,?,?,?,?,?)'
	books = [
	    (insId, bookName, bookNameKana,thumbnailPath, path, category, datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
	]
	c.executemany(insert_sql, books)
	conn.commit()

