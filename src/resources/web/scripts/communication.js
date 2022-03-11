function sendPost(url, jsonRequest, output, callback) {
    var xhttp = new XMLHttpRequest(); 
    
    var date = new Date();
    if (output) console.log("SENDING", date.getTime(), url, jsonRequest);

    xhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
            json = JSON.parse(this.responseText);
            if(output) console.log("RESPONSE", date.getTime(), url, json);
            if (this.status == 401 && json.ERROR == "Unable to authorize with this token")
                location = "http://" + location.hostname;
            if(callback) callback(json);
        }
    };
    xhttp.open("POST", url);
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhttp.send(jsonRequest);
}