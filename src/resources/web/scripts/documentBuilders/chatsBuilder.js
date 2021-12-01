function deleteWholeTable(table) {
    table.innerHTML = "";
}

function sortChats() {
    for (var i = 0; i < chatsArray.length - 1; i++) {
        for (var j = 0; j < chatsArray.length - i - 1; j++) {
            if (chatsArray[j].LAST_ACTIVITY < chatsArray[j + 1].LAST_ACTIVITY) {
                var tmp = chatsArray[j];
                chatsArray[j] = chatsArray[j + 1];
                chatsArray[j + 1] = tmp;
            }
        }
    }
}

// adds row in chatsTable which represents chat
function addChat(chat) {
    chatClass = "seenChat";

    var cellUserImg = document.createElement("td");
    var cellContent = document.createElement("td");
    var content = "";

    if (chat.MESSAGES.MESSAGES.length > 0) {
        //marks if chat is seen
        if (chat.MESSAGES.LAST_SEEN_MESSAGE_ID != chat.MESSAGES.MESSAGES[0].ID) {
            chatClass = "unseenChat";
        }

        content = chat.MESSAGES.MESSAGES[0].CONTENT;

        if (content.length > 27) {
            content = content.substring(0, 27) + "...";
        }
    }

    for (var i = 0; i < chat.CHAT_USERS.length; i++) {
        var user = chat.CHAT_USERS[i];
        if (user.ID != connectedUser.ID && chat.CHAT_USERS.length <= 2) {
            cellContent.innerHTML = "<b>" + chat.CHAT_NAME + "</b> ";
            cellUserImg.innerHTML = "<img class='chatPic' src='/pictures/" + user.PICTURE_ID + ".png'>";
        }
        else if (user.ID != connectedUser.ID) {
            cellContent.innerHTML = "<b>" + chat.CHAT_NAME + "</b> ";
            cellUserImg.innerHTML = "<img class='chatPic' src='/pictures/" + chat.PICTURE_ID + ".png'>";
        }
    }
    cellUserImg.setAttribute("class", "userInMessage");
    cellContent.innerHTML += "<br>" + content;
    cellContent.setAttribute("class", chatClass);

    var row = document.createElement("tr");
    row.setAttribute("onclick", "showChat(" + chat.ID + ")");
    row.appendChild(cellUserImg);
    row.appendChild(cellContent);
    
    chatsTable.appendChild(row);
}

// rewrites whole chatsTable
function updateChatsTable() {
    deleteWholeTable(chatsTable);
    sortChats();

    for (var i = 0; i < chatsArray.length; i++) {
        addChat(chatsArray[i]);
    }
}

// after login
function loadChats() {
    updateChatsTable();

    document.getElementById("loginScreen").style.animation = "animLogin 1.5s forwards";
    document.getElementById("mainScreen").style.animation = "animMainScreen 1.5s forwards";
}