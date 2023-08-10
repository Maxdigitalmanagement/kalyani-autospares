$('.slider_wrap').slick({
    dots: true,
    infinite: false,
    speed: 500,
    slidesToShow: 1,
    arrows: false,
    autoplay: true,
    autoplaySpeed: 5000,
});

const left = document.querySelector('.sec1_left');
const right = document.querySelector('.sec1_right');

const minus = document.getElementById('minus_btn');
const plus = document.getElementById('plus_btn');
const itemno = document.getElementById('item_no');
const like = document.getElementById('like');
const favou = document.getElementById('favou');
const likecontainer = document.getElementById('likecontainer');





function handleSizeChange() {
    if (left.clientHeight > right.clientHeight+20) {
        if(!right.classList.value.includes('grat')){
            right.classList.add('grat');
        }
    }
    else{
        if(right.classList.value.includes('grat')){
            right.classList.remove('grat');
        }
    }
}

window.addEventListener('resize', handleSizeChange,false);

handleSizeChange();


var items = 1;
plus.addEventListener('click', () => {
    if (items < 10) {
        items++;
        console.log(items)

        if (items < 10) {
            itemno.innerHTML = "0" + items;
        }
        else {
            itemno.innerHTML = items;
        }

    }

})

minus.addEventListener('click', () => {
    if (items > 1) {
        items--;
        console.log(items)
        itemno.innerHTML = "0" + items;
    }

})

likecontainer.addEventListener('click', () => {
    prchk();
});


prchk();

function prchk() {
    if (like.checked) {
        likecontainer.style.backgroundColor = '#214CDB';
    }
    else {
        likecontainer.style.backgroundColor = '#B3B3B3';
    }
}

const sec1 = document.querySelector('.section1');
 
function setsechei(){
    if(window.innerWidth>1200){
         sec1.style.maxHeight = per(sec1.clientWidth,70) + "px";
         console.log(per(sec1.clientWidth,70));
    }
    else{
        sec1.style.maxHeight = "100%";
    }
}

window.addEventListener('load',setsechei);
window.addEventListener('resize',setsechei);
