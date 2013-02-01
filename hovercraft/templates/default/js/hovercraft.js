var showSlideNumbers = function() {
    var asides = document.getElementsByClassName('page_number');
    var hidden = asides[0].style.display != 'block';
    for (var i = 0; i < asides.length; i++) {
        asides.item(i).style.display = hidden ? 'block' : 'none';
    }
};

var showSlideSources = function() {
    var asides = document.getElementsByClassName('source');
    var hidden = asides[0].style.display != 'block';
    for (var i = 0; i < asides.length; i++) {
        asides.item(i).style.display = hidden ? 'block' : 'none';
    }
};

impress().init();
console().init(cssFile="css/impressConsole.css");
/* console().open();*/

console().registerKeyEvent([78], showSlideNumbers)
console().registerKeyEvent([78], showSlideNumbers, window)
console().registerKeyEvent([83], showSlideSources)
console().registerKeyEvent([83], showSlideSources, window)
