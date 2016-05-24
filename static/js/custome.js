$(document).ready(function(){
    $(".rdo1").click(function(){
      //	un select all
    	$('.rdo').removeClass('rdo_select');

    	//set selected radio button
      $(this).addClass("rdo_select");
      document.getElementById('rdo1').checked=true;
    });
    $(".rdo2").click(function(){
       // un select all
      $('.rdo').removeClass('rdo_select');

      //set selected radio button
      $(this).addClass("rdo_select");
      document.getElementById('rdo2').checked=true;
    });

//date picker
		$( "#datepickerStart" ).datepicker();
		$( "#datepickerEnd" ).datepicker();
 
});
