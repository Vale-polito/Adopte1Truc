$(document).ready(function)(){
	
	$('.get-more').click(function(){
		
		$.ajax({
			type:"GET",
			url:"/ajax/more/",
			success: function(data){
				for(i=; i<data.length; i++){
					$('ul').append('<li>'+data[i]+'</li>');
				}
			}
		});
	});
});
