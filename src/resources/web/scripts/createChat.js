async function createChatButton(wantedUserId) {
    var chat = await createChat([connectedUser.ID, wantedUserId]);
    if (chat.ERROR == null) {
        chat = chat.CHAT;
        var messages = await getChatMessages(0, [chat.ID]);
        if (messages.ERROR == null) {
            chat.MESSAGES = messages.CHATS[0];
            chatsArray.push(chat);
            openChat = chat.ID;
            updateChatsTable();
            showChat(openChat);
            createChatInp.value = "";
        }
    }
}

async function addUserButton(userId) {
    var chat = await addUser(openChat, userId);
    if (chat.ERROR == null) {
        chat = chat.CHAT;
        var messages = await getChatMessages(0, [chat.ID]);
        if (messages.ERROR == null) {
            chat.MESSAGES = messages.CHATS[0];
            chatsArray[findChatIndexById(chat.ID)] = chat;
            updateChatsTable();
            showChat(openChat);
            addUserInp.value = "";
        }
    }
}

async function renameChatButton() {
    var name = renameChatInp.value;
    console.log(name);
    var response = await renameChat(openChat, name);
    if (response.ERROR == null) {
        chat = chatsArray[findChatIndexById(response.CHAT_ID)];
        chat.CHAT_NAME = name;
        updateChatsTable();
        showChat(openChat);
    }
}