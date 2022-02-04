// https://stackoverflow.com/questions/28879696/equivalent-of-getjson-function-without-jquery
function createFavorite(e) {
	e.preventDefault();
	const id = e.target.parentElement.parentElement.id;
	const request = new XMLHttpRequest();
	request.onload = () => {toggleFavButton(id)};
	request.open('post', '/create_favorite/' + id, true);
	request.send();
	return false;
}

function destroyFavorite(e) {
	e.preventDefault();
	const id = e.target.parentElement.parentElement.id;
	const request = new XMLHttpRequest();
	request.onload = () => {toggleFavButton(id)};
	request.open('post', '/destroy_favorite/' + id, true);
	request.send();
	return false;
}

function retweet(e) {
	e.preventDefault();
	const id = e.target.parentElement.parentElement.id;
	const request = new XMLHttpRequest();
	request.onload = () => {};
	request.open('post', '/retweet/' + id, true);
	request.send();
	return false;
}

function toggleFavButton(id) {
	const favButton = document.querySelector(`#{id} > .buttons > .fav_button`);
	const unfavButton = document.querySelector(`#{id} > .buttons > .unfav_button`);
	favButton.disabled = !favButton.disabled
	unfavButton.disabled = !unfavButton.disabled
}

window.addEventListener('load', function(){
	const favButtons = document.getElementsByClassName('fav_button');
	for(let i = 0; i < favButtons.length; i++) {
		favButtons[i].addEventListener('click', createFavorite, false);
	}

	const unfavButtons = document.getElementsByClassName('unfav_button');
	for(let i = 0; i < unfavButtons.length; i++) {
		unfavButtons[i].addEventListener('click', destroyFavorite, false);
	}

	const rtButtons = document.getElementsByClassName('rt_button');
	for(let i = 0; i < rtButtons.length; i++) {
		rtButtons[i].addEventListener('click', retweet, false);
	}
}, false);
