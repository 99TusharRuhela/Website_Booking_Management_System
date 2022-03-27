odoo.define('ak_website_booking_system.custom_booking_template', function (require) {
"use strict";
  
});

var modal = document.getElementById("myModal");
console.log("111111111111111", modal)
// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];
console.log("222222222222222", span)
// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  console.log("333333333333333333")
  modal.style.display = "none";
}
// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}
// When the user clicks the button, open the modal
function click_book_now(){
	var book_btn =$(event.target);
	var book_product_id;
	if(book_btn.hasClass('book-style')){
		book_product_id = book_btn.next().val()
  }
  else{
    book_product_id = book_btn.parent().next().val()
  }
	$.ajax({
		url: "/get/popup/modal",
    method: "POST",
    contentType: 'application/json',
    data: JSON.stringify({"params": {
    	"book_product_id":book_product_id,
      }}),
     success: function(result) {
      var modal = document.getElementById("myModal");
     	$(modal).find(".modal-content")[0].innerHTML=result.result['template_data']
     	modal.style.display = "block";
    },
	});
}

function select_date() {
	var temp_get_day =$(event.target);
	var get_day;
	var get_config_id;
	var book_product_id;

	if(temp_get_day.hasClass('style-active-day')){
		get_day = temp_get_day.children().text()
		get_config_id = temp_get_day.children().next().val()
		book_product_id = temp_get_day.children().next().next().val()
  }
  else{
    get_day = temp_get_day.text()
    get_config_id = temp_get_day.next().val()
    book_product_id = temp_get_day.next().next().val()
  }
  $.ajax({
		url: "/get/popup/modal/time",
    method: "POST",
    contentType: 'application/json',
    data: JSON.stringify({"params": {
    	"get_config_id":get_config_id,
    	"book_product_id":book_product_id,
      }}),
     success: function(result) {
     	var modalTime = document.getElementById("modalTime");
     	$(modalTime).find(".modal-content-time")[0].innerHTML=result.result['template_data_time']
     	// var modalPlan = document.getElementById("modalPlan");
     	// $(modalPlan).find(".modal-content-plan")[0].innerHTML=result.result['template_data_plan']
    },
	});
}


function select_seat(ev) {
  var $link = $(event.target);
  var $input = $link.closest('.input-group').find("input");
  var min = parseFloat($input.data("min") || 0);
  var max = parseFloat($input.data("max") || Infinity);
  var previousQty = parseFloat($input.val() || 0, 10);
  var quantity = ($link.has(".fa-minus").length ? -1 : 1) + previousQty;
  var newQty = quantity > min ? (quantity < max ? quantity : max) : min;
  var seat_qty = document.getElementsByClassName("qty-seat")[0].innerText

  if (newQty !== previousQty && newQty <= seat_qty) {
      $input.val(newQty).trigger('change');
  }

  var temp_select_seat = $input.val();
  var span_plan_price = document.getElementsByClassName("style-active-plan")[0].children[2].innerText
  var temp = span_plan_price.match(/\d+/)[0]
  var amt = temp_select_seat * temp
  var total_amt = "$ "+amt+".0"
  document.getElementById("myAmt").value = total_amt;
}


function Change(node){
 var j=document.getElementsByClassName("style-active-day");
  for(var i=0;i<j.length;i++){
    j[i].className="style-td";
    }  
  node.className="style-active-day";   
}

function ChangeTime(node){
 var j=document.getElementsByClassName("style-active-time");
  for(var i=0;i<j.length;i++){
    j[i].className="style-td";
    }  
  node.className="style-active-time";
  var temp_get_time =$(event.target);
  var book_slot_time_id;
  var product_template_id;

  if(temp_get_time.hasClass('style-active-time')){
    book_slot_time_id = temp_get_time.children().next().val()
    product_template_id = temp_get_time.children().next().next().val()
  }
  else {
    book_slot_time_id = temp_get_time.next().val()
    product_template_id = temp_get_time.next().next().val()
  }

  $.ajax({
    url: "/get/popup/modal/slot/time",
    method: "POST",
    contentType: 'application/json',
    data: JSON.stringify({"params": {
      "book_slot_time_id":book_slot_time_id,
      'product_template_id':product_template_id,
      }}),
     success: function(result) {
      var modalPlan = document.getElementById("modalPlan");
      $(modalPlan).find(".modal-content-plan")[0].innerHTML=result.result['template_data_plan']
    },
  });   
}

function ChangePlan(node){
 var j=document.getElementsByClassName("style-active-plan");
  for(var i=0;i<j.length;i++){
    j[i].className="style-td";
    }  
  node.className="style-active-plan";   
}

function close_modal() {
	var check =$(event.target);
	var modal=check.parent().parent()
	location.reload();
}

