// adds row in chatTable
function addSearchedUser(user) {

    var row = document.createElement("tr");
    var cellImg = document.createElement("td");
    var cellName = document.createElement("td");
    
    cellImg.innerHTML = "<img class='chatPic' src='/pictures/" + user.PICTURE_ID + ".png'>";
    cellName.innerHTML = user.USER_NAME;

    row.appendChild(cellImg);
    row.appendChild(cellName);
    row.setAttribute("onclick", "createChatButton(" + user.ID + ")");
    
    searchedUsersTable.appendChild(row);
}

function showSearchedUsers(users) {
    deleteWholeTable(searchedUsersTable);

    for (const user of users) {
        addSearchedUser(user);
    }
}

function addSearchedUser2(user) {

    var row = document.createElement("tr");
    var cellImg = document.createElement("td");
    var cellName = document.createElement("td");
    
    cellImg.innerHTML = "<img class='chatPic' src='/pictures/" + user.PICTURE_ID + ".png'>";
    cellName.innerHTML = user.USER_NAME;

    row.appendChild(cellImg);
    row.appendChild(cellName);
    row.setAttribute("onclick", "addUserButton(" + user.ID + ")");
    
    searchedUsersTable2.appendChild(row);
}

function showSearchedUsers2(users) {
    deleteWholeTable(searchedUsersTable2);

    for (const user of users) {
        addSearchedUser2(user);
    }
}