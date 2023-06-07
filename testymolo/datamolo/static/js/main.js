$(document).ready(function() {

    $("p").hover(function(){
        $(this).css('color','red');
    })

    $("div#data_fig").hover(
        function()
        {
            var $this = $(this);

            $this
                .data('prehovercolor', $this.css('color'))
                .css('color', '#aaa');
        },
        function()
        {
            var $this = $(this);
            $this
                .css('color', $this.data('prehovercolor'));
        }
    );

});