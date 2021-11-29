
// endpoint call
function getChats(fromTime) {
    var url = "/chats/getChats";
    var request = JSON.stringify(
        { 
            "TOKEN": token,
            "FROM_TIME": fromTime
        }
    );
    
    return new Promise(resolve => {
        sendPost(url, request, debug, function(response) { 
            resolve(response);
        });
    });
}

// endpoint call
function getChatsById(ids) {
    var url = "/chats/getChatsById";
    var request = JSON.stringify(
        { 
            "TOKEN": token,
            "CHAT_IDS": ids
        }
    );
    
    return new Promise(resolve => {
        sendPost(url, request, debug, function(response){
            resolve(response);
        });
    });
}

// endpoint call
function addUser(chatId, userId) {
    var url = "/chats/addUser";
    var request = JSON.stringify(
        { 
            "TOKEN": token,
            "CHAT_ID": chatId,
            "USER_ID": userId
        }
    );
    
    return new Promise(resolve => {
        sendPost(url, request, debug, function(response){
            resolve(response);
        });
    });
}


//endpoint call
function createChat(chatUsers) {
    var url = "/chats/createChat";
    var request = JSON.stringify(
        { 
            "TOKEN": token,
            "CHAT_USERS": chatUsers
        }
    );
    
    return new Promise(resolve => {
        sendPost(url, request, debug, function(response){
            resolve(response);
        });
    });
}

//endpoint call
function renameChat(chatId, name) {
    var url = "/chats/renameChat";
    var request = JSON.stringify(
        { 
            "TOKEN": token,
            "CHAT_ID": chatId,
            "NAME": name
        }
    );
    
    return new Promise(resolve => {
        sendPost(url, request, debug, function(response){
            resolve(response);
        });
    });
}