function createFavorite(e) {
	e.preventDefault();
	const id = e.target.parentElement.parentElement.id;
	const request = new XMLHttpRequest();
	request.onload = () => {};
	request.open('get', '/create_favorite/' + id, true);
	request.send();
	return false;
}

window.addEventListener('load', function(){
	const buttons = document.getElementsByClassName('fav_button');
	for(let i = 0; i < buttons.length; i++) {
		buttons[i].addEventListener('click', createFavorite, false);
	}
}, false);
