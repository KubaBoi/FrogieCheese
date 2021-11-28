async function createChatButton(wantedUserId) {
    var chat = await createChat([connectedUser.ID, wantedUserId]);
    if (chat.ERROR == null) {
        messageBox.value = "Nikdy nikomu neposílej svoje přihlašovací údaje. V případě komunikace s podporou se na tvoje heslo žabičky nikdy ptát nebudou.";
        chatsArray.push(chat);
        console.log(chat);
        openChat = chat.ID;
        sendMess();
        createChatInp.value = "";
    }

}