let vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0)

window.onload = function(){
updateActive();
setTargetToActicleA();
	handleResize();
}
function updateActive(){
	let current_page = document.location.pathname.replace(/\pyClocks/g,"").replace(/\//g, "")
	if (!current_page) { current_page = "home" }
	let element = document.getElementById("sidebar" + current_page)
	if ( !element ){ return }
	element.classList.add("active")
}

function setTargetToActicleA(){
	const elements = document.querySelectorAll("article * a");
	elements.forEach((e) => { if (!(e.classList.contains("postLink"))){e.setAttribute("target", "_blank")}})
}

function setMobileView(){
	document.getElementById("postsDiv").classList.add("hidden")
	document.getElementById("logoContent").classList.remove("hidden")
	document.getElementById("hamburgerClosed").classList.remove("hidden");
	document.getElementById("main").classList.add("mob")
	document.getElementById("main").classList.remove("desk")
}

function setDesktopView(){
	document.getElementById("hamburgerClosed").classList.add("hidden");
	document.getElementById("postsDiv").classList.remove("hidden")
	document.getElementById("logoContent").classList.add("hidden")
	document.getElementById("main").classList.add("desk")
	document.getElementById("main").classList.remove("mob")

}

function handleResize(){
	const vw = getViewportWidth();
	if ( vw < 800) {
		setMobileView();
	} else {
		setDesktopView();
	}
}

function getViewportWidth(){
	return Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0)
}

function showSidebar(){
	document.getElementById("postsDiv").classList.remove("hidden")
	document.getElementById("hamburgerClosed").classList.add("hidden")
}
function hideSidebar(){
	document.getElementById("postsDiv").classList.add("hidden")
	document.getElementById("hamburgerClosed").classList.remove("hidden");
}

function handleMainContentClick(){
	if ( !document.getElementById("main").classList.contains("mob")){return}
	hideSidebar();
	showHamburger();
}
