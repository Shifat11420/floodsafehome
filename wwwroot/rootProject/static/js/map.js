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
  
  /*image slider*/
  var img = document.getElementById('img');
  var img_array = ['static/img/construction/zero.png','static/img/construction/onefoot.png','static/img/construction/twofeet.png', 'static/img/construction/threefeet.png', 'static/img/construction/fourfeet.png'];
  function setImage(obj)
  {
  var value = obj.value;
  img.src = img_array[value];
    
  }

  var img2 = document.getElementById('img2');
  var img2_array = ['static/img/construction/zero.png','static/img/construction/onefoot.png','static/img/construction/twofeet.png', 'static/img/construction/threefeet.png', 'static/img/construction/fourfeet.png'];
  function setImage(obj)
  {
  var value = obj.value;
  img2.src = img2_array[value];
    
  }
  
  /* slider number:X zone with insurance*/
  var slider = document.getElementById("myRange");
  var output = document.getElementById("demo");
  output.innerHTML = slider.value;
  
  slider.oninput = function() {
  output.innerHTML = this.value;
  }
  
  
  var freeboard = document.getElementById("freeboard");
  var freeboard_array = ["{{FreeboardCost0}}", "{{FreeboardCost1}}", "{{FreeboardCost2}}", "{{FreeboardCost3}}", "{{FreeboardCost4}}"];
  function setValue()
  {
  var value = obj.value;
  freeboard.scr = freeboard_array[value];
  }
  
  (function() {
  const pricingSliders = document.querySelectorAll(".pricing-slider");
  
  if (pricingSliders.length > 0) {
    for (let i = 0; i < pricingSliders.length; i++) {
      const pricingSlider = pricingSliders[i];
  
      // Build the input object
      const pricingInput = {
        el: pricingSlider.querySelector("input")
      };
      pricingInput.data = JSON.parse(
        pricingInput.el.getAttribute("data-price-input")
      );
      pricingInput.currentValEl = pricingSlider.querySelector(
        ".pricing-slider-value"
      );
      pricingInput.thumbSize = parseInt(
        window
          .getComputedStyle(pricingInput.currentValEl)
          .getPropertyValue("--thumb-size"),
        10
      );
  
      // Build the output array
      const pricingOutputEls = pricingSlider.parentNode.querySelectorAll(
        ".pricing-item-price"
      );
      const pricingOutput = [];
      for (let i = 0; i < pricingOutputEls.length; i++) {
        const pricingOutputEl = pricingOutputEls[i];
        const pricingOutputObj = {};
        pricingOutputObj.currency = pricingOutputEl.querySelector(
          ".pricing-item-price-currency"
        );
        pricingOutputObj.amount = pricingOutputEl.querySelector(
          ".pricing-item-price-amount"
        );
        pricingOutputObj.after = pricingOutputEl.querySelector(
          ".pricing-item-price-after"
        );
        pricingOutputObj.data = JSON.parse(
          pricingOutputEl.getAttribute("data-price-output")
        );
        pricingOutput.push(pricingOutputObj);
      }
        
      pricingInput.el.setAttribute("min", 0);
      pricingInput.el.setAttribute(
        "max",
        Object.keys(pricingInput.data).length - 1
      );
      !pricingInput.el.getAttribute("value") &&
        pricingInput.el.setAttribute("value", 0);
  
      handlePricingSlider(pricingInput, pricingOutput);
      window.addEventListener("input", function() {
        handlePricingSlider(pricingInput, pricingOutput);
      });
    }
  }
  
  function handlePricingSlider(input, output) {
    // output the current slider value
    if (input.currentValEl)
      input.currentValEl.innerHTML = input.data[input.el.value];
    // update prices
    for (let i = 0; i < output.length; i++) {
      const outputObj = output[i];
      if (outputObj.currency)
        outputObj.currency.innerHTML = outputObj.data[input.el.value][0];
      if (outputObj.amount)
        outputObj.amount.innerHTML = outputObj.data[input.el.value][1];
      if (outputObj.after)
        outputObj.after.innerHTML = outputObj.data[input.el.value][2];
    }
    handleSliderValuePosition(input);
  }
  
  function handleSliderValuePosition(input) {
    const multiplier = input.el.value / input.el.max;
    const thumbOffset = input.thumbSize * multiplier;
    const priceInputOffset =
      (input.thumbSize - input.currentValEl.clientWidth) / 2;
    input.currentValEl.style.left =
      input.el.clientWidth * multiplier - thumbOffset + priceInputOffset + "px";
  }
  })();


  
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
  
  /* Add/Delete fields 
  function add(type) {
  
      //Create an input type dynamically.
      var element = document.createElement("input");
  
      //Assign different attributes to the element.
      element.setAttribute("type", type);
      element.setAttribute("value", type);
      element.setAttribute("name", type);
  
  
      var foo = document.getElementById("fooBar");
  
      //Append the element in page (in span).
      foo.appendChild(element);
  
  }*/
  
  let mainNavLinks = document.querySelectorAll("nav ul li a");
  let mainSections = document.querySelectorAll("main section");
  
  let lastId;
  let cur = [];
  
  // This should probably be throttled.
  // Especially because it triggers during smooth scrolling.
  // https://lodash.com/docs/4.17.10#throttle
  // You could do like...
  // window.addEventListener("scroll", () => {
  //    _.throttle(doThatStuff, 100);
  // });
  // Only not doing it here to keep this Pen dependency-free.
  
  
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
  