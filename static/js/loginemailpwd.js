
var passwordInput = document.getElementById("password-input");
var toggleButton = document.getElementById("toggle-button");
var toggleimg = document.getElementById("toggleimg");

const container = document.querySelector('.containermain');

const emailinput = document.getElementById('email-input');


window.addEventListener('load', settop, false);
window.addEventListener('resize', settop, false);

function settop(){
    if(container.scrollHeight>window.innerHeight){
        if(!container.classList.value.includes('justop')){
            container.classList.add('justop');
        }
        activeelement();
    }
    else{
        container.classList.remove('justop');
    }
}

function activeelement(){
    if(document.activeElement === emailinput){
        location.href='#emailwrp';
        emailinput.focus();
    }
    else if(document.activeElement === document.getElementById('password-input')){
        location.href='#passwrp';
        document.getElementById('password-input').focus();
    }
    else if(document.activeElement === document.getElementById('confirm-input')){
        location.href='#confirmwrp';
        document.getElementById('confirm-input').focus();
    }
    else if(document.activeElement === document.getElementById('firstname-input')){
        location.href='#firstnamewrp';
        document.getElementById('firstname-input').focus();
    }
    else if(document.activeElement === document.getElementById('lastname-input')){
        location.href='#lastnamewrp';
        document.getElementById('lastname-input').focus();
    }
    else if(document.activeElement === document.getElementById('phone-input')){
        location.href='#phonewrp';
        document.getElementById('phone-input').focus();
    }
    else{
        console.log("topp")
        location.href='#top';
    }
}




// location.href='loginnewpwd.html'