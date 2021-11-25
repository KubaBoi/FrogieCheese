// finds index of chat in local chatsArray
function findChatIndexById(chatId) {
    for (let i = 0; i < chatsArray.length; i++) {
        if (chatsArray[i].CHAT_ID == chatId) {
            return i;
        }
    }
    return null;
}

 //endpoint call
function getChatMessages(fromTime, chatIds) {
    var url = "/messages/getChatMessages";
    var request = JSON.stringify(
        { 
            "TOKEN": token,
            "FROM_TIME": fromTime,
            "CHATS": chatIds
        }
    );
    
    return new Promise(resolve => {
        sendPost(url, request, debug, function(response){
            resolve(response);
        });
    });
}

//endpoint call
function sendMessage(chatId, message) {
    var url = "/messages/sendMessage";
    var request = JSON.stringify(
        { 
            "TOKEN": token,
            "CHAT_ID": chatId,
            "CONTENT": message
        }
    );

    return new Promise(resolve => {
        sendPost(url, request, debug, function(response) {
            resolve(response);
        });
    });
}

//endpoint call
function seenMessage(messageId) {
    var url = "/messages/seenMessage";
    var request = JSON.stringify(
        { 
            "TOKEN": token,
            "MESSAGE_ID": messageId
        }
    );
    
    return new Promise(resolve => {
        sendPost(url, request, debug, function(response) {
            resolve(response);
        });
    });
}