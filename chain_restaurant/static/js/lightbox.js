$('#galleryCarousel').carousel({
    interval: false
  });
  var lightbox = false;
  $( "#gallery-thumbnails" ).on( "click", "a", function( event ) {
    event.preventDefault();
    if (lightbox === false) {
      lightbox = true;
      var slideNumber = $(this).attr("data-slide-number");
      $('#galleryCarousel').carousel(Number(slideNumber)); 
      $("#lightbox").show();
    }
  });
  $("#close").click(function() {
    if (lightbox === true) {
      lightbox = false;
      $("#lightbox").hide();
    }
  });