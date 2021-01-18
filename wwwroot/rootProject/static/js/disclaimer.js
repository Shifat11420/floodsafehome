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


/* Gague 
let chartConfig = {
type: 'gauge',
backgroundColor: 'none',
plot: {
  tooltip: {
    visible: false
  },
  aperture: 180,
  backgroundColor: 'none',
  csize: '4px'
},
plotarea: {
  margin: '100px 0px 0px 0px',
  backgroundColor: 'none',
  borderWidth: '0px'
},
scaleR: {
  aperture: 180,
  backgroundColor: 'none',
  center: {
    backgroundColor: 'none',
    borderColor: 'none',
    size: '0px'
  },
  item: {
    padding: '5px',
    fontColor: '#1E5D9E',
    fontFamily: 'Montserrat',
    offsetR: 0
  },
  maxValue: 500,
  minValue: 0,
  ring: {
    rules: [
      {
        backgroundColor: '#d7191c',
        rule: '%v < 100'
      },
      {
        backgroundColor: '#fdae61',
        rule: '%v >= 100 && %v < 200'
      },
      {
        backgroundColor: '#f7f783',
        rule: '%v >= 200 && %v < 300'
      },
      {
        backgroundColor: '#a6d96a',
        rule: '%v >= 300 && %v < 400'
      },
      {
        backgroundColor: '#1a9641',
        rule: '%v >= 400'
      }
    ],
    size: '3px'
  },
  step: 1,
  tick: {
    lineColor: '#1E5D9E',
    placement: 'out'
  }
},
series: [
  {
    text: 'Internal',
    values: [256],
    backgroundColor: '#1E5D9E',
    lineColor: '#00BAF2'
  }
]
};

zingchart.render({
id: 'myChart',
data: chartConfig,
height: '50%',
width: '50%',
});
*/

/*image slider*/
var img = document.getElementById('img');
var img_array = ['static/img/construction/zero.png','static/img/construction/onefoot.png','static/img/construction/twofeet.png', 'static/img/construction/threefeet.png', 'static/img/construction/fourfeet.png'];
function setImage(obj)
{
var value = obj.value;
img.src = img_array[value];
  
}

/* slider number*/
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



let chartConfig = {
  type: 'line',
  title: {
    text: 'Freeboard cost'
  },
  subtitle: {
    text: 'Click and check label vertically.'
  },
  plot: {
    tooltip: {
      visible: false
    },
    cursor: 'hand'
  },
  scaleX: {
    markers: [],
    offsetEnd: '85px',
    labels: ['BFE +0 feet', 'BFE +1 feet', 'BFE +2 feet', 'BFE +3 feet', 'BFE +4 feet']
  },
  crosshairX: {},
  series: [
    {
      text: 'Freeboard cost',
      values: ["{{total_annual_premium_BFE}}", "{{total_annual_premium_BFE1}}", "{{total_annual_premium_BFE2}}", "{{total_annual_premium_BFE3}}", "{{total_annual_premium_BFE4}}"]
    }
  ]
};

/*zingchart*/
// DEFINE CHART LOCATIONS (IDS)
// -----------------------------
// Main chart render location
// var chartId = 'myChart';
var chart1Id = 'chart1';
var chart2Id = 'chart2';


// CHART DATA
// -----------------------------

var views = ["{{ freeboardCost0|escape}}","{{ freeboardCost1|escape}}","{{ freeboardCost2|escape}}","{{ freeboardCost3|escape}}","{{ freeboardCost4|escape}}"];

var showings = ["{{total_annual_premium_BFE|escape}}","{{total_annual_premium_BFE1|escape}}","{{total_annual_premium_BFE2|escape}}","{{total_annual_premium_BFE3|escape}}","{{total_annual_premium_BFE4|escape}}"];


// CHART CONFIG
// -----------------------------

// Chart 1
var chart1Data = {
  type: 'line',
  title: {
    text: 'Freeboard cost graph',
    fontWeight: 'normal',
    fontColor: 'var(--black)',
    align: 'left',
    marginLeft: '2rem'
  },
  tootltip: {
    visible:false
  },
  cursor: 'hand',
  globals: {
    fontColor: 'var(--fontColor)',
    fontFamily: 'Roboto'
  },
  legend: {
    borderWidth: 0,
    layout: '1',
    marker: {
      type: 'pie'
    }
  },
  scaleX: { 
    markers: [],
    labels: ['BFE +0 ft', 'BFE +1 ft', 'BFE +2 ft', 'BFE +3 ft', 'BFE +4 ft'],
    tick: {
      visible: false
    },
  crosshairX: {},
  },
  plot: {
    aspect: 'spline'
  },
  series: [
    {
      values: views,
      text: 'Freeboard cost'
      
    }
  ]
};

// Chart 2
var chart2Data = {
  type: 'line',
  title: {
    text: 'Insurance savings per year',
    align: 'left',
    fontColor: 'var(--black)',
    fontWeight: 'normal',
    marginLeft: '2rem'
  },
  tooltip: {
    visible: false
  },
  cursor: 'hand',
  globals: {
    fontColor: 'var(--fontColor)',
    fontFamily: 'Roboto'
  },
  legend: {
    borderWidth: 0,
    layout: '1',
    marker: {
      type: 'pie'
    }
  },  
  scaleX: { 
    markers: [],
    labels: ['BFE +0 ft', 'BFE +1 ft', 'BFE +2 ft', 'BFE +3 ft', 'BFE +4 ft'],
    tick: {
      visible: false
    },
  crosshairX: {},
  },
  plot: {
    aspect: 'spline'
  },
  series: [
    {
      values: showings,
      text: 'Insurance saving'
    }
  ]
};


// RENDER CHARTS
// -----------------------------

// Chart 1
zingchart.render({ 
  id: chart1Id, 
  data : chart1Data, 
  width: '100%'
});

// Chart 2
zingchart.render({ 
  id: chart2Id, 
  data : chart2Data, 
  width: '100%'
});