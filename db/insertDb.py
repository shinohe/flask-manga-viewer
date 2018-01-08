# -*- coding: utf-8 -*-

import psycopg2
from datetime import datetime


def insertBooks(bookName, bookNameKana, thumbnailPath, path, category):
	conn = psycopg2.connect("host=ec2-54-83-46-116.compute-1.amazonaws.com port=5432 dbname=dbfppmk6l1t0tt user=xnsrwjdwqjosvp password=128e66d4fa11ab6667cb7fbc456f16f95b34ccda2cc1431e945d12baeed76bf9")
	c = conn.cursor()

	insId = 0
	select_sql = 'select count(id) from books'
	c.execute(select_sql)
	for row in c:
		print(row[0])
		insId = int(row[0]) + 1

	# 本のデータの挿入増えたら足してく
	insert_sql = 'insert into books(id, bookName, kana, thumbnailPath, path, category, updateDate) values (%s,%s,%s,%s,%s,%s,%s)'
	books = [
	    (insId, bookName, bookNameKana,thumbnailPath, path, category, datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
	]
	c.executemany(insert_sql, books)
	conn.commit()

