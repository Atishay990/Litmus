var limiter = {
    allowed: 0, 
    counter: null, 
    textarea: null, 
    init: function(max, counter, textarea){
      limiter.allowed = max;
      limiter.counter = counter;
      limiter.counter.innerHTML = limiter.allowed;
      limiter.textarea = textarea;
      limiter.textarea.setAttribute("maxlength", limiter.allowed);
      limiter.textarea.addEventListener("keyup", limiter.update);
      limiter.textarea.removeAttribute("disabled");
    },
    update: function(evt){
      let remain = limiter.allowed - limiter.textarea.value.length;
      limiter.counter.innerHTML = remain;
    },
  };
  window.onload = function(){
    limiter.init(
      1000,
      document.getElementById("remain"),
      document.getElementById("textin")
    );
  }; 


  const friend_request = document.getElementById("req-btn");
const friend_request_area = document.getElementById("friend-req-area");
friend_request.onclick = function(){
  if(window.getComputedStyle(friend_request_area).display === "none") {
    friend_request_area.style.display="block";
  }else{
    friend_request_area.style.display="none";
  }
} 


var slideIndex = 1;
showDivs(slideIndex);

function plusDivs(n) {
  showDivs(slideIndex += n);
}

function showDivs(n) {
  var i;
  var x = document.getElementsByClassName("mySlides");
  if (n > x.length) {slideIndex = 1}
  if (n < 1) {slideIndex = x.length}
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";  
  }
  x[slideIndex-1].style.display = "block";  
}

var mybutton = document.getElementById("myBtnscroll");

 // When the user scrolls down 20px from the top of the document, show the button
 window.onscroll = function() {
     scrollFunction()
    };
 
 function scrollFunction() {
   if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
     mybutton.style.display = "block";
   } else {
     mybutton.style.display = "none";
   }
 }
 
 // When the user clicks on the button, scroll to the top of the document
 function topFunction() {
   document.body.scrollTop = 0; // this is for mac users
   document.documentElement.scrollTop = 0; // this is for windows user

 }

 const font_selection_region = document.getElementById("font-family-tool");
 const font_size_selection_region = document.getElementById("font-size-tool");
 function displayTools()
 {
   if(window.getComputedStyle(font_selection_region).display === "none") {
     font_selection_region.style.display="block";
     font_size_selection_region.style.display="none";
     }else{
    font_selection_region.style.display="none";
   }

 }

// for font family
 var selected_font = document.getElementById("font-family-input");
 var fontStyle_textArea = document.getElementById("textin");

function inputfamily(family)
{
  selected_font.value= family;
  selectedFont();
}
function selectedFont()
{
  if(selected_font.value==="")
  {
    selected_font.value='Monospace';
  }
  var font_input = selected_font.value;
  fontStyle_textArea.style.fontFamily = font_input;
  selected_font.style.fontFamily=font_input;
}
function selectedFontremove(){
  selectedFont();
  font_selection_region.style.display="none";
}
