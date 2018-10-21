var urllogin = "https://www.recreation.gov/api/accounts/login"

var request = new XMLHttpRequest();

request.open('GET', 'http://api.amp.active.com/camping/campgrounds/?pstate=IL&api_key=8qmqjffpscjuwgqmmgcz3v84', true);

request.onload = function () {

  
  console.log(this.response);

  console.log("AAAAAAAAAAAAAAAAAAAAAAAAAAA")

  console.log(JSON.parse(this.response))

  $.post( "/postmethod", {
            javascript_data: JSON.parse(this.response)
    });

}

request.send();



