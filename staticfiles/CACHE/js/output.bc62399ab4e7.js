$("#daily").on('click',function(){if($("#daily_time").is(":hidden")){$("#daily_time").removeAttr('hidden');$("#submit_btn").css('visibility','hidden');$("#daily_time").slideDown();}
else{$("#daily_time").hide();$("#time").val('');$("#submit_btn").css('visibility','visible');$("#daily_time").slideUp();}});;