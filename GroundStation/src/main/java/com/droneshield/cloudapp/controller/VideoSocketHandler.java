package com.droneshield.cloudapp.controller;

import java.io.IOException;

import com.droneshield.cloudapp.service.VideoStreamManager;

import org.springframework.stereotype.Component;
import org.springframework.web.socket.CloseStatus;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.AbstractWebSocketHandler;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Component
@RequiredArgsConstructor
public class VideoSocketHandler extends AbstractWebSocketHandler {
    
    private final VideoStreamManager videoStreamManager;
	
	@Override
	public void afterConnectionEstablished(WebSocketSession session) throws Exception {
		log.debug("WebSocket Connection OPEN. Session {} IP {}", session.getId(), session.getRemoteAddress());
	}
    
    @Override
	public void afterConnectionClosed(WebSocketSession session, CloseStatus closeStatus) throws Exception {
        log.debug("WebSocket Connection CLOSED. Session {} IP {} {}", 
                       session.getId(), session.getRemoteAddress(), closeStatus);
	}
	
    @Override
    protected void handleTextMessage(WebSocketSession session, TextMessage droneId) throws IOException {
    	videoStreamManager.setVideoWebSocketSessionForDroneId(session, droneId.getPayload());
    } 
}
