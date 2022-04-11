function apiFunction(url) {    
    return new Promise(resolve => {
        sendGet(url, debug, function(response){
            resolve(response);
        });  
    });
}

function restart() {
    if (confirm("Do you really want to restart your application?\nIt will took about 20 seconds.")) {
        clearInterval(updateInterval);
        document.getElementById("restartButt").disabled = true;
        apiFunction("/admin/restart");
        textInterval = setInterval(function() { loadingText("Waiting for response from server"); }, 200);
        setTimeout(buildTableWithDelay, 500);
    }
}

async function buildTableWithDelay() {
    response = await getActiveLog();
    if (!response.ERROR) {
        if (response.RESPONSE.LOG.includes("<label class='warning'>Restart will start in 5 seconds</label></td></tr>\n")) {
            clearInterval(textInterval);

            element = document.getElementById("log");
            var b = element.scrollHeight - element.clientHeight;
            element.scrollTop = b;
            
            prepareRestart();
            setTimeout(checkLife, 15000);
        }
        else {
            setTimeout(buildTableWithDelay, 500);
        }
    }
}

function prepareRestart() {
    textInterval = setInterval(function() { loadingText("Server is restarting"); }, 200);
}
var dots = 0;
function loadingText(text) {
    for (let i = 0; i < dots; i++) {
        text += ".";
    }
    dots += 1;
    if (dots >= 10) dots = 0;
    document.querySelector("#logTable").innerHTML = text;
}

async function checkLife() {
    fetch("/alive")
    .then(
        (response) => {
            updateInterval = setInterval(update, 1000);
            clearInterval(textInterval);
            document.getElementById("restartButt").disabled = false;
            alert("Server has been restarted :)");
        },
        (err) => {
            setTimeout(checkLife, 500);
        }
    );
}

async function pullChanges() {
    var response = await apiFunction("/admin/update");
    if (response.ERROR) {
        alert(response.ERROR);
    }
}