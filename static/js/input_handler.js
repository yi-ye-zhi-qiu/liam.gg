//focus input on page load
input = $("#input-box")
input.focus()

//form-delay;
const form = $("#riot-api-form");
    form.submit(() => {
  //some other functions you need to proceed before submit
    var box_opacity = $('.ghgtu').css('opacity', '1');
    setTimeout(() => {}, 0.5);
           return true;
});

$('.button--bubble').each(function() {
  var $circlesTopLeft = $(this).parent().find('.circle.top-left');
  var $circlesBottomRight = $(this).parent().find('.circle.bottom-right');

  var tl = new TimelineLite();
  var tl2 = new TimelineLite();

  var btTl = new TimelineLite({ paused: true });

  tl.to($circlesTopLeft, 1.2, { x: -25, y: -25, scaleY: 2, ease: SlowMo.ease.config(0.1, 0.7, false) });
  tl.to($circlesTopLeft.eq(0), 0.1, { scale: 0.2, x: '+=6', y: '-=2' });
  tl.to($circlesTopLeft.eq(1), 0.1, { scaleX: 1, scaleY: 0.8, x: '-=10', y: '-=7' }, '-=0.1');
  tl.to($circlesTopLeft.eq(2), 0.1, { scale: 0.2, x: '-=15', y: '+=6' }, '-=0.1');
  tl.to($circlesTopLeft.eq(0), 1, { scale: 0, x: '-=5', y: '-=15', opacity: 0 });
  tl.to($circlesTopLeft.eq(1), 1, { scaleX: 0.4, scaleY: 0.4, x: '-=10', y: '-=10', opacity: 0 }, '-=1');
  tl.to($circlesTopLeft.eq(2), 1, { scale: 0, x: '-=15', y: '+=5', opacity: 0 }, '-=1');

  var tlBt1 = new TimelineLite();
  var tlBt2 = new TimelineLite();

  tlBt1.set($circlesTopLeft, { x: 0, y: 0, rotation: -45 });
  tlBt1.add(tl);

  tl2.set($circlesBottomRight, { x: 0, y: 0 });
  tl2.to($circlesBottomRight, 1.1, { x: 30, y: 30, ease: SlowMo.ease.config(0.1, 0.7, false) });
  tl2.to($circlesBottomRight.eq(0), 0.1, { scale: 0.2, x: '-=6', y: '+=3' });
  tl2.to($circlesBottomRight.eq(1), 0.1, { scale: 0.8, x: '+=7', y: '+=3' }, '-=0.1');
  tl2.to($circlesBottomRight.eq(2), 0.1, { scale: 0.2, x: '+=15', y: '-=6' }, '-=0.2');
  tl2.to($circlesBottomRight.eq(0), 1, { scale: 0, x: '+=5', y: '+=15', opacity: 0 });
  tl2.to($circlesBottomRight.eq(1), 1, { scale: 0.4, x: '+=7', y: '+=7', opacity: 0 }, '-=1');
  tl2.to($circlesBottomRight.eq(2), 1, { scale: 0, x: '+=15', y: '-=5', opacity: 0 }, '-=1');

  tlBt2.set($circlesBottomRight, { x: 0, y: 0, rotation: 45 });
  tlBt2.add(tl2);

  btTl.add(tlBt1);
  btTl.to($(this).parent().find('.button.effect-button'), 0.8, { scaleY: 1.1 }, 0.1);
  btTl.add(tlBt2, 0.2);
  btTl.to($(this).parent().find('.button.effect-button'), 1.8, { scale: 1, ease: Elastic.easeOut.config(1.2, 0.4) }, 1.2);

  btTl.timeScale(2.6);

  $(this).on('mouseover', function() {
    btTl.restart();
  });
});

window.addEventListener('scroll', scrollFunc);

function scrollFunc() {
    var windowScroll = this.scrollY;

    var $logo = document.getElementsByClassName('logo')[0];
    $logo.style.transform = 'translateY(' + windowScroll/2 + '%)';

    var $backBird = document.getElementsByClassName('back-bird')[0];
    $backBird.style.transform = 'translateY(' + windowScroll/4 + '%)';

    var $foreBird = document.getElementsByClassName('fore-bird')[0];
    $foreBird.style.transform = 'translateY(-' + windowScroll/100 + '%)';

}


function fade_out(element) {
    var op = 1;  // initial opacity
    var timer = setInterval(function () {
        if (op >= 0.05){
            clearInterval(timer);
            element.style.display = 'none';
        }
        element.style.opacity = op;
        element.style.filter = 'alpha(opacity=' + op * 100 + ")";
        op -= op * 0.1;
    }, 50);
    element.dataset.state ='faded_out'
}

function fade_in(element) {
    var op = 1;  // initial opacity
    var timer = setInterval(function () {
        if (op >= 0.1){
            clearInterval(timer);
            element.style.display = 'block';
        }
        element.style.opacity = op;
        element.style.filter = 'alpha(opacity=' + op * 100 + ")";
        op -= op * 0.1;
    }, 50);
    element.dataset.state ='faded_in'
}

var show_deets = document.querySelectorAll('.game_deets')
var btn = document.querySelectorAll('.content')
for (let i = 0; i < btn.length; i++) {
    btn[i].addEventListener("click", function() {
      if(show_deets[i].dataset.state==='faded_out'){ fade_in(show_deets[i])}
      else{fade_out(show_deets[i])}
    });
}


var stats = document.querySelector('#xgboost_reveal')
var stats_underneath = document.querySelectorAll('.xgboost_result')

stats.addEventListener('click', function() {
  stats_underneath.forEach(e => {
    if(e.classList.contains('is-hidden')){
      e.style.display = 'block'
      e.classList.remove('is-hidden')
    } else {
      e.style.display = 'none'
      e.classList.add('is-hidden')
    }
  })
})


let color_selector = () => {

  var border = document.querySelector('.bird-box'),
   borders = document.querySelectorAll('.content'),
   lp = document.querySelector('.lp'),
   wins = document.querySelector('.wins'),
   loses = document.querySelector('.loses'),
   rank = document.querySelector('#persons-rank'),
   color_arr = [['bronze', '#d4a373'],['silver','#d2d2cf'],
                  ['gold','#ffb646'],['diamond','#9bf6ff'],
                  ['master','#7371fc'],
                  ['challenger','linear-gradient(100deg, #ffabab, #ffdaab, #ddffab, #abe4ff, #d9abff)']];
  if(rank != ''){
    for(let i=0; i<color_arr.length; i++){
      if(color_arr[i][0] === rank.textContent.toLowerCase()){
        border.style.borderBottom = '10px solid'+color_arr[i][1]
        for( let j=0; j<borders.length; j++){
          borders[j].style.borderCollapse = 'separate'
          borders[j].style.borderSpacing = '5px'
          borders[j].style.paddingBottom = '10px'
          borders[j].style.borderBottom = '2px solid'+color_arr[i][1]
        }
      }
    }
  }
}
color_selector()
