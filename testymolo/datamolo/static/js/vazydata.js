
function TopPanel_hightlight_100() {
    $(".TopPanel p span.progress").each(function () {
        let txt = $(this).html();
        if (txt == "100.0") {
            $(this).parent().css("font-weight", "bold");
        }
        else if (txt != "0.0") {
            $(this).css("font-weight", "bold");
        }
    });
}

function TopPanel_mouseover() {
    $(".TopPanel p button").on('mouseover', function () {
        $(this).css("border", "darkblue solid 1px");
        $(this).css("background", "rgb(235,235,235)");
    });
    $(".TopPanel p button").on('mouseout', function () {
        $(this).css("border", "rgb(220,220,255) solid 1px");
        $(this).css("background", "none");
    });
}

function TopPanel_selected() {
    $(".TopPanel p button").on('click', function () {
        $(".TopPanel p button.selected").each(function () {
            $(this).css("text-decoration", "none");
            $(this).removeClass('selected');
        });
        if(! $(this).hasClass("selected")) {
            $(this).addClass('selected');
            $(this).css("text-decoration", "underline");
        }
    });
}

// AJAX
function AJAX(url, value, parentDOM) {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!this.crossDomain) {
                var csrftoken = getCookie('csrftoken');
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            }
        }
    });
    $.ajax({
        url: url,
        method: 'POST',
        data: { 
            key: value 
        },
        dataType: 'html',
        success: function(response) {
            $(parentDOM).html(response);
        },
        error: function(error) {
            console.error('Error', error);
        }
    });
}



// ######################################################################################################################## //
$(document).ready(function () {

    // TopPanel progression
    TopPanel_hightlight_100();
    TopPanel_mouseover();
    TopPanel_selected();

});