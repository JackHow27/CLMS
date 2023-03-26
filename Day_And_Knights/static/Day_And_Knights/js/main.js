$(document).ready(function() {
    // Add banner to homepage
    if ($('body').hasClass('homepage')) {
      var bannerHtml = '<div class="banner">' +
                       '<h2>Welcome to our website!</h2>' +
                       '<p>We offer the best chess league management system around.</p>' +
                       '</div>';
      $('body').prepend(bannerHtml);
    }
  });
  