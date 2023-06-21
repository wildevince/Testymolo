


function updateSection_figure() {
    // Send AJAX request to load figure
    $.ajax({
        url: '/load-figure',
        dataType: 'html',
        success: function(data) {
            $("#loadingFigure")
                .html(data)
        },
        error: function(error) {
            console.error('Error', error);
        }
    });
}

function updateSection_figure_plus(id) {
    // sent the protein from mainframe to mainminus
    //var csrftoken = getCookie('csrftoken');
    var url = '/plus-figure/' + id + '/';

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
            //csrfmiddlewaretoken: csrftoken,
            protein_id: id 
        },
        dataType: 'html',
        success: function(response) {
            // console log 
            $("#loadingProfile").html("");
            $("#loadingFigure").html(response);
        },
        error: function(error) {
            console.error('Error', error);
        }
    });
}

function updateSection_figure_minus() {
    // sent the protein from mainframe to mainminus
    $.ajax({
        url: '/minus-figure',
        dataType: 'html',
        success: function(data) {
            // add protein in minus focus
            $("#mainminus")
                .append(data);
            sortSection_minusfigure();

            // remove protein in main focus
            $("#loadingFigure")
                .html("")
        },
        error: function(error) {
            console.error('Error', error);
        }
    });
}

function updateSection_modulecard(subseqId) {
    //var csrftoken = getCookie('csrftoken'); 
    var url = '/module/' + subseqId + '/';

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
            //csrfmiddlewaretoken: csrftoken,
            subseq_id: subseqId
        },
        dataType: 'html',
        success: function(response) {
            // do stuff
            $("#modulecard").html(response);
        },
        error: function(error) {
            console.error('Error', error);
        }
    });
}

function sortSection_minusfigure() {
    var $div = $("#mainminus"),
        $div_list = $div.children('svg');

    $div_list.sort(function(a,b){
        var ap = a.getAttribute('protein'),
            bp = b.getAttribute('protein');
        
            if(ap > bp) { 
                return -1;
            }
            if(ap > bp) {
                return 1;
            }
            return 0;
    });

    $div_list.detach().appendTo($div);
}

function makeAsReference(proteinID) {
    $button = $("button#button_" + proteinID);
    $star = $button.children("span");
    if ($star.attr('value') == 'true') {
        console.log("protein " + proteinID + " as reference");
        $star.attr('value', 'false');
        $star.css('color', 'grey');
        $("#loadingFigure button.compare").detach();
    } 
    else if ($star.attr('value') == 'false') {
        console.log("protein " + proteinID + " deselected");
        $star.attr('value', 'true');
        $star.css('color', 'orange');
        $("#loadingFigure .button-container").append("<button class='compare'>Compare with <span class='uni_star' value=false style='color: orange;'>★</span></button>");
    }
}



$(document).ready(function(){

    // generate figure
    updateSection_figure();

    // change opacity on mouseover
    $(document).on("mouseover", "rect.subseq", function() {
        $(this).attr("fill-opacity", "0.8");
        let $id = $(this).attr('id');
        $("#module_name_" + $id).prop("hightlighted", true);
        $("#numbering_" + $id).prop("hightlighted", true);
    });

    $(document).on("mouseout", "rect.subseq", function() {
        $(this).attr("fill-opacity", "0.2");
        let $id = $(this).attr('id');
        $("#module_name_" + $id).prop("hightlighted", false);
        $("#numbering_" + $id).prop("hightlighted", false);
    });

    // click_module
    $(document).on("click", "svg rect.subseq", function() {
        var $id = $(this).attr('subseq');
        // run ajax 
        console.log("ajax to subseq "+ $id);
        updateSection_modulecard($id);
    });

    


})




// utilities
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
 
  
  
  
  
  