function change_slide_number(e)
{
	var step = e.target.attributes['step'].value;
    document.getElementById('slide-number').innerText = parseInt(step) + 1;
}

function goto_slide_number(e)
{
    var key = event.charCode || event.keyCode;
    if(key == 103)
    {
        var target = prompt("Enter slide number");
        target = parseInt(target) - 1;
        impress().goto(target);
    }
}
