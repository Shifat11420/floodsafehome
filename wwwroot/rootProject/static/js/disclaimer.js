
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

  /*
  $('#create_pdf').click(function() {
	//convert pdf_wrap to canvas
	html2canvas($('#pdf_wrap')[0]).then(function(canvas) {
		var doc = new jsPDF('p', 'mm', 'a4'); //generate jspdf
    var imgData = canvas.toDataURL('image/png'); //canvas to image
    doc.addImage(imgData, 'PNG', 0, 0); //generate pdf based on image 
    doc.save('sample-file.pdf'); //save as a pdf
  });
});
*/
// Hide Header on on scroll down 
