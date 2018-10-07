/**
 * gotoSlide.js
 *
 * An impress.js plugin to move to a specific slide number
 *
 * MIT Licensed, see license.txt.
 *
 * Copyright 2012-2017 impress-console contributors (see README.txt)
 *
 */

(function ( document, window ) {

    var gotoSlide = function (event) {
        var target = event.view.prompt("Enter slide number or id");

        if (isNaN(target)) {
            var goto_status = impress().goto(target);
        } else if (target === null) {
            return;
        } else {
            // goto(0) goes to step-1, so substract
            var goto_status = impress().goto(parseInt(target) - 1);
        }
        if (goto_status === false) {
            event.view.alert("Slide not found: '" + target + "'");
        }
    };

    document.addEventListener( "impress:init", function( event ) {
        var api = event.detail.api;
        var util = api.lib.util;


        document.addEventListener( "keyup", function( event ) {

            if ( event.keyCode === 71 ) { // "g"
                event.preventDefault();
                gotoSlide( event );
            }
        }, false );

        util.triggerEvent( document, "impress:help:add",
                           {command: "G",
                            text: "Go to slide",
                            row: 3 }
        );

    });

})(document, window);
