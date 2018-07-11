var ajaxRequest;  // The variable that makes Ajax possible!
function ajaxFunction() {
   try {
      // Opera 8.0+, Firefox, Safari
      ajaxRequest = new XMLHttpRequest();
   } catch (e) {
   
      // Internet Explorer Browsers
      try {
         ajaxRequest = new ActiveXObject("Msxml2.XMLHTTP");
      } catch (e) {
      
         try {
            ajaxRequest = new ActiveXObject("Microsoft.XMLHTTP");
         } catch (e) {
      
            // Something went wrong
            alert("Your browser broke!");
            return false;
         }
      }
   }
}


function validateUserId() {
    ajaxFunction();
    
    // Here processRequest() is the callback function.
    ajaxRequest.onreadystatechange = processRequest;
    
    if (!target) target = document.getElementById("userid");
    var url = "validate?id=" + escape(target.value);
    
    ajaxRequest.open("GET", url, true);
    ajaxRequest.send(null);
 }

 var a = $('#mydiv').data('myval'); //getter
 
 

$(function() {
    $("#client_name").autocomplete({
      source: "api/get_client_name/",
      minLength: 2, 
      autoFocus: true, 
    });
    // $('#client_id').attr("value", client);
  });

$(function() {
    $("#client_email").autocomplete({
      source: "api/get_client_email/",
      minLength: 2,
      autoFocus: true,
    })  ;
  });

$(function() {
    $("#client_phone").autocomplete({
      source: "api/get_client_phone/",
      minLength: 2,
      autoFocus: true,
    });
  });


// $( ".selector" ).autocomplete({
//     select: function(event, ui) { ... }
//  });

// goToClient({})



