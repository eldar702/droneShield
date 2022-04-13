import time
from dronekit import connect, VehicleMode, LocationGlobalRelative, Command, LocationGlobal
from pymavlink import mavutil
import cv2
import Laser
import DroneFunc
import Detecting
##################################################################################
#######################          droneShield            ##########################
##################################################################################
######   Initialize     ########
# -- Setup the commanded flying speed
gnd_speed = 1  # [m/s]
arm_height = 5
mode = 'GROUND'
vehicle = connect('udp:127.0.0.1:14551') # Connect to the vehicle
print('Connecting...')
# vehicle = connect('tcp:127.0.0.1:5762', wait_ready=True)
DroneFunc.dummy_yaw_initializer()
Laser.first_laser_use() # init some stuff for laser use
laser_is_on_flag = False
laser_max_time = 5
detect = Detecting.Detect()

def main():
    global mode, vehicle, gnd_speed, laser_is_on_flag, arm_height
    start_laser_flag = 0
    # Var's declaration:
    area_is_clear = False
    drone_x, drone_y, drone_z = 0, 0, 0
    centered_flag = 0
    ####  MAIN LOOP  #####
    while True:

        # if suspected area is clear - return to HOME
        if area_is_clear is True:
            # -- We go back home
            DroneFunc.changeMode("RTL")
            mode = "BACK"

        ### Mode for: looking for missions while drone on the ground
        if mode == 'GROUND':
            # --- Wait until a valid mission has been uploaded
            numOf_WPs, missionList = DroneFunc.get_current_mission(vehicle)
            time.sleep(2)
            if numOf_WPs > 0:
                print("A valid mission has been uploaded: takeoff!")
                mode = 'TAKEOFF'

        ### Mode for: take off
        elif mode == 'TAKEOFF':

            # -- Add the Home waypoint for backing to home when finish the mission
            DroneFunc.add_last_waypoint_to_mission(vehicle.location.global_relative_frame.lat,
                                         vehicle.location.global_relative_frame.lon, vehicle.location.global_relative_frame.alt)
            print("Home waypoint added to the mission")
            time.sleep(1)

            # -- Takeoff
            DroneFunc.arm_and_takeoff(arm_height)

            # -- Change the UAV mode to AUTO
            print("Changing to AUTO")
            DroneFunc.changeMode("AUTO")

            # -- Change mode, set the ground speed
            vehicle.groundspeed = gnd_speed
            mode = 'REACHED TO LOCATION'
            print("Switch mode to REACHED TO LOCATION")

        elif mode == 'REACHED TO LOCATION':
            # -- vehicle.commands.cout is the total number of waypoints
            # -- vehicle.commands.next is the waypoint the vehicle is going to
            print("Current WP: %d of %d " % (vehicle.commands.next, vehicle.commands.count))
            if vehicle.commands.next == vehicle.commands.count:
                print("drone reached the desirable location: time to start search for balloons")
                # -- First we clear the flight mission
                DroneFunc.clear_mission(vehicle)
                DroneFunc.changeMode("GUIDED")
                mode = 'SEARCHING'

        #### need to add: mode for searching the balloons
        elif mode == "SEARCHING" and area_is_clear is False:
            cap = cv2.VideoCapture(0)
            cap.set(3, detect.Height)
            cap.set(4, detect.Weight)
            # cap.set(10,70)

            while True:
                success, img = cap.read()
                detected_boxes = detect.getBoxes(img)
                objects = detect.tracker.update(detected_boxes)
                detected_flag = len(detected_boxes)

               # if balloon is detected - move drone so balloon will be in the middle of the frame (directly in front how the drone)
                if detected_flag:
                    drone_x, drone_y, drone_z = DroneFunc.values_for_balloon_centered(detected_boxes[0],
                    detect.frame_center_x, detect.frame_center_y, detect.desire_area)
                    DroneFunc.send_local_ned_velocity(drone_x, drone_y, drone_z)

                    centered_flag = (drone_x == 0 and  drone_y == 0 and drone_z == 0)
                    if centered_flag and laser_is_on_flag is False:
                        start_laser_flag = time.time()
                        Laser.turn_laser_on()
                        laser_is_on_flag = True

                if (time.time() > start_laser_flag + laser_max_time) and laser_is_on_flag:
                    Laser.turn_laser_off()
                    laser_is_on_flag = False

                elif detected_flag is False:
                    area_is_clear = DroneFunc.scanning()
                # loop over the tracked objects and write details on screen (rectangle and id). IF there is a problem with the writing excange this line with the function's lines
                Detecting.write_details_on_screen(img, objects)

                cv2.imshow("Output", img) #TODO: only for testing, after testing dont forget to delete (and the lines cv2.putText and cv2.circle too)
                cv2.waitKey(1)


        elif mode == "BACK":
            # If drone back home - still steady ant wait for the next mission.
            if vehicle.location.global_relative_frame.alt < 1:
                mode = 'GROUND'
                print("Switch to GROUND mode, waiting for new missions")

        time.sleep(0.5)


if __name__ == '__main__':
    main()
