class VideoStreamClient {
    /** Constructor */
    constructor(droneId, hostname, port, endpoint) {
        this.droneId = droneId;
        this.webSocket = null;
        this.hostname = hostname;
        this.port = port;
        this.endpoint = endpoint;
    }
    /** Function to open websocket - used in video.html */
    activateStream() {
        this.webSocket = new WebSocket(this.getServerUrl());
        var activeDroneId = this.droneId;

        /* hendler function for when socket is open (when connected
           to the backend) - send the drone id which open        */
        this.webSocket.onopen = function (event) {
            this.send(activeDroneId);}

        /* hendler function for sending data from and to drone and ground station*/
        this.webSocket.onmessage = function (event) {
            $('#video' + activeDroneId).attr("src", "data:image/jpg;base64," + event.data);
        } }

    send(message) {
        if (this.webSocket != null && this.webSocket.readyState == WebSocket.OPEN) {
            this.webSocket.send(message); } }

    getServerUrl() {
        return "ws://" + this.hostname + ":" + this.port + this.endpoint;
    }
    /* close the websocket*/
    disconnect() {
        if (this.webSocket != null) {
            this.webSocket.close();
        }
    }
}

