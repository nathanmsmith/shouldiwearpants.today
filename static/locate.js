$(document).ready(function() {
    $.geolocation.get({
        win: determineWhetherPantsShouldBeWornFromLocation,
        error: showError
    });

    $('input[type=text]').keyup(function(e) {
        if (e.keyCode == 13) {
          determineWhetherPantsShouldBeWornFromUserInput($(this).val());
        }
    });

    $('#why').click(function() {
      areDetailsDown = !areDetailsDown;
      $("#details").slideToggle();
    });

    $('#locate').click(function() {
        $.geolocation.get({
            win: determineWhetherPantsShouldBeWornFromLocation,
            error: showError
        });
    });
});

areDetailsDown = false;

function displayLoading() {
  if (areDetailsDown) {
    $("#details").slideUp();
  }
  $('#answer').hide();
  $('#loading').show();
  $('#why').hide();
  $('#subtext').show();
  clearInput()
}

function displayResults(data) {
  $('#loading').hide();
  $('#answer').show();
	$('#answer').text(data.answer);
  $('#subtext').hide();
  $('#why').show();
  $('#details').html(data.details);
  if (areDetailsDown) {
    $("#details").slideDown();
  }
  clearInput()
}

function displayError() {
  if (areDetailsDown) {
    $("#details").slideUp();
  }
  $('#answer').hide();
  $('#loading').hide();
  $('#why').hide();
  $('#subtext').hide();
  clearInput()
}

function clearInput() {
  $('input[type=text]').val("");
  $('input[type=text]').blur();
}

function determineWhetherPantsShouldBeWornFromUserInput(input) {
  displayLoading();
		$.getJSON($SCRIPT_ROOT + '/pant_results_user', {
				input: input
		}, displayResults);
}

function determineWhetherPantsShouldBeWornFromLocation(position) {
  displayLoading();
    $.getJSON($SCRIPT_ROOT + '/pant_results_location', {
        longitude: position.coords.longitude,
        latitude: position.coords.latitude
    }, displayResults);
}

function showError(error) {

    var string = "";

    switch (error.code) {
        case error.PERMISSION_DENIED:
            string = "We need to know where you are to check the weather! Please enter your location below.";
            break;
        case error.POSITION_UNAVAILABLE:
            string = "Well this is awkward... Something went wrong! Please try again.";
            break;
        case error.TIMEOUT:
            string = "Well this is awkward... Something went wrong! Please try again.";
            break;
        case error.UNKNOWN_ERROR:
            string = "Well this is awkward... Something went wrong!Please try again.";
            break;
    }

    displayError();
    alert(string);
}
