
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


//endpoint call
function createChat(chatUsers) {
    var url = "/chats/createChat";
    console.log(chatUsers);
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