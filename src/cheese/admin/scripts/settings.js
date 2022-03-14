function getSettings() {
    url = "/admin/getSettings";
    
    return new Promise(resolve => {
        sendGet(url, debug, function(response){
            resolve(response);
        });  
    });
}

async function buildSettingTable() {
    response = await getSettings();
    if (!response.ERROR) {
        for (const key in response) {
            if (response.hasOwnProperty(key)) {
                addSetting(key, response[key]);
            }
        }
    }
}

function addSetting(setting, value) {
    var table = document.querySelector("#settingsTable");

    var row = document.createElement("tr");
    var nameColumn = document.createElement("td");
    var valueColumn = document.createElement("td");

    nameColumn.innerHTML = setting;
    valueColumn.innerHTML = "<input type='text' value='" + value + "'>";
    
    row.appendChild(nameColumn);
    row.appendChild(valueColumn);
    table.appendChild(row);
}