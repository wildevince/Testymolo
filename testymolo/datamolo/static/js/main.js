function updateSection_figure() {
    // Send AJAX request to load figure
    $.ajax({
        url: '/load-figure',
        dataType: 'html',
        success: function(data) {
            $("#loadingFigure")
                .html(data)
                .prop('loaded', true);
        },
        error: function(error) {
            console.error('Error', error);
        }
    });
}

$(document).ready(function(){

    // generate figure
    updateSection_figure();

    // change opacity on mouseover
    $(document).on("mouseover", "rect.subseq", function() {
        $(this).attr("fill-opacity", "0.8");
        //let $id = $(this).attr('id');
        //$("#module_name_" + $id).prop("hightlighted", true);
        //$("#numbering_" + $id).prop("hightlighted", true);
    });

    $(document).on("mouseout", "rect.subseq", function() {
        $(this).attr("fill-opacity", "0.2");
        //let $id = $(this).attr('id');
        //$("#module_name_" + $id).prop("hightlighted", false);
        //$("#numbering_" + $id).prop("hightlighted", false);
    });

})



