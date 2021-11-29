// user properties
var token;
var connectedUser;

//document variables
var openChat = -1;
var chatsTable = document.querySelector("#chatsTable");
var chatTable = document.querySelector("#chatTable"); 
var messageBox = document.querySelector("#messageBox");
var sendButton = document.querySelector("#messageSend");
var createChatInp = document.querySelector("#createChatInp");
var searchedUsersTable = document.querySelector("#searchedUsersTable");
var chatTableDiv = document.querySelector("#chatTableDiv");

var openChatName = document.querySelector("#openChatName");
var openChatImg = document.querySelector("#openChatImg");
var chatUsersTable = document.querySelector("#chatUsersTable");
var addUserInp = document.querySelector("#addUserInp");
var searchedUsersTable2 = document.querySelector("#searchedUsersTable2");
var renameChatInp = document.querySelector("#renameChatInp");

var settName = document.querySelector("#settName");
var settPic = document.querySelector("#settPic");

var debug = false;

// other
var chatsArray = 
[
    {
        "CHAT_ID": 0, 
        "CHAT_NAME": "Frank", 
        "CHAT_USERS": [0, 1],
        "LAST_ACTIVITY": 1,
        "MESSAGES": {
            "MESSAGES": [
                {
                    "MESSAGE_ID": 1,
                    "CONTENT": "zduř",
                    "CHAT_ID": 0,
                    "AUTHOR_ID": 0,
                    "TIME_STAMP": 1
                },
                {
                    "MESSAGE_ID": 0,
                    "CONTENT": "ahoj kamo",
                    "CHAT_ID": 0,
                    "AUTHOR_ID": 1,
                    "TIME_STAMP": 0
                }
            ],
            "LAST_DELIVERED_MESSAGE_ID": 1,
            "LAST_SEEN_MESSAGE_ID": 0
        }
    }
];