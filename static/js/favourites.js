document.addEventListener("mousemove",parallax);
document.addEventListener("mouseleave",parallaxres);


function parallax(e){
    document.querySelectorAll(".levitate").forEach(function(move){
        var moving_value = move.getAttribute("data-value");
        var x = e.clientX * moving_value/200;
        var y = e.clientY * moving_value/200;
        move.style.transform = "translateX(" + x + "px) translateY(" + y + "px)";
    });
}

function parallaxres(){
    document.querySelectorAll(".levitate").forEach(function(move){
        move.style.transform = "translateX(" + 0 + "px) translateY(" + 0 + "px)";
    });
}


const chek = document.getElementById('ChekBox');
const empty = document.querySelector('.wr_empty');
const heading = document.querySelector('.section1');
const topmarg = document.querySelector('.topmar');

function displayc(){
    if(chek.checked){
        console.log("checked");
        empty.style.display = "none";
        heading.style.display = "flex";
    }
    else{
        console.log("unchecekd")
        heading.style.display = "none";
        topmarg.style.display = "none";
    }
}

displayc();

window.addEventListener('resize',displayc)

