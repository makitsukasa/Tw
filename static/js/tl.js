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
	// https://qiita.com/ka-ko/items/feacb4d3ff22666d51b1
	const q = `#\\3${id.slice(0, 1)} ${id.slice(1)} > .buttons`;
	const favButton = document.querySelector(`${q} > .fav_button`);
	const unfavButton = document.querySelector(`${q} > .unfav_button`);
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
