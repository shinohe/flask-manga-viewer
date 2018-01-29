# -*- coding: utf-8 -*-

import sqlite3
from datetime import datetime

dbname = 'database.db'
tablename = 'books'

conn = sqlite3.connect(dbname)
c = conn.cursor()

# 削除するなら
c.execute("SELECT * FROM sqlite_master WHERE type='table' and name='%s'" % tablename)
if c.fetchone() != None: #存在してたら初期化
	c.execute('DROP TABLE books')

if c.fetchone() == None: #存在してないので作る
	# executeメソッドでSQL文を実行する
	create_table = '''create table books (id int, bookName varchar(256), kana varchar(256), thumbnailPath varchar(256), path varchar(256), category varchar(256), updateDate datetime, createDate datetime, displayFlag int)'''
	c.execute(create_table)

#データの削除
delete_sql = 'delete from books'
c.execute(delete_sql)
conn.commit()


# 本のデータの挿入増えたら足してく
insert_sql = 'insert into books(id, bookName, kana, thumbnailPath, path, category, updateDate, createDate, displayFlag) values (?,?,?,?,?,?,?,?,?)'
books = [
    (1, 'ブラックジャックによろしく１', 'ﾌﾞﾗｯｸｼﾞｬｯｸﾆﾖﾛｼｸｲﾁ','static/images/bj01/bj01_000002.jpg', 'bj01', '医療', datetime.now().strftime("%Y/%m/%d %H:%M:%S"), datetime.now().strftime("%Y/%m/%d %H:%M:%S"),1),
    (2, 'ブラックジャックによろしく2', 'ﾌﾞﾗｯｸｼﾞｬｯｸﾆﾖﾛｼｸｲﾁ','static/images/bj02/bj01_000061.jpg', 'bj02', '医療', '2017/10/13 11:54:22', datetime.now().strftime("%Y/%m/%d %H:%M:%S"),1),
    (3, 'ブラックジャックによろしく3', 'ﾌﾞﾗｯｸｼﾞｬｯｸﾆﾖﾛｼｸｲﾁ','static/images/bj03/bj01_000087.jpg', 'bj03', '医療', datetime.now().strftime("%Y/%m/%d %H:%M:%S"), datetime.now().strftime("%Y/%m/%d %H:%M:%S"),1)
]
c.executemany(insert_sql, books)
conn.commit()

#select_sql = 'select * from books limit ? offset ?'
select_sql = 'select * from books'
params = (2,1)
for row in c.execute(select_sql):
	print(row)

conn.close()
