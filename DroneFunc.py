import time
from dronekit import connect, VehicleMode, LocationGlobalRelative, Command, LocationGlobal
from pymavlink import mavutil
import Laser


####################             FUNCTIONS :               #############################

#################             Modes :               ##########################
# Function: Clear the mission


from droneShield import vehicle


# Function: arm and takeoff
# Describe: As it sounds
def arm_and_takeoff(altitude):
    while not vehicle.is_armable:
        print("waiting to be armable")
        time.sleep(1)

    print("Arming motors")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed: time.sleep(1)

    print("Taking Off")
    vehicle.simple_takeoff(altitude)

    # check if the drone reached to the desairble altitude
    while True:
        v_alt = vehicle.location.global_relative_frame.alt
        print(">> Altitude = %.1f m" % v_alt)
        if v_alt >= altitude - 1.0:
            print("Target altitude reached")
            break
        time.sleep(1)

# Function: Clear the mission
# Describe: Because we want the drone modified the given mission so he can operate autonomously,
#           we need to clear the user mission, and upload the antonymous mission.
def clear_mission(vehicle):

    cmds = vehicle.commands
    vehicle.commands.clear()
    vehicle.flush()

    # After clearing the mission you MUST re-download the mission from the vehicle
    cmds = vehicle.commands
    cmds.download()
    cmds.wait_ready()


# Function: download the  mission
# Describe: download the user mission, in our case ot will be the user waypoints,
def download_mission(vehicle):
    cmds = vehicle.commands
    cmds.download()
    cmds.wait_ready()  # wait until download is complete.


# Function: get the current mission
# Describe: Downloads the mission and returns the wp list and number of WP,
def get_current_mission(vehicle, send_cmds = False):

    "Downloading mission"
    download_mission(vehicle)
    missionList = []
    n_WP = 0
    cmds = vehicle.commands
    for wp in vehicle.commands:
        missionList.append(wp)
        n_WP += 1
    if send_cmds:
        return cmds, n_WP, missionList
    return n_WP, missionList


# Function: create "Home" point
# Describe: add as last point the staring point. for backing home after finish the mission.
def add_last_waypoint_to_mission(vehicle, Latitude, longitude, altitude):
    # Var Init:
    numberOfWPs = 0
    missionList = []
    cmds, numberOfWPs, missionList = get_current_mission(vehicle, True)
    # create the last WP
    last_WP = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                           0, 0, 0, 0, 0, 0, Latitude, longitude, altitude)
    missionList.append(last_WP)  ## add the last WP

    cmds.clear()

    # Write the modified mission and flush to the vehicle
    for command in missionList:
        cmds.add(command)
    cmds.upload()

    return cmds.count

# Function: Change mode
# Describe: change the REAL drone's mode (Guided, Auto, LTR etc)
def ChangeMode(vehicle, mode):
    while vehicle.mode != VehicleMode(mode):
        vehicle.mode = VehicleMode(mode)
        time.sleep(0.5)
    return True
