async function loginButton() {
    loginResponse = await login();
    if (loginResponse.ERROR == null) {
        connectedUser = loginResponse.USER;
        token = loginResponse.TOKEN;

        document.querySelector("#loggedAs").innerHTML = connectedUser.USER_NAME; //debug
        chatsArray = await getChats(0);
        if (chatsArray.ERROR == null) { 
            chatsArray = chatsArray.CHATS;
            chatIds = [];
            for (var i = 0; i < chatsArray.length; i++) {
                chatIds.push(chatsArray[i].CHAT_ID);
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