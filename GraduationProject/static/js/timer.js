$(document).ready(function() {
    // timer function
    function startTimer(duration, display) {
        var timer = duration, minutes, seconds;
        var refresh = setInterval(function () {
            minutes = parseInt(timer / 60, 10)
            seconds = parseInt(timer % 60, 10);

            minutes = minutes < 10 ? "0" + minutes : minutes;
            seconds = seconds < 10 ? "0" + seconds : seconds;

            var output = minutes + " : " + seconds;
            display.text(output);
            $("title").html(output);

            if (--timer < 0) {
                display.text("Time's Up!");
                clearInterval(refresh);  // exit refresh loop
                document.getElementById("time").style.color = "red";
                // alert("Time is up!")
                // document.getElementById("submit").click();
            }
        }, 1000);

    }

    // start timer
    jQuery(function ($) {
        var display = $('#time');
        startTimer(Seconds, display);
    });

})
