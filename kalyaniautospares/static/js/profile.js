
const sec1 = document.querySelector('.section1');
const wrp = document.querySelector('.wrapper');

var i = 0;

function setlay() {
    if (window.innerWidth > 800 ) {
        if (wrp.scrollHeight > window.innerHeight - 70) {
            console.log(true)
            if (sec1.classList.value.includes('cencen')) {
                sec1.classList.remove('cencen');
                dliveredord.style.height = "max-content";
                processingord.style.height = hhh + "max-content";
                cancelledord.style.height = hhh + "max-content";
            }
        }
        else {
            if (!sec1.classList.value.includes('cencen')) {
                sec1.classList.add('cencen');
                if (i < 1) {
                    var hhh = allorders.scrollHeight;
                    console.log(hhh);
                    dliveredord.style.height = hhh + "px";
                    processingord.style.height = hhh + "px";
                    cancelledord.style.height = hhh + "px";
                    i++;
                }
            }
        }
    }


    if (document.querySelector(".navradios")) {
        if (document.querySelector(".navradios").scrollWidth > window.innerWidth - 40) {
            document.querySelector('.navradios').style.overflow = "scroll";
            setDraggable(document.querySelector('.navradios'));
        }
        else {
            document.querySelector('.navradios').style.overflow = "hidden";
            document.querySelector(".navradios").classList.remove("draggable_sl");
        }
    }


}



window.addEventListener('resize', setlay, false);
window.addEventListener('load', setlay, false);

const stat = document.querySelectorAll('.ot_det_st h3');
stat.forEach(element => {
    if (element.innerHTML.toUpperCase() == "DELIVERED") {
        element.style.color = "#27AE60"
    }
    if (element.innerHTML.toUpperCase() == "PROCESSING") {
        element.style.color = "#F2C94C"
    }
    if (element.innerHTML.toUpperCase() == "CANCELLED") {
        element.style.color = "#EB5757"
    }
    if (element.innerHTML.toUpperCase() == "NEW") {
        element.style.color = "#214CDB"
    }

});



var radios = document.querySelectorAll('input[type=radio][name="slider"]');

radios.forEach(radio => radio.addEventListener('change', setorderslayout));

const allorders = document.querySelector(".allord");
const neworders = document.querySelector(".neword");
const dliveredord = document.querySelector(".deliord");
const processingord = document.querySelector(".possord");
const cancelledord = document.querySelector(".cancord");

function setorderslayout() {
    if (document.getElementById("allorders").checked === true) {
        console.log(true);
        allorders.classList.add("disfle")
    }
    else {
        allorders.classList.remove("disfle");
    }

    if (document.getElementById("new").checked === true) {
        console.log(true);
        neworders.classList.add("disfle")
    }
    else {
        neworders.classList.remove("disfle");
    }

    if (document.getElementById("delivered").checked === true) {
        dliveredord.classList.add("disfle");
    }
    else {
        dliveredord.classList.remove("disfle");
    }

    if (document.getElementById("processing").checked === true) {
        processingord.classList.add("disfle");
    }
    else {
        processingord.classList.remove("disfle");
    }
    
    if (document.getElementById("cancelled").checked === true) {
        cancelledord.classList.add("disfle");
    }
    else {
        cancelledord.classList.remove("disfle");
    }
}


// **************** 
// myreviews page things
// ****************


const chek = document.getElementById('ChekBox');
const empty = document.querySelector('.wr_empty');
const heading = document.querySelector('main');
const topmarg = document.querySelector('.topmar');

function displayc(){
    if(chek.checked){
        console.log("checked");
        heading.style.display = "flex";
    }
    else{
        console.log("unchecekd")
        empty.style.display = "flex";
        heading.style.display = "none";
    }
}

window.addEventListener('load',()=>{
    displayc();
});



// **************** 
// my_orders page things
// ****************


const ordcheckboxes = document.querySelectorAll('.order_wrap input[type="checkbox"]');

ordcheckboxes.forEach(checkbox => {
    checkbox.addEventListener('change', handleordCheckboxChange);
});

function handleordCheckboxChange(e) {
    ordcheckboxes.forEach(checkbox => {
        if (checkbox !== e.target) {
            checkbox.checked = false;
        }
    });
}



// **************** 
// saved_cards page things
// ****************




const cardcheckboxes = document.querySelectorAll('.card_wrap input[type="checkbox"]');

cardcheckboxes.forEach(checkbox => {
    checkbox.addEventListener('change', handlecardCheckboxChange);
});

function handlecardCheckboxChange(e) {
    cardcheckboxes.forEach(checkbox => {
        if (checkbox !== e.target) {
            checkbox.checked = false;
        }
    });
}



// *******************
// My_info page things
// *******************


var passwordInput = document.getElementById("password-input");
var toggleButton = document.getElementById("toggle-button");
var toggleimg = document.getElementById("toggleimg");
const btnsave_info = document.querySelector('.btn_save_info');

function togglePasswordVisibility() {

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        toggleimg.src = "/images/togglevisible.svg";
    } else {
        passwordInput.type = "password";
        toggleimg.src = "/images/togglehide.svg";
    }


}


const btnsEd = document.querySelectorAll('.btn_edit');
btnsEd.forEach(btnEd => {
    btnEd.addEventListener('click', () => {
        if (btnEd.parentElement.querySelector('input').readOnly) {
            btnEd.parentElement.querySelector('input').readOnly = false;
            btnEd.parentElement.querySelector('input').style.color = "#214CDB";
            btnEd.style.display = "none";
            btnsave_info.style.display = "flex";
        }
    });
});



btnsave_info.addEventListener('click', ()=>{
    document.getElementById('saveinfo').click();
});



const inputss = document.querySelectorAll('.wrpp input')
console.log(inputss);

inputss.forEach(inp => {
    inp.addEventListener('focus', () => {
        console.log("#"+inp.parentElement.id,findpos(inp.parentElement));

        if(inp === document.getElementById('phone-input')){
            window.scroll(0,findpos(inp.parentElement.parentElement));
        }
        else{
            window.scroll(0,findpos(inp.parentElement));
        }

    });
});


function scrolltothe(){
    if(document.activeElement === document.getElementById('phone-input')){
        window.scroll(0,findpos(document.activeElement.parentElement.parentElement));
    }
    else{
        window.scroll(0,findpos(document.activeElement.parentElement));
    }
}


function findpos(obj){
    var currenttop = -60;
    if(obj.offsetParent){
        do{
            currenttop+=obj.offsetTop;
        }while((obj=obj.offsetParent));
        return [currenttop];
    };
}



window.addEventListener('resize', scrolltothe, false);
