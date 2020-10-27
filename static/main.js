let socket = new WebSocket("ws://" + location.host + "/ws");

socket.onopen = function (event) {
    console.log("websocket opened");
    socket.send(JSON.stringify({"subscribe": ""}))
};

socket.onmessage = function (event) {
    let data = JSON.parse(event.data)
    console.log(data);
    drawDataToPage(data)
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

function drawDataToPage(data) {
    classes_and_descriptors = {"Inspiratory Pressure": "dP",
                               "PEEP": "PEEP",
                               "PIP": "PIP",
                               "Tidal Volume": "Tv",
                               "Flow Rate": "flowRate"};
    for (i = 0; i < 4; ++i) {
        for (const [key, value] of Object.entries(data["patient-" + i])) {
            var descriptorMagnitude = Number(value).toFixed(2);
            dataElement = getElementByXpath("//div[@class='_dataCell patient-" + i + " " + classes_and_descriptors[key] + "']");
            if (dataElement != null) {
                dataElement.innerHTML = descriptorMagnitude;
            }
        }
    }
}

function getElementByXpath(path) {
    return document.evaluate(path,
                             document,
                             null,
                             XPathResult.FIRST_ORDERED_NODE_TYPE,
                             null).singleNodeValue;
}
