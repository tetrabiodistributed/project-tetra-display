// Placeholder

let socket = new WebSocket("ws://" + location.host + "/ws");

socket.onopen = function (event) {
    console.log("websocket opened");
    socket.send(JSON.stringify({"subscribe": ""}))
};

socket.onmessage = function (event) {
    var ul = document.getElementById("content");
    var li = document.createElement("li");
    li.appendChild(document.createTextNode(event.data));
    ul.appendChild(li);
}

socket.onclose = function (event) {
    if (event.wasClean) {
        console.log("connection closed");
    } else {
        console.log("connection died");
    }
}

socket.onerror = function (event) {
    console.log("error: " + event.message)
}
