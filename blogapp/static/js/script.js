var navbar=document.getElementById("#navi")
var menu=document.getElementById("#menu")

window.onscroll=function(){
    if(window.pageYOffset>=menu.offsetTop){
        navbar.classList.add("sticky")
    }
    else{
        navbar.classList.remove("sticky")
    }
}