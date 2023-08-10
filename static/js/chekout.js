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





var add_name = "";
var add_house_no = "";
var add_roadname_area = "";
var add_city = "";
var add_state = "";
var add_pincode = "";

const checkboxes = document.querySelectorAll('.addresses_to_select input[type="checkbox"]');
const addresses = document.querySelectorAll('.address_wr');

function handleCheckboxChange(e) {
    // Uncheck all checkboxes except the one that triggered the event
    checkboxes.forEach(checkbox => {
        if (checkbox !== e.target) {
            checkbox.checked = false;
        }
    });

    setaddress();


}

setaddress();

function setaddress(){
    addresses.forEach(function (ele) {
        const chkbox = ele.querySelector('input[type="checkbox"]');
    
        if (chkbox.checked) {
            add_name = ele.querySelector('h2[id="ship_name"]').innerHTML;
            add_house_no = ele.querySelector('h4[id="houseno"]').innerHTML;
            add_roadname_area = ele.querySelector('h4[id="Roadname_area_colony"]').innerHTML;
            add_city = ele.querySelector('h4[id="city"]').innerHTML;
            add_state = ele.querySelector('h4[id="State"]').innerHTML;
            add_pincode = ele.querySelector('span[id="pincode"]').innerHTML;
        }
    });
}

checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', handleCheckboxChange);
});

const continuebtn = document.querySelector('.chekout');

continuebtn.addEventListener('click',()=>{
    vibrate();
    alert(add_name+add_house_no+add_roadname_area+add_city+add_state+add_pincode);
});





window.addEventListener('resize',dothis,false);
window.addEventListener('load',dothis,false);

function dothis(){
    const addwr = document.querySelector('.select_address');
    const faders = document.querySelector('.faders');

    faders.style.width= (addwr.clientWidth + 1) + "px";
    console.log(addwr.clientWidth + "px")

}