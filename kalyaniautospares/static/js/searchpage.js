const sitem = document.querySelectorAll('.sitem');
const bikefltrwrap = document.querySelectorAll('.bikefilter_wrap');
const sort_item_short = document.querySelector('.sort_short');
var sort_opt = document.querySelector('input[name="sortop"]:checked');
const sortbg = document.querySelector('.sort_big');
const sortCont = document.querySelector('.conten');

const radiobtns_short = document.querySelectorAll('input[name="sortop"]');
const radiobtns_shorts = document.querySelectorAll('input[name="sortopb"]');
var sort_clear = document.querySelector('.clearsort');
var sort_clears = document.querySelector('.clearsorts');


for (var i = 0; i < sitem.length; i++) {
    seton(sitem[i]);
}

sortbg.addEventListener('click', ()=>{
    if(sortCont.classList.value.includes('dsflex')){
        sortCont.classList.remove('dsflex');
        sort_clears.classList.remove('dflex');
        sortbg.classList.remove('paddtopbot');
        setchb();
    }
    else{
        sortCont.classList.add('dsflex');
        sort_clears.classList.add('dflex');
        sortbg.classList.add('paddtopbot');
    }
})



function seton(sitem) {
    sitem.addEventListener('click', (sitem) => {
        if (sitem.srcElement.classList.value.includes('sitem') & !(sitem.srcElement.classList.value.includes('sort_big'))) {
            sitem.srcElement.classList.toggle('activesitem');
        }
    });
}


var sortPopup = document.getElementById('sortPopup');
var closeSortPopup = document.getElementById('closeSortPopup');
sort_item_short.addEventListener('click', function(event) {
    sortPopup.style.display = 'block';
    vibrate();
});
closeSortPopup.addEventListener('click', function() {
    sortPopup.style.display = 'none';
    setch();
});



sort_clear.addEventListener('click', () => {
    radiobtns_short.forEach((radio) => {
        radio.checked = false;
    })
    radiobtns_shorts.forEach((radio) => {
        radio.checked = false;
    })
});

sort_clears.addEventListener('click', () => {
    radiobtns_shorts.forEach((radio) => {
        radio.checked = false;
    })
    radiobtns_short.forEach((radio) => {
        radio.checked = false;
    })
});



function setchb(){
    var selectedOption=0;

    if(selectedOption = document.querySelector('input[name="sortopb"]:checked')){
        if(!sortbg.classList.value.includes('activesitem')){
            sortbg.classList.add('activesitem');
        }
    }
    else{
        if(sortbg.classList.value.includes('activesitem')){
            sortbg.classList.remove('activesitem');
        }
    }
}


function setch(){
    var selectedOption=0;

    if(selectedOption = document.querySelector('input[name="sortop"]:checked')){
        sort_opt=document.querySelector('input[name="sortop"]:checked').id;
        console.log(selectedOption , sort_opt);
        if(!sort_item_short.classList.value.includes('activesitem')){
            sort_item_short.classList.add('activesitem');
        }
        if(!sort_clear.classList.value.includes('dflex')){
            sort_clear.classList.add('dflex');
        }
    }
    else{
        if(sort_item_short.classList.value.includes('activesitem')){
            sort_item_short.classList.remove('activesitem');
        }
        if(sort_clear.classList.value.includes('dflex')){
            sort_clear.classList.remove('dflex');
        }
    }

}





