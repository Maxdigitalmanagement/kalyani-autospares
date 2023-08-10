$('.slider_wrap').slick({
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    arrows: false,
    autoplay: true,
    autoplaySpeed: 2000,
});

$('.slider_wrap2').slick({
    dots: false,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    arrows: false,
    autoplay: true,
    autoplaySpeed: 1000,
});

const sec1 = document.querySelector('.section1');
 
function setsechei(){
    if(window.innerWidth>801){
         sec1.style.maxHeight = per(sec1.clientWidth,70) + "px";
         console.log(per(sec1.clientWidth,70));
    }
    else{
        sec1.style.maxHeight = "100%";
    }
}


const fader = document.querySelector('.faders');
const slideBike  = document.querySelector('.bikes');
const imgw = document.querySelector('.imagewraper');
const imgs = document.querySelectorAll('.imgs');

var img = 0;

window.addEventListener('resize',dothis,false);

function dothis() {

    setsechei();

    if (per(imgw.scrollHeight, 80) >= imgw.scrollWidth) {
        for (var i = 0; i < imgs.length; i++) {
            imgs[i].style.width = "auto"
            imgs[i].style.height = "100%"
        }
    }
    else {

        for (var i = 0; i < imgs.length; i++) {
            imgs[i].style.width = "100%"
            imgs[i].style.height = "auto"
        }

    }


    console.log()

    fader.style.height=slideBike.clientHeight+"px";
    fader.style.width=(slideBike.clientWidth+3)+"px";

    console.log()
    

}

dothis();




