const namelogo = document.getElementById('name_logo');
const input = document.getElementById('inputHolder');

const sbleft = document.getElementById('sbleft');
const sbcont = document.getElementById('sbcont');

const back = document.getElementById('backBtn');


if(back){
    back.addEventListener('click',function(event){
        event.preventDefault();
        history.back();
        vibrate();
    });
}

var preLoader = document.getElementById("preloader");
window.addEventListener("load", function () {
    preLoader.style.display = "none";
});


if(input){
    input.addEventListener('focus', () => {
        namelogo.style.display = "none";
        sbcont.style.width = "100%";
        sbleft.style.width = "100%";
        input.style.width = "100%";
    });

    if (input.value.length >= 1) {
        namelogo.style.display = "none";
        sbcont.style.width = "100%";
        sbleft.style.width = "100%";
        input.style.width = "100%";
    }
    
    input.addEventListener('focusout', () => {
    
        if (input.value.length >= 1) {
            namelogo.style.display = "none";
            sbcont.style.width = "100%";
            sbleft.style.width = "100%";
            input.style.width = "100%";
        }
        else {
            namelogo.style.display = "flex";
            sbcont.style.width = "40px";
            sbleft.style.width = "40px";
            input.style.width = "40px";
        }
    });
}






function per(given, cent) {

    var perse = given / 100;
    return perse * cent;

}

// set dragable to the slides with class name "draggable_sl"

const productsd = document.querySelectorAll('.draggable_sl');
for (var i = 0; i < productsd.length; i++) {
    setDraggable(productsd[i]);
}


function setDraggable(products) {

    let isDown = false;
    let startX;
    let scrollLeft;

    products.addEventListener('mousedown', (e) => {
        isDown = true;
        products.classList.add('active');
        startX = e.pageX - products.offsetLeft;
        scrollLeft = products.scrollLeft;
    });
    products.addEventListener('mouseleave', () => {
        isDown = false;
        products.classList.remove('active');
    });
    products.addEventListener('mouseup', () => {
        isDown = false;
        products.classList.remove('active');
    });
    products.addEventListener('mousemove', (e) => {
        if (!isDown) return;
        e.preventDefault();
        const x = e.pageX - products.offsetLeft;
        const walk = (x - startX); //scroll-fast
        products.scrollLeft = scrollLeft - walk;
    });

}



function vibrate(){
    if ('vibrate' in navigator) {
        // Event listener for the click event
          navigator.vibrate(50);
          console.log('Vibrated');
      } else {
        console.log('Vibration API is not supported.');
      }
}



