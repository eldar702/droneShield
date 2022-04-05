import time
from dronekit import connect, VehicleMode, LocationGlobalRelative, Command, LocationGlobal
from pymavlink import mavutil
import Laser
import DroneFunc

##################################################################################
#######################          droneShield            ##########################
##################################################################################
######   Initialize     ########
# -- Setup the commanded flying speed
gnd_speed = 10  # [m/s]
arm_height = 5
mode = 'GROUND'
vehicle = connect('udp:127.0.0.1:14551') # Connect to the vehicle
print('Connecting...')
# vehicle = connect('tcp:127.0.0.1:5762', wait_ready=True)
DroneFunc.dummy_yaw_initializer()
Laser.first_laser_use() # init some stuff for laser use
laser_is_turn = False
def main():
    global mode, vehicle, gnd_speed, laser_is_turn, arm_height
    # Var's declaration:
    area_is_clear = False
    Laser.first_laser_use()
    ####  MAIN LOOP  #####
    while True:

        # if suspected area is clear - return to HOME
        if area_is_clear is True:
            # -- We go back home
            DroneFunc.ChangeMode(vehicle, "RTL")
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
            DroneFunc.add_last_waypoint_to_mission(vehicle, vehicle.location.global_relative_frame.lat,
                                         vehicle.location.global_relative_frame.lon, vehicle.location.global_relative_frame.alt)
            print("Home waypoint added to the mission")
            time.sleep(1)

            # -- Takeoff
            DroneFunc.arm_and_takeoff(arm_height)

            # -- Change the UAV mode to AUTO
            print("Changing to AUTO")
            DroneFunc.ChangeMode(vehicle, "AUTO")

            # -- Change mode, set the ground speed
            vehicle.groundspeed = gnd_speed
            mode = 'REACHING TO LOCATION'
            print("Switch mode to REACHING TO LOCATION")

        elif mode == 'REACHING TO LOCATION':
            # -- vehicle.commands.cout is the total number of waypoints
            # -- vehicle.commands.next is the waypoint the vehicle is going to
            print("Current WP: %d of %d " % (vehicle.commands.next, vehicle.commands.count))
            if vehicle.commands.next == vehicle.commands.count:
                print("drone reached the desirable location: time to start search for balloons")
                # -- First we clear the flight mission
                DroneFunc.clear_mission(vehicle)
                DroneFunc.ChangeMode(vehicle, "GUIDED")
                mode = 'SEARCHING'

        # #### need to add: mode for searching the balloons
        # elif mode == "SEARCHING":
        #
        # # mode for target in the exact position, so the laser will pointed the detected balloon
        # elif mode == "targeting":
        #
        # # mode for turning on and off the laser
        # elif mode == "lasering":
        #     Laser.turn_laser_on_off(laser_is_turn)
        #     # TODO: create function that keeping the laser on until the balloon
        #     #       popped, and after TURNOFF the laser AND BACK TO SEARCHING
        # ###  Mode for: backing to home
        # elif mode == "BACK":
        #     # If drone back home - still steady ant wait for the next mission.
        #     if vehicle.location.global_relative_frame.alt < 1:
        #         mode = 'GROUND'
        #         print("Switch to GROUND mode, waiting for new missions")

        time.sleep(0.5)


if __name__ == '__main__':
    main()
