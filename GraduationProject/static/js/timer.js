$(document).ready(function() {
    // timer function
    function startTimer(duration, display, spendtime, count) {
        var timer = duration, minutes, seconds;
        var refresh = setInterval(function () {
            minutes = parseInt(timer / 60, 10)
            seconds = parseInt(timer % 60, 10);

            minutes = minutes < 10 ? "0" + minutes : minutes;
            seconds = seconds < 10 ? "0" + seconds : seconds;

            var output = minutes + " : " + seconds;
            if (timer < 20) {
                display.text("Hurry up! You have "+output+" left!");
            }else{
                display.text(output);
            }

            spendtime.text(duration-timer);
            count.text(timer);


            if(vue.finish === true){
                clearInterval(refresh);
            }

            const newtime = timer;

            $('#addTime1').click(function () {
                if(vue.timeCap1 > 0){
                    timer = newtime+10, minutes, seconds;
                    document.getElementById("addTime1").disabled = true;
                    setTimeout(function(){document.getElementById("addTime1").disabled = false;},5000);
                }
            })

            $('#addTime2').click(function () {
                if(vue.timeCap2 > 0){
                    timer = newtime+20, minutes, seconds;
                    document.getElementById("addTime2").disabled = true;
                    setTimeout(function(){document.getElementById("addTime2").disabled = false;},5000);
                }
            })

            if (--timer < 0) {
                display.text("Time's Up!");
                clearInterval(refresh);  // exit refresh loop
                document.getElementById("time").style.color = "red";
                vue.submit();
                $('#addTime1').prop('disabled', true);
                $('#addTime2').prop('disabled', true);
            }
        }, 1000);
    }

    // start timer
    jQuery(function ($) {
        var display = $('#time');
        var spendtime = $('#spendtime');
        var count = $('#count');
        startTimer(Seconds, display, spendtime, count);
    });
})


// function addTimer(duration, display, spendtime) {
//         var timer = duration, minutes, seconds;
//         var refresh = setInterval(function () {
//             minutes = parseInt(timer / 60, 10)
//             seconds = parseInt(timer % 60, 10);
//
//             minutes = minutes < 10 ? "0" + minutes : minutes;
//             seconds = seconds < 10 ? "0" + seconds : seconds;
//
//             var output = minutes + " : " + seconds;
//             display.text(output);
//
//             spendtime.text(duration-timer);
//
//             if(vue.finish === true){
//                 clearInterval(refresh);
//             }
//
//             if (--timer < 0) {
//                 display.text("Time's Up!");
//                 clearInterval(refresh);  // exit refresh loop
//                 document.getElementById("time").style.color = "red";
//                 vue.submit();
//             }
//         }, 1000);
// }
