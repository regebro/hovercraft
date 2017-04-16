function insert_slide_numbers()
{
    var slides = document.getElementsByClassName("step");
    for(var i = 0; i < slides.length; i++)
    {
        var slide = slides[i];
        var slidenumberdiv = document.createElement('DIV');
        slidenumberdiv.innerText = parseInt(slide.attributes['step'].value) + 1;
        slidenumberdiv.classList.add('slide-number');
        slide.appendChild(slidenumberdiv, null);
    }
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
