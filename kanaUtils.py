#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
import random

hiragana = "ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろゎわゐゑをん"
katakana = "ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロヮワヰヱヲンヴ"
suuji = "0123456789０１２３４５６７８９"

# ひらがなだけの文字列ならTrue
def ishira(strj):
	return all([ch in hiragana for ch in strj])

# カタカナだけの文字列ならTrue
def iskata(strj):
	return all([ch in katakana for ch in strj])

# カタカナ・ひらがなだけの文字列ならTrue
def iskatahira(strj):
	return all([ch in katakana or ch in hiragana for ch in strj])

# ひらがなをカタカナに直す
def kata_to_hira(strj):
	return "".join([chr(ord(ch) - 96) if ("ァ" <= ch <= "ン") else ch for ch in strj])

# ひらがなをカタカナに直す        
def hira_to_kata(strj):
	return "".join([chr(ord(ch) + 96) if ("ぁ" <= ch <= "ん") else ch for ch in strj])

# 全角数字を半角数字に直す
def hankaku_suuji(strj):
	dic2 = str.maketrans("０１２３４５６７８９", "0123456789")
	return strj.translate(dic2)

def randamAlphaStr(n):
	return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(n)])
