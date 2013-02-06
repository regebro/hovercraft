impress().init();
console().init(cssFile='css/impressConsole.css');

var impressattrs = document.getElementById('impress').attributes
if (impressattrs.hasOwnProperty('auto-console') && impressattrs['auto-console'].value === 'True') {
    consoleWindow = console().open();
}
