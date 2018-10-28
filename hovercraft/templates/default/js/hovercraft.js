// Main hovercraft js file
( function( document ) {
    "use strict";

    document.addEventListener( "impress:init", function( event ) {

        var api = event.detail.api;
        var util = api.lib.util;


        // Set up the help-box
        // Overwrite the default navigation help
        util.triggerEvent( document, "impress:help:add", { command: "Left, Down, Page Down, Space",
                                                           text: "Next step",
                                                           row: 1 } );
        util.triggerEvent( document, "impress:help:add", { command: "Right, Up, Page Up",
                                                           text: "Previous step",
                                                           row: 2 } );
    });

    // Initialize impress.js
    impress().init();

    var impressattrs = document.getElementById('impress').attributes;
    if (impressattrs.hasOwnProperty('auto-console') && impressattrs['auto-console'].value.toLowerCase() === 'true') {
        impressConsole().open();
    }

}) (document);


// Function updating the slide number counter
function update_slide_number(evt)
{
    var step = evt.target.attributes['step'].value;
    document.getElementById('slide-number').innerText = parseInt(step) + 1;
}
