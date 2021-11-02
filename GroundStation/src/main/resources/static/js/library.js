class VideoStreamClient {

    constructor(droneId, hostname, port, endpoint) {
        this.droneId = droneId;
        this.webSocket = null;
        this.hostname = hostname;
        this.port = port;
        this.endpoint = endpoint;
    }

    activateStream() {
        this.webSocket = new WebSocket(this.getServerUrl());

        var activeDroneId = this.droneId;

        this.webSocket.onopen = function (event) {
            this.send(activeDroneId);
        }

        this.webSocket.onmessage = function (event) {
            $('#video' + activeDroneId).attr("src", "data:image/jpg;base64," + event.data);
        }
    }

    send(message) {
        if (this.webSocket != null && this.webSocket.readyState == WebSocket.OPEN) {
            this.webSocket.send(message);
        }
    }

    getServerUrl() {
        return "ws://" + this.hostname + ":" + this.port + this.endpoint;
    }

    disconnect() {
        if (this.webSocket != null) {
            this.webSocket.close();
        }
    }
}


class Drone {
    constructor(id, lat, lng) {
        this.id = id;
        this.lat = lat;
        this.lng = lng;
        this.videoSocket = new VideoStreamClient(id, PUBLIC_IP, 80, VIDEO_ENDPOINT);
        this.posMark = new google.maps.Marker({
            position: { lat: lat, lng: lng },
            map: WORLD_MAP, 
            label: id + '',
            icon: 'drone.svg'
        });
        this.locationToPointDataMap = new Map();
        this.labelCounter = 0;
        this.speed = 0.0;
        this.alt = 0.0
    }

    startMission() {
        $.ajax({
            type: 'POST',
            url: '/startMission',
            data: {
                points: this.getPointDataJSON(),
                droneId: this.id
            }
        })
            .done(function (response) {
                console.log(response)
            })
            .fail(function (data) {
                console.log(data)
            });
    }

    sendCommand(commandId) {
        $.ajax({
            type: 'POST',
            url: '/sendCommand',
            data: { commandCode: commandId, droneId: this.id }
        })
            .done(function (response) {
                console.log(response)
            })
            .fail(function (data) {
                console.log(data)
            });
    }

    startVideoFeed() {
        this.videoSocket.disconnect();
        this.videoSocket.activateStream();
    }

    stopVideoFeed() {
        this.videoSocket.disconnect();
    }

    setPosition(lat, lng, alt) {
        this.posMark.setPosition({ lat: lat, lng: lng, alt: alt });
        this.lat = lat;
        this.lng = lng;
        this.alt = alt;
    }

    addPoint(marker) {
        var pointId = Drone.createPointID(marker);
        var pointData = new PointData(marker, DEFAULT_SPEED, DEFAULT_ALTITUDE);
        this.locationToPointDataMap.set(pointId, pointData);
        return pointId;
    }

    static createPointID(marker) {
        return marker.getPosition().lat() + "" + marker.getPosition().lng();
    }

    getPointDataJSON() {
        var result = '[';
        this.locationToPointDataMap.forEach(function (pointData) {
            result += '{"lat":"' + pointData.marker.getPosition().lat() + '",' +
                '"lng":"' + pointData.marker.getPosition().lng() + '",' +
                '"speed":' + pointData.speed + ',' +
                '"height":' + pointData.height + ',' +
                '"action":' + pointData.action + '},';
        });
        return result.substring(0, result.length - 1) + ']';
    }

    getPointDataForID(key) {
        return this.locationToPointDataMap.get(key);
    }

    removePoint(key) {
        this.locationToPointDataMap.get(key).marker.setMap(null);
        this.locationToPointDataMap.delete(key);
    }

    hidePoints() {
        this.locationToPointDataMap.forEach(function (pointData) {
            pointData.marker.setMap(null);
        });
    }

    showPoints() {
        this.locationToPointDataMap.forEach(function (pointData) {
            pointData.marker.setMap(WORLD_MAP);
        });
    }

    removePoints() {
        this.hidePoints();
        this.locationToPointDataMap = new Map();
        this.labelCounter = 0;
    }

    getNextLabelIndex() { 
        return ++this.labelCounter + "";
    }
}


class PointData {
    constructor(marker, speed, height) {
        this.marker = marker;
        this.speed = speed;
        this.height = height;
        this.action = 0;
    }
}


const addMarker = function (location) {
    if (SELECTED_DRONE == null || SELECTED_DRONE == undefined) {
        return;
    }

    var marker = new google.maps.Marker({
        position: location,
        draggable: true,
        label: SELECTED_DRONE.getNextLabelIndex(),
        map: WORLD_MAP
    });

    var pointId = SELECTED_DRONE.addPoint(marker);

    var contentString = renderMapPointDataComponent(pointId, DEFAULT_ALTITUDE, DEFAULT_SPEED);

    var infowindow = new google.maps.InfoWindow({
        content: contentString
    });

    marker.addListener('click', function (event) {
        infowindow.open(WORLD_MAP, marker);
    });

    marker.addListener('dragend', function (event) {
        marker.setPosition(event.latLng);
    });
}



