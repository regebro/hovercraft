// Keypress handler to go to a specific slide
function goto_slide()
{
    var key = event.charCode || event.keyCode;
    // 103 = "g"
    if(key == 103)
    {
        var target = prompt("Enter slide number");
        if (isNaN(target)) {
            var goto_status = impress().goto(target);
        } else {
            // goto(0) goes to step-1, so substract 1
            var goto_status = impress().goto(parseInt(target) - 1);
        }
        if (goto_status === false) {
            alert("Slide not found: '" + target + "'");
        }
    }
}

// register "g" key handler to jump to a slide
document.addEventListener("keypress", goto_slide);
