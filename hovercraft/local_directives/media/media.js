//fullscreen

(function () {
  var fullscreenElements = document.getElementsByClassName("media-fullscreen");
  var impressId = document.getElementById("impress");
  Array.prototype.forEach.call(fullscreenElements, function(element) {
    var container = element.closest(".step");
    // center element within container
    container.style.display = 'flex'; container.style.justifyContent = 'center'; container.style.alignItems = 'center';
    scaleContainer(container); // set initial scaling
    // create an observer instance to monitor for changes to recaluculate scaling on impressId style change
    var observer = new MutationObserver(function(mutations) {
      mutations.forEach(function(mutation) {
        scaleContainer(container);
        console.log(mutation.type);
      });    
    });
    // pass impressId node and options to observer
    observer.observe(impressId, {attributes: true}); 
  });
  
  function scaleContainer(container) {
    // get impress's scaling factor and divide it by 100 to get a de-scaling factor
    var impressDescale = Math.round(100/parseFloat(/scale\((\d+(?:\.\d+)?)\)/.exec(impressId.style.transform)[1])*100)/100 || 100;
    container.style.height = impressDescale + 'vh';
    container.style.width = impressDescale + 'vw';
  }
  
})();

// autoplay
// based on work by matejmosko https://github.com/impress/impress.js/issues/100

(function () {
  // Video
  var videos = document.getElementsByTagName("video");
  Array.prototype.forEach.call(videos, function(video) {
    if (video.hasAttribute("data-media-autoplay")) {
      var videoStep = video.closest(".step");
      videoStep.addEventListener("impress:stepenter", function() {setTimeout(function() {video.play();}, 500);}, false);
      videoStep.addEventListener("impress:stepleave", function() {video.pause();}, false);
    };
  });
  
  // Audio
  var audios = document.getElementsByTagName("audio");
  Array.prototype.forEach.call(audios, function(audio) {
    if (audio.hasAttribute("data-media-autoplay")) {
      var audioStep = audio.closest(".step");
      audioStep.addEventListener("impress:stepenter", function() {setTimeout(function() {audio.play();}, 500);}, false);
      audioStep.addEventListener("impress:stepleave", function() {audio.pause();}, false);
    };
  });
})();
