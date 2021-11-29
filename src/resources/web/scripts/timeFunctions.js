// is called every 1 second
async function updateChats() {
    var changes = await update();
    if (changes.ERROR == null && changes.CHANGES.length > 0) {
        var updatedChats = await getChatsById(changes.CHANGES);
        if (updatedChats.ERROR == null) {
            for (var i = 0; i < updatedChats.length; i++) {
                var isIn = false;
                var updatedChat = updatedChats[i];
                for (var j = 0; j < chatsArray.length; i++) {
                    var chat = chatsArray[j];
                    if (updatedChat.CHAT_ID == chat.CHAT_ID) {
                        isIn = true;
                    }
                }

                if (!isIn) {
                    chatsArray.push(updatedChat);
                }
            }

            var messages = await getChatMessages(0, changes.CHANGES); 
            if (messages.ERROR == null) {
                for (var i = 0; i < messages.CHATS.length; i++) {

                    var chatMessages = messages.CHATS[i];
                    var chat = chatsArray[findChatIndexById(chatMessages.CHAT_ID)];
                    console.log(chatMessages);
                    if (chat.MESSAGES == null) {
                        chat.MESSAGES = chatMessages;
                    }
                    else {
                        for (var m = 0; m < chatMessages.MESSAGES.length; m++) {
                            var mC = chatMessages.MESSAGES[m];
                            if (mC.ID > chat.MESSAGES.LAST_DELIVERED_MESSAGE_ID) {
                                chat.MESSAGES.MESSAGES.push(mC);
                            }
                        }
                        chat.MESSAGES.LAST_DELIVERED_MESSAGE_ID = chatMessages.LAST_DELIVERED_MESSAGE_ID;
                        chat.MESSAGES.LAST_SEEN_MESSAGE_ID = chatMessages.LAST_SEEN_MESSAGE_ID;
                        chat.LAST_ACTIVITY = chat.MESSAGES.MESSAGES[chat.MESSAGES.MESSAGES.length-1].TIME_STAMP;
                        sortMessages(chat);
                    }
                }
                updateChatsTable();
                showChat(openChat);
            }
        }
    }
}

// is called every 1 second
var oldInput = "";
var oldInput2 = "";
async function searchUsers() {
    if (createChatInp.value != "" && oldInput != createChatInp.value) {
        var users = await getUserDynamic(createChatInp.value);
        if (users.ERROR == null) {
            showSearchedUsers(users.USERS);
        }
        oldInput = createChatInp.value;
    }
    else if (createChatInp.value == "") {
        oldInput = "";
        deleteWholeTable(searchedUsersTable);
    }

    if (addUserInp.value != "" && oldInput2 != addUserInp.value) {
        var users = await getUserDynamic(addUserInp.value);
        if (users.ERROR == null) {
            showSearchedUsers2(users.USERS);
        }
        oldInput2 = addUserInp.value;
    }
    else if (addUserInp.value == "") {
        oldInput = "";
        deleteWholeTable(searchedUsersTable2);
    }
}