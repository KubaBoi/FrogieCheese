// adds row in chatTable
function addSearchedUser(user) {

    var row = document.createElement("tr");
    var cellImg = document.createElement("td");
    var cellName = document.createElement("td");
    
    cellImg.innerHTML = "<img class='chatPic' src='/pictures/" + user.PICTURE_ID + ".jpg'>";
    cellName.innerHTML = user.USER_NAME;

    row.appendChild(cellImg);
    row.appendChild(cellName);
    row.setAttribute("onclick", "createChatButton(" + user.USER_ID + ")");
    
    searchedUsersTable.appendChild(row);
}

function showSearchedUsers(users) {
    deleteWholeTable(searchedUsersTable);

    for (const user of users) {
        addSearchedUser(user);
    }
}
