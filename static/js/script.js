
//$(document).ready(function(){
//    $('.form-group').hide();
//    $('.btn1').mouseover(function(){
//        $('.form-group').show();
//    });
//});
/*display menu nav in single.html*/
$('.tab').each(function() {
    $(this).css('display', 'none');
});
function hide_item(){
	$('.tab').each(function() {
	    $(this).css('display', 'none');
	});
    }
   
function show(para){
     hide_item();
     //alert(para);
     document.getElementById("id"+para).style.display = "block";     
}

