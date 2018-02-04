// クッキー関係の初期化処理
function initializeCookie(){
	
}

// お気に入り取得
function getFavoritCookie(){
	if ($.cookie("favoritBooks")) {
		return JSON.parse($.cookie("favoritBooks"));
	} else {
		return [];
	}
}

// お気に入りに追加
function saveFavoritCookie(id){
	books = getFavoritCookie();
	if (books.indexOf(id) < 0) {
		books.push(id);
	} else {
		books.splice(books.indexOf(id),1);
		books.push(id);
	}
	$.cookie("favoritBooks",JSON.stringify(books) ,{ expires: 3650 });
}

// お気に入りから削除
function delFavoritCookie(id){
	books = getFavoritCookie();
	if (books.indexOf(id) >= 0) {
		books.splice(books.indexOf(id),1);
	}
	$.cookie("favoritBooks",JSON.stringify(books),{ expires: 3650 });
}

