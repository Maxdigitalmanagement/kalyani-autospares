document.addEventListener("mousemove", parallax);
document.addEventListener("mouseleave", parallaxres);


function parallax(e) {
    document.querySelectorAll(".levitate").forEach(function (move) {
        var moving_value = move.getAttribute("data-value");
        var x = e.clientX * moving_value / 200;
        var y = e.clientY * moving_value / 200;
        move.style.transform = "translateX(" + x + "px) translateY(" + y + "px)";
    });
}

function parallaxres() {
    document.querySelectorAll(".levitate").forEach(function (move) {
        move.style.transform = "translateX(" + 0 + "px) translateY(" + 0 + "px)";
    });
}


const chek = document.getElementById('ChekBox');
const empty = document.querySelector('.wr_empty');
const heading = document.querySelector('.section1');
const topmarg = document.querySelector('.topmar');

function displayc() {
    if (chek.checked) {
        console.log("checked");
        empty.style.display = "none";
        heading.style.display = "flex";
    }
    else {
        console.log("unchecekd")
        heading.style.display = "none";
        topmarg.style.display = "none";
    }
}

displayc();

window.addEventListener('resize', displayc)


const cartwarp = document.querySelector('.cart_items_wrap');
const right = document.querySelector('.sec1_right');
const left = document.querySelector('.sec1_left');
const sect1 = document.querySelector('.section1');

if (sect1.clientHeight > left.scrollHeight) {
    left.classList.add('justcen');
}

setmarbot();

function setmarbot() {
    if (window.innerWidth <= 800) {
        cartwarp.style.paddingBottom = (right.clientHeight) + "px";
    }
}





var addr_id = "";

const checkboxes = document.querySelectorAll('.addresses_to_select input[type="checkbox"]');
const addresses = document.querySelectorAll('.address_wr');

function handleCheckboxChange(e) {
    // Uncheck all checkboxes except the one that triggered the event
    checkboxes.forEach(checkbox => {
        if (checkbox !== e.target) {
            checkbox.checked = false;
        }
    });

}

checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', handleCheckboxChange);
});

const continuebtn = document.querySelector('.chekout');

continuebtn.addEventListener('click',()=>{
    vibrate();
    var chek = false
    addresses.forEach(function (ele) {
        const chkbox = ele.querySelector('input[type="checkbox"]');
    
        if (chkbox.checked) {
            chek = true
            document.querySelector("input[name='addr_id']").value = ele.querySelector('h4[id="addr_id"]').textContent;
        }
    });
    if(chek){
        document.getElementById('place_order_btn').click();
    }
    else{
        alert("select address");
    }
});



window.addEventListener('resize',dothis,false);
window.addEventListener('load',dothis,false);

function dothis(){
    const addwr = document.querySelector('.select_address');
    const faders = document.querySelector('.faders');

    faders.style.width= (addwr.clientWidth + 1) + "px";
    console.log(addwr.clientWidth + "px")

}