// Initialize impress.js
impress().init();

// Set up the help-box
var helpdiv = window.document.getElementById('hovercraft-help');

if (window.top!=window.self) {
    // This is inside an iframe, so don't show the help.
    helpdiv.className = "disabled";

} else {
    // Install a funtion to toggle help on and off.
    var help = function() {
        if(helpdiv.className == 'hide')
            helpdiv.className = 'show';
        else
            helpdiv.className = 'hide';
    };
    impressConsole().registerKeyEvent([72], help, window);

    // The help is by default shown. Hide it after five seconds.
    setTimeout(function () {
        var helpdiv = window.document.getElementById('hovercraft-help');
        if(helpdiv.className != 'show')
            helpdiv.className = 'hide';
    }, 5000);
}


if (impressConsole) {
    impressConsole().init(cssFile='css/impressConsole.css');

    var impressattrs = document.getElementById('impress').attributes
    if (impressattrs.hasOwnProperty('auto-console') && impressattrs['auto-console'].value.toLowerCase() === 'true') {
        consoleWindow = console().open();
    }
}
