//endpoint call
function update() {
    var url = "/users/update";
    var request = JSON.stringify(
        { 
            "TOKEN": token
        }
    );
    
    return new Promise(resolve => {
        sendPost(url, request, debug, function(response){
            resolve(response);
        });
    });
}

//endpoint call
function getUser(userId) {
    var url = "/users/getUser";
    var request = JSON.stringify(
        { 
            "TOKEN": token,
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
function createUser(userName, password, email) {
    var url = "/users/createUser";
    var request = JSON.stringify(
        { 
            "USER_NAME": userName,
            "PASSWORD": password,
            "EMAIL": email 
        }
    );
    
    return new Promise(resolve => {
        sendPost(url, request, debug, function(response){
            resolve(response);
        });  
    });
}

// endpoint call
function getUserByName(name) {
    var url = "/users/getUserByName";
    var request = JSON.stringify(
        { 
            "TOKEN": token,
            "USER_NAME": name
        }
    );
    
    return new Promise(resolve => {
        sendPost(url, request, debug, function(response){
            resolve(response);
        });  
    });
}

//endpoint call
function getUserDynamic(userNameStart) {
    var url = "/users/getUserDynamic";
    var request = JSON.stringify(
        { 
            "TOKEN": token,
            "USER_NAME_START": userNameStart
        }
    );
    
    return new Promise(resolve => {
        sendPost(url, request, debug, function(response){
            resolve(response);
        });  
    });
}

//endpoint call
function setUserPicture(userId, picture) {
    var url = "/users/setUserPicture";
    var request = JSON.stringify(
        { 
            "TOKEN": token,
            "USER_ID": userId,
            "PICTURE": picture
        }
    );
    
    return new Promise(resolve => {
        sendPost(url, request, debug, function(response){
            resolve(response);
        });  
    });
}