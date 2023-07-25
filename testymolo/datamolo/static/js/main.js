
function updateSection_figure() {
    // Send AJAX request to load figure
    $.ajax({
        url: '/load-figure',
        dataType: 'html',
        success: function(data) {
            $("#loadingFigure").html(data);
            //figure
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

    AJAX(url, id, "#loadingFigure");
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

            // random protein in main focus
            updateSection_figure();
        },
        error: function(error) {
            console.error('Error', error);
        }
    });
}

function updateSection_modulecard(subseqId) {
    //var csrftoken = getCookie('csrftoken'); 
    var url = '/module/' + subseqId + '/';

    AJAX(url, subseqId, "#modulecard");
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

function updateSection_profile(profileId) {
    // sent the protein from mainframe to mainminus
    //var csrftoken = getCookie('csrftoken');
    var url = '/profile/' + profileId + '/';

    AJAX(url, profileId, "#loadingProfile");

    intervalId;
}

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

function updateSection_logo(profileId) {
    var url = '/load-logo/' + profileId + '/';
    AJAX(url, profileId, "#loadingProfile div.logo")
}

function session_refresh() {
    // delete the cookie
    //document.cookie = 'session' + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    // ajax 
    var url = '/new-session/';
    $.ajax({
        url: url,
        dataType: 'html',
        success: function(response) {
<<<<<<< HEAD
            document.open("text/html", "replace");
=======
            //console.log("session: "+response);
            document.open();
>>>>>>> 2d7fe3c7a4cade570a3b7bd45ee9457e1c77de84
            document.write(response);
            document.close();
        },
        error: function(error) {
            console.error('Error', error);
        }
    });
}

// intervally (1 sec) check if logo is finish and fetch the logo figure
var intervalId = setInterval(function() {

    tempFasta = getCookie('tempFasta')
    if (tempFasta != null) {
        // AJAX request to fetch HTML content
        // AJAX(url, tempFasta, "#mainfocus #loadingProfile");
        $.ajax({
            url: '/check_logo',
            dataType: 'html',
            success: function(data) {
                $("#mainfocus #loadingProfile").html(data);
            },
            error: function(error) {
                console.error('Error', error);
            }
        });
        
        // Clear the interval once the cookie is found
        clearInterval(intervalId);
    }
}, 1000); // Repeat every 1 second


//######################################################################



$(document).ready(function(){

    // check cookie 'session'
    var session = getCookie('session');
    if(session) {
        console.log("session: "+session)
    } else {
        session_refresh();
    }

    //setInterval(function(){console.log("Hey dude !")},1000);

    


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
        console.log("ajax to subseq " +$id);
        updateSection_modulecard($id);
    });


    $(document).on("mouseover", "p.profile", function() {
        $(this).css('color', 'purple');
    });
    $(document).on("mouseout", "p.profile", function() {
        $(this).css('color', 'blue');
    });
    $(document).on("click", "p.profile", function() {
        var $id = $(this).attr('id');
        console.log("ajax to profile " +$id);
        updateSection_profile($id);
    });


    // auto-hide minus protein if in mainfocus
    $.when($("#loadingFigure svg")).then(function(self) {
        var proteinID = $(self).attr('protein');
        $.when($("#mainminus svg")).then(function(self) {
            let minusprotID = $(self).attr('protein');
            if(minusprotID == proteinID) {
                $(self).hide();
            }
        });
    });
    


    // look for witness to search for logo(SVG)
    //$.when($("#loadingProfile div.logo")).then((self) => {});
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

function checkCookie(cookieName) {
    var cookieValue = document.cookie.replace(/(?:(?:^|.*;\s*) + cookieName \s*=\s*([^;]*).*$)|^.*$/, "$1");
    return cookieValue !== undefined;
}
  
  
  
  
  