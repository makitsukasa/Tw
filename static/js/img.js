window.addEventListener('load', function(){
	const elems = document.getElementsByTagName('img');
	for(let i = 0; i < elems.length; i++) {
		elems[i].addEventListener('error', () => {
			this.style.display = 'none';
		}, false);
	}
}, false);
