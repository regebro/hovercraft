impress().init();
console().init(cssFile='css/impressConsole.css');

var help = function() {
    var helpdiv = window.document.getElementById('hovercraft-help');
    if(helpdiv.className == 'show')
        helpdiv.className = 'hide';
    else
        helpdiv.className = 'show';    
}

// Toggle help.
console().registerKeyEvent([72], help, window);

setTimeout(function () {
    var helpdiv = window.document.getElementById('hovercraft-help');
    helpdiv.className = 'hide';
}, 5000);

var impressattrs = document.getElementById('impress').attributes
if (impressattrs.hasOwnProperty('auto-console') && impressattrs['auto-console'].value.toLowerCase() === 'true') {
    consoleWindow = console().open();
}
