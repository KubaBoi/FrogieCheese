
// onclick event shows chat by chatId in chatDiv

// recreate table of chats 
function setSeenMessage(chat) {
    chat.LAST_ACTIVITY = chat.MESSAGES.MESSAGES[0].TIME_STAMP;
    chat.MESSAGES.LAST_DELIVERED_MESSAGE_ID = chat.MESSAGES.MESSAGES[0].ID;
    chat.MESSAGES.LAST_SEEN_MESSAGE_ID = chat.MESSAGES.MESSAGES[0].ID;
    updateChatsTable();
}

function findAuthor(array, authorId) {
    for (var i = 0; i < array.length; i++) {
        if (array[i].ID == authorId) {
            return array[i];
        }
    }
    return null;
}

function sortMessages(chat) {
    for (var i = 0; i < chat.MESSAGES.MESSAGES.length - 1; i++) {
        for (var j = 0; j < chat.MESSAGES.MESSAGES.length - i - 1; j++) {
            if (chat.MESSAGES.MESSAGES[j].TIME_STAMP < chat.MESSAGES.MESSAGES[j + 1].TIME_STAMP) {
                var tmp = chat.MESSAGES.MESSAGES[j];
                chat.MESSAGES.MESSAGES[j] = chat.MESSAGES.MESSAGES[j + 1];
                chat.MESSAGES.MESSAGES[j + 1] = tmp;
            }
        }
    }
}

// adds row in chatTable
function addMessage(author, message) {
    cellClass = "myMessage";

    var row = document.createElement("tr");
    var cellUser = document.createElement("td");
    var cellContent = document.createElement("td");
    var div = document.createElement("div");

    if (author.ID != connectedUser.ID) {        
        cellClass = "otherMessage";

        cellUser.innerHTML = "<img class='chatPic' src='/pictures/" + author.PICTURE_ID + ".png' title='" + author.USER_NAME + "'>";
        cellUser.setAttribute("class", "userInMessage");

    }

    div.innerHTML = message.CONTENT;
    div.setAttribute("class", cellClass);

    cellContent.appendChild(div);
    row.setAttribute("id", "message" + message.ID);
    row.appendChild(cellUser);
    row.appendChild(cellContent);
    
    chatTable.appendChild(row);
}

function doChatInfo(chat) {
    deleteWholeTable(chatUsersTable);

    openChatName.innerHTML = chat.CHAT_NAME;
    openChatImg.setAttribute("src", "/pictures/" + chat.PICTURE_ID + ".png");

    for (var i = 0; i < chat.CHAT_USERS.length; i++) {
        var user = chat.CHAT_USERS[i];
        var row = document.createElement("tr");
        var cellImg = document.createElement("td");
        var cellUser = document.createElement("td");

        cellImg.innerHTML = "<img class='chatPic' src='/pictures/" + user.PICTURE_ID + ".png'>";
        cellUser.innerHTML = user.USER_NAME;

        row.appendChild(cellImg);
        row.appendChild(cellUser);

        chatUsersTable.appendChild(row);
    }
}

// builds chat in chatDiv
async function showChat(chatId) {
    if (chatsArray.length > 0 && chatId != null) {
        deleteWholeTable(chatTable);

        localChatArray = findChatIndexById(chatId);

        chat = chatsArray[localChatArray];
        doChatInfo(chat);
        if (chat.MESSAGES != null) {
            openChat = chatId;
            
            sortMessages(chat);

            for (var i = chat.MESSAGES.MESSAGES.length - 1; i >= 0; i--) {
                message = chat.MESSAGES.MESSAGES[i];
                author = findAuthor(chat.CHAT_USERS, message.AUTHOR_ID);
                addMessage(author, message);
            }
            
            //chats table update
            seenMess = await seenMessage(chat.MESSAGES.MESSAGES[0].ID);
            if (seenMess.ERROR == null) {
                setSeenMessage(chat);
            }
        }
    }
}

//send button
async function sendMess() {
    message = await sendMessage(openChat, messageBox.value);
    if (message.ERROR == null) {
        message = message.MESSAGE;
        addMessage(connectedUser, message);
        chat = chatsArray[findChatIndexById(message.CHAT_ID)];
        if (chat.MESSAGES == null) {
            chat.MESSAGES = {};
        }
        if (chat.MESSAGES.MESSAGES == null) {
            chat.MESSAGES.MESSAGES = [];
        }

        chat.MESSAGES.MESSAGES.push(message);
        sortMessages(chat);
        messageBox.value = "";

        updateChatsTable();
        showChat(chat.ID);
        chatTableDiv.scrollTo(0, chatTableDiv.scrollHeight);
    }
}
