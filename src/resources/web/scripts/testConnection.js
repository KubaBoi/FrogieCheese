var socket = new SockJS('/room'); 
var stompClient = Stomp.over(socket);
var sessionId = "";

stompClient.connect({}, function (frame) {
    var url = stompClient.ws._transport.url;
    url = url.replace(
      "ws://localhost:8080/spring-security-mvc-socket/room/",  "");
    url = url.replace("/websocket", "");
    url = url.replace(/^[0-9]+\//, "");
    console.log("Your current session is: " + url);
    sessionId = url;
});

stompClient.subscribe('/user/queue/specific-user' 
  + '-user' + sessionId, function (msgOut) {
     console.log(msgOut);
});
