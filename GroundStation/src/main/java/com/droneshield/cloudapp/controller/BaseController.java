package com.droneshield.cloudapp.controller;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.URL;
import com.droneshield.cloudapp.configuration.ConfigReader;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Controller
@RequiredArgsConstructor

public class BaseController {

    private final ConfigReader configurations;

    /** mapping the different url's http requests */
    @GetMapping("/")
    public String indexPage() {
        return "index";
    }
    /** create models - objects representing the different drones which connected, so after
     *  we can acess them in the front end (by entring the server adress + /v/drone id )        */
    @GetMapping("/v/{droneId}")
	public String getVideoFeed(Model model, @PathVariable("droneId") String droneId) {
		
		model.addAttribute("publicIp", getPublicIpAddress());
		model.addAttribute("droneId", droneId);
		model.addAttribute("videoEndpoint", configurations.getVideoWsEndpoint());
        
        return "video";
    }
    /** get the ip adress of server host  */
    private String getPublicIpAddress() {
		String ip = "";
		try {
			final URL whatismyip = new URL("http://checkip.amazonaws.com");

			try(final BufferedReader in = new BufferedReader(new InputStreamReader(whatismyip.openStream()))){
				ip = in.readLine();
			}

		} catch (Exception e) {
			log.error(e.getMessage());
		}
		return ip;
    }
}


