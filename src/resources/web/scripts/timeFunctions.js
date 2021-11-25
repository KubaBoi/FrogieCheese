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
                    if (chat.MESSAGES == null) {
                        chat.MESSAGES = chatMessages;
                    }
                    else {
                        for (var m = 0; m < chatMessages.MESSAGES.length; m++) {
                            var mC = chatMessages.MESSAGES[m];
                            if (mC.MESSAGE_ID > chat.MESSAGES.LAST_DELIVERED_MESSAGE_ID) {
                                chat.MESSAGES.MESSAGES.push(mC);
                            }
                        }
                        chat.MESSAGES.LAST_DELIVERED_MESSAGE_ID = chatMessages.LAST_DELIVERED_MESSAGE_ID;
                        chat.MESSAGES.LAST_SEEN_MESSAGE_ID = chatMessages.LAST_SEEN_MESSAGE_ID;
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
}