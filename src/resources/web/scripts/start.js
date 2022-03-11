autoLogin();
async function autoLogin() {
    console.log
    if (getCookie("username") != "") 
        document.querySelector("#fname").value = getCookie("username");
    if (getCookie("password") != "") 
        document.querySelector("#fpass").value = getCookie("password");

    if (getCookie("token") != "") {
        response = await authorizeToken();
        if (response.ERROR == null) {
            token = getCookie("token");
            if (getCookie("user") != "") {
                connectedUser = getCookie("user");
            }
            else {
                response = await getUserByToken();
                if (response.ERROR == null) {
                    connectedUser = response.USER;
                    setCookie("user", response.USER, 5);
                }
            }
            logged();

            setCookie("token", getCookie("token"), 5);
            setCookie("user", connectedUser, 5);
        }
    }
}

async function loginButton() {
    loginResponse = await login();
    if (loginResponse.ERROR == null) {
        setCookie("username", document.getElementById("fname").value, 5);
        setCookie("password", document.getElementById("fpass").value, 5);
        setCookie("token", loginResponse.TOKEN, 5);
        setCookie("user", loginResponse.USER, 5);

        connectedUser = loginResponse.USER;
        token = loginResponse.TOKEN;

        logged();
    }
}

async function logged() {
    settName.innerHTML = connectedUser.USER_NAME;
    settPic.setAttribute("src", "/pictures/" + connectedUser.PICTURE_ID + ".png")

    document.querySelector("#loggedAs").innerHTML = connectedUser.USER_NAME; //debug
    document.querySelector("#loggedAsImg").setAttribute("src", "/pictures/" + connectedUser.PICTURE_ID + ".png")
    
    chatsArray = await getChats(0);
    if (chatsArray.ERROR == null) { 
        chatsArray = chatsArray.CHATS;
        chatIds = [];
        for (var i = 0; i < chatsArray.length; i++) {
            chatIds.push(chatsArray[i].ID);
        }

        var chatMessages = await getChatMessages(0, chatIds);
        if (chatMessages.ERROR == null) {
            for (var ci = 0; ci < chatMessages.CHATS.length; ci++) {
                var chat = chatMessages.CHATS[ci];
                var chatInArray = chatsArray[findChatIndexById(chat.CHAT_ID)];

                chatInArray.MESSAGES = chat;
            }

            showChat(chatIds[0]);
            loadChats();
            window.setInterval(updateChats, 1000);
            window.setInterval(searchUsers, 1000);
        }
    }
} 

function enterInput() {
    var key = window.event.keyCode;

    if (key === 13) { //&& !window.event.shiftKey) {
        sendMess();
        return false;
    }
    else {
        return true;
    }

}

function userSettingsButton() {
    document.getElementById("userSettingsScreen").style.animation = "userSettingsDown 0.5s forwards";
}

function userSettingsButtonBack() {
    document.getElementById("userSettingsScreen").style.animation = "userSettingsUp 0.5s forwards";
}

function registerButton() {
    document.getElementById("loginScreen").style.animation = "registerLogin 1s forwards";
    document.getElementById("registerScreen").style.animation = "registerRegisterScreen 1s forwards";
}

async function register() {
    var name = document.querySelector("#rname");
    var nB = true;
    var mail = document.querySelector("#rmail");
    var mB = true;
    var pass1 = document.querySelector("#rpass1");
    var p1B = true;
    var pass2 = document.querySelector("#rpass2");
    var pass = true;

    if (name.value == "") {
        nB = false;
        name.setAttribute("class", "badInput");
    }
    else {
        name.setAttribute("class", "input");
    }
    if (mail.value == "") {
        mB = false;
        mail.setAttribute("class", "badInput");
    }
    else {
        mail.setAttribute("class", "input");
    }
    if (pass1.value == "") {
        p1B = false;
        pass1.setAttribute("class", "badInput");
    }
    else {
        pass1.setAttribute("class", "input");
    }
    if (pass1.value != pass2.value && p1B) {
        pass = false;
        pass1.setAttribute("class", "badInput");
        pass2.setAttribute("class", "badInput");
    }
    else {
        pass1.setAttribute("class", "input");
        pass2.setAttribute("class", "input");
    }

    if (nB && mB && pass) {
        var user = await createUser(name.value, pass1.value, mail.value);
        if (user.ERROR == null) {
            document.getElementById("loginScreen").style.animation = "registeredLogin 1s forwards";
            document.getElementById("registerScreen").style.animation = "registeredRegisterScreen 1s forwards";    
        }
    }
}

function uploadPicture() {
    let xhr = new XMLHttpRequest();

    let picture = document.getElementById("file").files[0];
    let formData = new FormData();
    
    formData.append("userId", connectedUser.ID)
    formData.append("picture", picture);

    xhr.onreadystatechange = state => { 
        console.log(xhr.response); 
        connectedUser.PICTURE_ID = JSON.parse(xhr.response).PICTURE_ID;
        settPic.setAttribute("src", "/pictures/" + connectedUser.PICTURE_ID + ".png")
    } // err handling
    xhr.timeout = 5000;
    xhr.open("POST", "/users/uploadProfilePicture"); 
    xhr.send(formData);

}