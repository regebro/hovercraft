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
console().init(cssFile='css/impressConsole.css');

var impressattrs = document.getElementById('impress').attributes
if (impressattrs.hasOwnProperty('auto-console') && impressattrs['auto-console'].value === 'True') {
    consoleWindow = console().open();
    /*
        
        console().registerKeyEvent([78], showSlideNumbers);
        console().registerKeyEvent([83], showSlideSources); */
}

console().registerKeyEvent([78], showSlideNumbers, window);
console().registerKeyEvent([83], showSlideSources, window);
