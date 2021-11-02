package com.droneshield.cloudapp.configuration;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import lombok.Getter;
import lombok.Setter;
/** for baseController which map the different urls */
@Getter
@Setter
@Component

public class ConfigReader {

    @Value("${app.drone.video-ws-endpoint}")
	private String videoWsEndpoint;

    @Value("${app.drone.video-server-port}")
	private int videoServerPort;

    @Value("${app.drone.drone-id-length}")
	private int droneIdLength;
    
}