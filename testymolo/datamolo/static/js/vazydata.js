
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

function button_fasta_clipboard(){
    $("button.js-copy-fasta-clipboard").click(function(e) {
        //console.log("fasta copied to CLipboard")
        var fasta = $(this).parent().find("textarea").text();
        //console.log(fasta);
        navigator.clipboard.writeText(fasta);
    });
}

function Hide_form_fields() {
    $(".CompletionForm form input[name*='hide']").parent().hide();
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


function fetchTaxonkit() {
    // read input
    // run AJAX taxonkit
    // return HTML in "div.taxonkit div.taxonkit-result"
    taxid = $("input#input-taxid").val();

    var url = '/resumedb/taxonkit/' + taxid + '/';

    $("div.taxonkit div.taxonkit-result").html("...loading...");
    
    AJAX(url, taxid, "div.taxonkit div.taxonkit-result");
}

function add_form_Protein() {
    var url = '/resumedb/addProtein/';
    var selector = "div.CompletionForm span#add_form_Protein";
    $(selector).html("...loading...");

    AJAX(url, 'addProtein', selector);
    //$("div.CompletionForm span#add_form_Protein").html('There there, take an another bite my dear ...');
}

function parse_old_DB() {
    var taxid = $(".CompletionForm").attr('object');
    var url = '/resumedb/parse_vazy_data_1/' + taxid + '/';
    var selector = ".parse_vazy_data_1";

    $(selector).html("...loading...");
    AJAX(url, taxid, selector);
}

function blastp_runner() {
    $("button.blastp_runner").click(function() {
        console.log('clicked');
        var _id = $(this).parent().find("form").attr("protein");
        let url = '/resumedb/blastp/' + _id + '/';
        let selector = 'div.blastp';
        $(selector).html("...launching...");
        AJAX(url, _id, selector);
    });
}

var intervalId = setInterval(function() {
    tempFasta = getCookie('ongoing_blastp')
    if (tempFasta != null) {
        $.ajax({
            url: '/resumedb/blastp_response/',
            dataType: 'html',
            success: function(data) {
                $("div.blastp").html(data);
                blastp_sort_hit_value();
            },
            error: function(error) {
                console.error('Error', error);
            }
        });
        
        clearInterval(intervalId);
    }
}, 1000); // Repeat every 1 second


function blastp_sort_hit_value() {
    $(".blastp .blastp_hit span[value]").each(function() {
        if ($(this).attr('value') != '100.00') {
            $(this).parent().css('background-color: rgb(190,190,190)')
        }
    })
}

function parse_accessionNumber() {
    //AJAX
    var value = $(".NCBIrecord .query #id_accesionNumber").val();
    var url = "https://www.ncbi.nlm.nih.gov/protein/"+value+'/';
    var selector = $(".NCBIrecord .response");
    selector.html('...loading...');
    window.open(url, '_blank').focus();
    //AJAX(url, value, selector);
}


// ######################################################################################################################## //
$(document).ready(function () {

    // TopPanel progression
    TopPanel_hightlight_100();
    TopPanel_mouseover();
    TopPanel_selected();

    button_fasta_clipboard();
    //Hide_form_fields();

    blastp_runner();

    });








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
  