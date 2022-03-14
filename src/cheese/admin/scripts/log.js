debug = true;

function getActiveLog() {
    url = "/admin/getActiveLog";
    
    return new Promise(resolve => {
        sendGet(url, debug, function(response){
            resolve(response);
        });  
    });
}

async function buildLogTable() {
    response = await getActiveLog();
    if (!response.ERROR) {
        var table = document.querySelector("#logTable");
        table.innerHTML = "";
        table.innerHTML = response.RESPONSE.LOG;

        var label = document.querySelector("#logDesc");
        if (label.tagName == "LABEL") {
            label.innerHTML = "<button onclick=\"location='/admin/logs'\">All logs</button>	&nbsp;" +
            "<button onclick=\"location='/admin/activeLog.html'\">Full log</button>";
        }
        else {
            label.innerHTML = "Cheese log - " + response.RESPONSE.LOG_DESC + " - ACTIVE";
        }
    }
}

if (typeof dontRunScript == "undefined") setInterval(update, 1000);
var oldC = 1;
var oldScrollHeight = 0;
function update() {
    buildLogTable();
    element = document.getElementById("log");
    var a = element.scrollTop;
    var b = element.scrollHeight - element.clientHeight;
    if (oldC < 500 && oldScrollHeight < element.scrollHeight) {
        element.scrollTop = b;
    }

    oldScrollHeight = element.scrollHeight;
    oldC = b - a;
}