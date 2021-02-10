// When the user scrolls the page, execute myFunction
window.onscroll = function() {stick_nav()};

var navbar = document.querySelector(".navbar");

var sticky = navbar.offsetTop;

function stick_nav() {
  if (window.pageYOffset >= sticky) {
    console.log(navbar)
    navbar.classList.add("sticky")
  } else {
    navbar.classList.remove("sticky");
  }
}
