$(document).ready(function() {
    // timer function
    function startTimer(duration, display, spendtime) {
        var timer = duration, minutes, seconds;
        var refresh = setInterval(function () {
            minutes = parseInt(timer / 60, 10)
            seconds = parseInt(timer % 60, 10);

            minutes = minutes < 10 ? "0" + minutes : minutes;
            seconds = seconds < 10 ? "0" + seconds : seconds;

            var output = minutes + " : " + seconds;
            display.text(output);
            // $("title").html(output);

            // var spend = duration-timer;
            //
            // var spendminutes = parseInt(spend / 60, 10)
            // var spendseconds = parseInt(spend % 60, 10);
            //
            // spendminutes = spendminutes < 10 ? "0" + spendminutes : spendminutes;
            // spendseconds = spendseconds < 10 ? "0" + spendseconds : spendseconds;
            //
            // var spendoutput = spendminutes + " : " + spendseconds;
            // $("spendtime").html(duration);
            //

            spendtime.text(duration-timer);

            if(vue.finish === true){
                clearInterval(refresh);
            }

            if (--timer < 0) {
                display.text("Time's Up!");
                clearInterval(refresh);  // exit refresh loop
                document.getElementById("time").style.color = "red";
                vue.submit();
            }
        }, 1000);
    }

    // start timer
    jQuery(function ($) {
        var display = $('#time');
        var spendtime = $('#spendtime');
        startTimer(Seconds, display, spendtime);
    });

})
