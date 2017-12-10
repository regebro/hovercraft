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

    // The help is by default shown. Hide it after five seconds.
    setTimeout(function () {
        var helpdiv = window.document.getElementById('hovercraft-help');
        if(helpdiv.className != 'show')
            helpdiv.className = 'hide';
    }, 5000);
}


if (impressConsole) {
    var impressattrs = document.getElementById('impress').attributes;
    var consoleCss = impressattrs['console-css'];
    var previewCss = null;
    if (impressattrs.hasOwnProperty('preview-css')) {
        previewCss = impressattrs['preview-css'];
    }

    impressConsole().init(css=consoleCss, cssPreview=previewCss);

    // P to open Console
    impressConsole().registerKeyEvent([72], help, window);

    if (impressattrs.hasOwnProperty('auto-console') && impressattrs['auto-console'].value.toLowerCase() === 'true') {
        consoleWindow = impressConsole().open();
    }
}

// Function updating the slide number counter
function update_slide_number(evt)
{
    var step = evt.target.attributes['step'].value;
    document.getElementById('slide-number').innerText = parseInt(step) + 1;
}
