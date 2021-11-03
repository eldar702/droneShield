
/** The stream manager: saves the drones id with currespondeing session and 
 *  receive incoming udp data packets manage the video between drones and web */
package com.droneshield.cloudapp.service;
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import com.droneshield.cloudapp.configuration.ConfigReader;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession; 
import lombok.extern.slf4j.Slf4j;
  
  @Slf4j
  @Component
  public class VideoStreamManager implements Runnable {
      private static final int UDP_MAX_SIZE = 65507;
      private final int ID_LENGTH;
      private final Map<String, Set<WebSocketSession>> droneIdToWebSocketSession;   /** map for mapping drone id to open sessions  */
      private final DatagramSocket videoReceiverDatagramSocket;
      private final ExecutorService serverRunner; /** threadpool for manage the threads */
       
      /** constructor */
      public VideoStreamManager(ConfigReader configuration) {
          try {
              videoReceiverDatagramSocket = new DatagramSocket(configuration.getVideoServerPort());
          } catch (IOException e) {
              log.error(e.getMessage(), e);
              throw new RuntimeException(e);
          }
  
          serverRunner = Executors.newSingleThreadExecutor();
          droneIdToWebSocketSession = new ConcurrentHashMap<>();
          
          ID_LENGTH = configuration.getDroneIdLength();
  
          activate();
      }
      /** active the videoStreamManager task and put it in the thread pool */
      public void activate() {
          serverRunner.execute(this);
          log.info("Video Stream Manager is Active");
      }
  
      public void run() {
          while(!videoReceiverDatagramSocket.isClosed()){
              try {
                  byte[] buf = new byte[UDP_MAX_SIZE];
                  DatagramPacket packet = new DatagramPacket(buf, buf.length);
                  videoReceiverDatagramSocket.receive(packet);
                  String droneId = new String( packet.getData(), 0, ID_LENGTH);
                  String data = new String(packet.getData(), ID_LENGTH, packet.getLength());
                  Set<WebSocketSession> droneIdWebSessions = droneIdToWebSocketSession.get(droneId);
                  if (droneIdWebSessions == null || droneIdWebSessions.isEmpty()) {
                      continue;
                  }
                  Iterator<WebSocketSession> it = droneIdWebSessions.iterator();
                  while(it.hasNext()) {
                      WebSocketSession session = it.next();
                      if (!session.isOpen()) {
                          it.remove();
                          continue;
                      }
                      session.sendMessage(new TextMessage(data));
                  }
              } catch(Exception e) {
                  log.error(e.getMessage());
              }}}

      /** function which get the drone id, check if there is open session or not.
       *  if yes, open it in different thread for other session
       *  if no - open the first one */
      public void setVideoWebSocketSessionForDroneId(WebSocketSession session, String droneId) {
          Set<WebSocketSession> droneIdSessions = droneIdToWebSocketSession.putIfAbsent(droneId, new HashSet<>());
          /** check if there is already open session for that drone */
          if(droneIdSessions == null) {
              droneIdSessions = droneIdToWebSocketSession.get(droneId);
          } 
          droneIdSessions.add(session);
          log.debug("Drone ID {} has {} active Web Socket Sessions", droneId, droneIdSessions.size());
      }
  
      public boolean isServerClosed() {
          return videoReceiverDatagramSocket.isClosed();
      }
  
      public void shutdown() {
          if (!videoReceiverDatagramSocket.isClosed()) {
              try {
                  videoReceiverDatagramSocket.close();
              } catch (Exception e) {
                  log.error(e.getMessage());
              }
          }
          serverRunner.shutdown();
      }
  }
