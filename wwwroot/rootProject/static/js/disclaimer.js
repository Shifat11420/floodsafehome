jQuery(document).ready(function($){
  
  window.onload = function (){
    $(".bts-popup").delay(1000).addClass('is-visible');
    }
  
    //open popup
    $('.bts-popup-trigger').on('click', function(event){
        event.preventDefault();
        $('.bts-popup').addClass('is-visible');
    });
    
    //close popup
    $('.bts-popup').on('click', function(event){
        if( $(event.target).is('.bts-popup-close') ) {
            event.preventDefault();
            $(this).removeClass('is-visible');
        }
    });
    //close popup when clicking the esc keyboard button
    $(document).keyup(function(event){
        if(event.which=='27'){
            $('.bts-popup').removeClass('is-visible');
        }
    });

var didScroll; 
var lastScrollTop = 0; 
var delta = 5; 
var navbarHeight = $('header').outerHeight(); 
$(window).scroll(function(event){
didScroll = true; 
}); 
setInterval(function() {
if (didScroll) { 
hasScrolled(); didScroll = false; }
}, 250); 

function hasScrolled() { 
var st = $(this).scrollTop(); 

// Make sure they scroll more than delta 
if(Math.abs(lastScrollTop - st) <= delta) 

return; 

// If they scrolled down and are past the navbar, add class .nav-up. 
// This is necessary so you never see what is "behind" the navbar. 

if (st > lastScrollTop && st > navbarHeight){ 
// Scroll Down 
$('header').removeClass('nav-down').addClass('nav-up'); } else { 
// Scroll Up 
if(st + $(window).height() < $(document).height()) { 
$('header').removeClass('nav-up').addClass('nav-down'); 
} 
}
lastScrollTop = st; 
}


});


/*Toggling visibility*/
function ShowHideDiv() {
  var chkYes = document.getElementById("chkYes");
  var dvPassport = document.getElementById("dvPassport");
  var as = document.getElementById("as");
  var chkNo = document.getElementById("chkNo");

  dvPassport.style.display = chkYes.checked ? "block" : "none";
  as.style.display = chkNo.checked ? "block" : "none";
  
}

function ShowHideDiv2() {
  var chkYes = document.getElementById("chkYes2");
  var singleBuilding = document.getElementById("singleBuilding");
  var chkNo = document.getElementById("chkNo2");
  var SpatialScale = document.getElementById("SpatialScale");

  singleBuilding.style.display = chkYes.checked ? "block" : "none";  
  SpatialScale.style.display = chkNo.checked ? "block" : "none";
  
}

//Show and hide advanced function
function displayAdv() {
    
  if ($("#adv_Box_Div").is(':hidden')) {
      $("#adv_Box_Div").show();
     //$("#buttonAdv").css('background-color', 'grey');
      
  } else {
      $("#adv_Box_Div").hide();
      //$("#buttonAdv").addClass('btn-adv-close');
  }
}



function ShowHideDiv3() {
  var chkTenant = document.getElementById("chkTenant");
  var dvPassport = document.getElementById("dvPassport");
  var as = document.getElementById("as");
  var chkNo = document.getElementById("chkNo");


  dvPassport.style.display = chkTenant.checked ? "block" : "none";  
  as.style.display = chkNo.checked ? "block" : "none";
}

function ShowHideDiv4() {
  var dvPassport = document.getElementById("dvPassport");
  var chkLandlord = document.getElementById("chkLandlord");
  var as = document.getElementById("as");
  var chkNo = document.getElementById("chkNo");
  
  dvPassport.style.display = chkLandlord.checked ? "block" : "none";
  as.style.display = chkNo.checked ? "block" : "none";
  
}

let mainNavLinks = document.querySelectorAll("nav ul li a");
let mainSections = document.querySelectorAll("main section");

let lastId;
let cur = [];


/*Side menu highlighting based on scrolling*/
window.addEventListener("scroll", event => {
  let fromTop = window.scrollY;

  mainNavLinks.forEach(link => {
    let section = document.querySelector(link.hash);

    if (
      section.offsetTop <= fromTop &&
      section.offsetTop + section.offsetHeight > fromTop
    ) {
      link.classList.add("current");
    } else {
      link.classList.remove("current");
    }
  });
});
