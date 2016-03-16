$(document).ready(function () {
    path = window.location.pathname;
    $('#menu > li > a').each(function () {
        if ($(this).attr('href') == path.substring(0, $(this).attr('href').length)) {
            $(this).parent().addClass('active');
        }
    });

    $(".clickable-row").click(function() {
        window.document.location = $(this).data("href");
    });

    $('#draft').ready(toggleSendButtonText);
    $('#draft').click(toggleSendButtonText);
})

var toggleSendButtonText = function () {
    if ($('#draft').is(':checked')) {
        $("#send-button").text("Save");
    } else {
        $("#send-button").text("Send");
    }
}