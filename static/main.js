let socket = new WebSocket("ws://" + location.host + "/ws");

socket.onopen = function (event) {
    console.log("websocket opened");
    socket.send(JSON.stringify({"subscribe": ""}))
};

socket.onmessage = function (event) {
    console.log(JSON.parse(event.data));
    classes_and_descriptors = {"Inspiratory Pressure": "dP",
                               "PEEP": "PEEP",
                               "PIP": "PIP",
                               "Tidal Volume": "Tv"};
    data = JSON.parse(event.data);
    for (i = 0; i < 4; ++i) {
        for (const [key, value] of Object.entries(data["patient-" + i])) {
            dataElement = getElementByXpath("//div[@class='_dataCell patient-" + i + " " + classes_and_descriptors[key] + "']");
            dataElement.innerHTML = value.toFixed(2);
        }
    }
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

function getElementByXpath(path) {
    return document.evaluate(path,
                             document,
                             null,
                             XPathResult.FIRST_ORDERED_NODE_TYPE,
                             null).singleNodeValue;
}
