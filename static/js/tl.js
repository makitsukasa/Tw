// https://stackoverflow.com/questions/28879696/equivalent-of-getjson-function-without-jquery
function createFavorite(e) {
	e.preventDefault();
	const id = e.target.parentElement.parentElement.id;
	const request = new XMLHttpRequest();
	request.onload = () => {};
	request.open('post', '/create_favorite/' + id, true);
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

function showImage(e) {
	e.preventDefault();
	const id = e.target.parentElement.parentElement.id;
	const request = new XMLHttpRequest();
	request.onload = () => {};
	request.open('post', '/show_image/' + id, true);
	request.send();
	return false;
}

window.addEventListener('load', function(){
	const favButtons = document.getElementsByClassName('fav_button');
	for(let i = 0; i < favButtons.length; i++) {
		favButtons[i].addEventListener('click', createFavorite, false);
	}

	const rtButtons = document.getElementsByClassName('rt_button');
	for(let i = 0; i < rtButtons.length; i++) {
		rtButtons[i].addEventListener('click', retweet, false);
	}

	const imgButtons = document.getElementsByClassName('img_button');
	for(let i = 0; i < imgButtons.length; i++) {
		imgButtons[i].addEventListener('click', showImage, false);
	}
}, false);