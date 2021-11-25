
// endpoint call
function login() {
    var url = "/authentication/login";
    var request = JSON.stringify(
        { 
            "USER_NAME": document.getElementById("fname").value,
            "PASSWORD": document.getElementById("fpass").value
        }
    );

    return new Promise(resolve => {
        sendPost(url, request, debug, function(response) {
            resolve(response);
        });
    });
}