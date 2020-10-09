$(document).ready(function(){
	let data = JSON.parse('{{ movie["overview"] | tojson }}');
	$(".movie-image").hover(function(){
		

	},
	function()
	{
		$(this).find(".play").hide();
	});


	$(".blink").focus(function() {
            if(data==this.value) {
                this.value = '';
            }
        })
        .blur(function(){
            if(this.value=='') {
                this.value = data;                    
			}
		});
});
