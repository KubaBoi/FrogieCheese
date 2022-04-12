function getRelease() {
    url = "/admin/cheeseRelease";
    
    return new Promise(resolve => {
        sendGet(url, debug, function(response){
            resolve(response);
        });  
    });
}

async function setRelease() {
    var lbl = document.getElementById("release");

    var response = await getRelease();
    if (!response.ERROR) {
        lbl.innerHTML = "Cheese Framework (v" + response.RELEASE + ")"
    }
}