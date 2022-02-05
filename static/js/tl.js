// https://stackoverflow.com/questions/28879696/equivalent-of-getjson-function-without-jquery
function createFavorite(e) {
	e.preventDefault();
	const id = e.target.parentElement.parentElement.id;
	const request = new XMLHttpRequest();
	request.onload = () => {reactFavSucceed(id)};
	request.onerror = () => {reactFavFailed(id)};
	request.open('post', '/create_favorite', true);
	request.setRequestHeader("Content-Type", "application/json");
	request.send(JSON.stringify({'id': id}));
	return false;
}

function destroyFavorite(e) {
	e.preventDefault();
	const id = e.target.parentElement.parentElement.id;
	const request = new XMLHttpRequest();
	request.onload = () => {reactUnfavSucceed(id)};
	request.onerror = () => {reactUnfavFailed(id)};
	request.open('post', '/destroy_favorite', true);
	request.setRequestHeader("Content-Type", "application/json");
	request.send(JSON.stringify({'id': id}));
	return false;
}

function retweet(e) {
	e.preventDefault();
	const id = e.target.parentElement.parentElement.id;
	const request = new XMLHttpRequest();
	request.onload = () => {reactRtSucceed(id)};
	request.onerror = () => {reactRtFailed(id)};
	request.open('post', '/retweet', true);
	request.setRequestHeader("Content-Type", "application/json");
	request.send(JSON.stringify({'id': id}));
	return false;
}

function reactFavSucceed(id) {
	// https://qiita.com/ka-ko/items/feacb4d3ff22666d51b1
	const q = `#\\3${id.slice(0, 1)} ${id.slice(1)} > .buttons`;
	const favButton = document.querySelector(`${q} > .fav_button`);
	const unfavButton = document.querySelector(`${q} > .unfav_button`);
	favButton.disabled = true;
	unfavButton.disabled = false;
}

function reactFavFailed(id) {
	const q = `#\\3${id.slice(0, 1)} ${id.slice(1)} > .buttons`;
	const favButton = document.querySelector(`${q} > .fav_button`);
	favButton.innerHTML += ' ✕';
}

function reactUnfavSucceed(id) {
	const q = `#\\3${id.slice(0, 1)} ${id.slice(1)} > .buttons`;
	const favButton = document.querySelector(`${q} > .fav_button`);
	const unfavButton = document.querySelector(`${q} > .unfav_button`);
	favButton.disabled = false;
	unfavButton.disabled = true;
}

function reactUnfavFailed(id) {
	const q = `#\\3${id.slice(0, 1)} ${id.slice(1)} > .buttons`;
	const unfavButton = document.querySelector(`${q} > .unfav_button`);
	unfavButton.innerHTML += ' ✕';
}

function reactRtSucceed(id) {
	const q = `#\\3${id.slice(0, 1)} ${id.slice(1)} > .buttons`;
	const rtButton = document.querySelector(`${q} > .rt_button`);
	rtButton.innerHTML += ' ✓';
}

function reactRtFailed(id) {
	const q = `#\\3${id.slice(0, 1)} ${id.slice(1)} > .buttons`;
	const rtButton = document.querySelector(`${q} > .rt_button`);
	rtButton.innerHTML += ' ✕';
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
