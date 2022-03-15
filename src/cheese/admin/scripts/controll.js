function apiFunction(url) {    
    return new Promise(resolve => {
        sendGet(url, debug, function(response){
            resolve(response);
        });  
    });
}

async function restart() {
    clearInterval(updateInterval);
    apiFunction("/admin/restart");
    setTimeout(buildLogTable, 500);
    setTimeout(prepareRestart, 5000);
    setTimeout(checkLife, 15000);
}

function prepareRestart() {
    document.querySelector("#logTable").innerHTML = "Server is restarting...";
}

async function checkLife() {
    fetch("/alive")
    .then(
        (response) => {
            updateInterval = setInterval(update, 1000);
        },
        (err) => {
            setTimeout(checkLife, 500);
        }
    );
}