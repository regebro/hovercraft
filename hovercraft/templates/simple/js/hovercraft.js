impress().init();

var help = function() {
    var helpdiv = window.document.getElementById('hovercraft-help');
    if(helpdiv.className == 'show')
        helpdiv.className = 'hide';
    else
        helpdiv.className = 'show';    
}

var registerKeyEvent = function(keyCodes, handler, window) {
    if (window === undefined) {
        window = consoleWindow;
    }
    
    // prevent default keydown action when one of supported key is pressed
    window.document.addEventListener("keydown", function ( event ) {
        if ( !event.ctrlKey && !event.altKey && !event.shiftKey && !event.metaKey && keyCodes.indexOf(event.keyCode) != -1) {
            event.preventDefault();
        }
    }, false);
            
    // trigger impress action on keyup
    window.document.addEventListener("keyup", function ( event ) {
        if ( !event.ctrlKey && !event.altKey && !event.shiftKey && !event.metaKey && keyCodes.indexOf(event.keyCode) != -1) {
                handler();
                event.preventDefault();
        }
    }, false);
};

// Toggle help.
registerKeyEvent([72], help, window);

setTimeout(function () {
    var helpdiv = window.document.getElementById('hovercraft-help');
    helpdiv.className = 'hide';
}, 5000);
