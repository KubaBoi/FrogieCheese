function run() {
  var aR = getCookie("logArCookie");
  var aS = getCookie("logAsCookie");

  if (aS == "true") window.scrollTo(0,document.body.scrollHeight);

  document.getElementById("aR").checked = (aR == "false") ? false : true;
  document.getElementById("aS").checked = (aS == "false") ? false : true;
  setInterval(reload, 5000);
}

function reload() {
  setCookie("logArCookie", document.querySelector("#aR").checked, 10);
  setCookie("logAsCookie", document.querySelector("#aS").checked, 10);

  if(document.querySelector("#aR").checked) {
    location.reload();
  }
}


function setCookie(cname, cvalue, exdays) {
    const d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    let expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(";");
    for(let i = 0; i <ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == " ") {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
}