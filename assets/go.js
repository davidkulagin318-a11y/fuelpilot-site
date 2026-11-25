// Short tracking links (/fb, /ig, ...): Android phones go to Google Play,
// everything else to the App Store. Both URLs are on the <body> tag.
(function () {
  var b = document.body;
  var url = /android/i.test(navigator.userAgent) ? b.getAttribute('data-play') : b.getAttribute('data-ios');
  if (url) location.replace(url);
})();