const initializeDronesControls = function (id) {
    $("input[id='mStart" + id + "']").click(function () {
        SELECTED_DRONE.startMission();
    });
    $("input[id*='mCancel" + id + "']").click(function () {
        SELECTED_DRONE.sendCommand(CommandType.CANCEL_MISSION);
        SELECTED_DRONE.removePoints();
    });
    $("input[id*='mRTL" + id + "']").click(function () {
        SELECTED_DRONE.sendCommand(CommandType.RETURN_TO_LAUNCH);
    });
    $("input[id*='fActivate" + id + "']").click(function () {
        SELECTED_DRONE.sendCommand(CommandType.ACTIVATE_FUNCTION);
    });
    $("input[id*='fArm" + id + "']").click(function () {
        SELECTED_DRONE.sendCommand(CommandType.ARM);
    });
    $("input[id*='fDisarm" + id + "']").click(function () {
        SELECTED_DRONE.sendCommand(CommandType.DISARM);
    });
    $("input[id*='fKill" + id + "']").click(function () {
        SELECTED_DRONE.sendCommand(CommandType.KILL);
    });

    $("input[id*='cameraUP" + id + "']").click(function () {
        SELECTED_DRONE.sendCommand(CommandType.CAMERA_UP);
    });

    $("input[id*='cameraDOWN" + id + "']").click(function () {
        SELECTED_DRONE.sendCommand(CommandType.CAMERA_DOWN);
    });

    $("input[id*='btnF" + id + "']").click(function () {
        SELECTED_DRONE.sendCommand(CommandType.FORWARD);
    });

    $("input[id*='btnMvL" + id + "']").click(function () {
        SELECTED_DRONE.sendCommand(CommandType.MLEFT);
    });

    $("input[id*='btnMvR" + id + "']").click(function () {
        SELECTED_DRONE.sendCommand(CommandType.MRIGHT);
    });

    $("input[id*='btnCncl" + id + "']").click(function () {
        SELECTED_DRONE.sendCommand(CommandType.CANCEL_XMOVE);
    });

    $("input[id*='btnB" + id + "']").click(function () {
        SELECTED_DRONE.sendCommand(CommandType.BACKWARD);
    });

    $("input[id*='btnU" + id + "']").click(function () {
        SELECTED_DRONE.sendCommand(CommandType.UP);
    });

    $("input[id*='btnStopZ" + id + "']").click(function () {
        SELECTED_DRONE.sendCommand(CommandType.CANCEL_ZMOVE);
    });

    $("input[id*='btnD" + id + "']").click(function () {
        SELECTED_DRONE.sendCommand(CommandType.DOWN);
    });

    $("input[id*='btnRL" + id + "']").click(function () {
        SELECTED_DRONE.sendCommand(CommandType.RLEFT);
    });

    $("input[id*='btnRR" + id + "']").click(function () {
        SELECTED_DRONE.sendCommand(CommandType.RRIGHT);
    });

    $("input[id*='btnRLEFT45" + id + "']").click(function () {
        SELECTED_DRONE.sendCommand(CommandType.RLEFT45);
    });

    $("input[id*='btnRLEFT90" + id + "']").click(function () {
        SELECTED_DRONE.sendCommand(CommandType.RLEFT90);
    });

    $("input[id*='btnRRIGHT45" + id + "']").click(function () {
        SELECTED_DRONE.sendCommand(CommandType.RRIGHT45);
    });

    $("input[id*='btnRRIGHT90" + id + "']").click(function () {
        SELECTED_DRONE.sendCommand(CommandType.RRIGHT90);
    });
}

const CommandType = {
    START_MISSION: 14,
    CANCEL_MISSION: 6,
    FORWARD: 11,
    MLEFT: 15,
    MRIGHT: 16,
    CANCEL_XMOVE: 12,
    CANCEL_ZMOVE: 13,
    UP: 1,
    RLEFT: 2,
    RRIGHT: 3,
    BACKWARD: 4,
    DOWN: 5,
    RETURN_TO_LAUNCH: 7,
    ACTIVATE_FUNCTION: 8,
    ARM: 9,
    KILL: 17,
    CAMERA_UP: 22,
    CAMERA_DOWN: 23,
    DISARM: 10,
    RLEFT45: 18,
    RLEFT90: 19,
    RRIGHT45: 20,
    RRIGHT90: 21,
}

const executeKeyboardCommand = function (event) {
    switch (event.key) {
        case 'w':
            SELECTED_DRONE.sendCommand(CommandType.FORWARD);
            break;
        case 's':
            SELECTED_DRONE.sendCommand(CommandType.BACKWARD);
            break;
        case 'a':
            SELECTED_DRONE.sendCommand(CommandType.RLEFT);
            break;
        case 'd':
            SELECTED_DRONE.sendCommand(CommandType.RRIGHT);
            break;

        case '4':
            SELECTED_DRONE.sendCommand(CommandType.MLEFT);
            break;
        case '6':
            SELECTED_DRONE.sendCommand(CommandType.MRIGHT);
            break;
        case '8':
            SELECTED_DRONE.sendCommand(CommandType.UP);
            break;
        case '2':
            SELECTED_DRONE.sendCommand(CommandType.DOWN);
            break;
        case '5':
            SELECTED_DRONE.sendCommand(CommandType.CANCEL_XMOVE);
            SELECTED_DRONE.sendCommand(CommandType.CANCEL_ZMOVE);
            break;

        case 'r':
            SELECTED_DRONE.sendCommand(CommandType.CAMERA_UP);
            break;
        case 'f':
            SELECTED_DRONE.sendCommand(CommandType.CAMERA_DOWN);
            break;
    }
}

const removePoint = function (form) {
    SELECTED_DRONE.removePoint(form["key"].value);
}


const updatePointValue = function (form) {
    var pointData = SELECTED_DRONE.getPointDataForID(form["key"].value);
    pointData.speed = form["speed"].value;
    pointData.height = form["height"].value;
    pointData.action = form["action"].value;
}


const copyToClipboard = function (elmId) {
    var copyLink = document.getElementById(elmId);
    copyLink.select();
    copyLink.setSelectionRange(0, 99999);

    document.execCommand("copy");
}