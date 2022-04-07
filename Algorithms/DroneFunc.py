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
def get_current_mission(vehicle, send_cmds=False):
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


##Send a velocity command with +x being the heading of the drone.

# Function: velocity
# Describe: change the velocity with respect to the position of the drone
def send_global_ned_velocity(vx, vy, vz):
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,  # time_boot_ms (not used)
        0, 0,  # target system, target component
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,  # frame
        0b0000111111000111,  # type_mask (only speeds enabled)
        0, 0, 0,  # x, y, z positions (not used)
        vx, vy, vz,  # x, y, z velocity in m/s
        0, 0, 0,  # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)  # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)
    vehicle.send_mavlink(msg)
    vehicle.flush()


def change_yaw(degrees, relative):
    if relative:
        is_relative = 1  # yaw relative to direction of travel
    else:
        is_relative = 0  # yaw is an absolute angle

    # create the CONDITION_YAW command using command_long_encode()
    msg = vehicle.message_factory.command_long_encode(
        0, 0,  # target system, target component
        mavutil.mavlink.MAV_CMD_CONDITION_YAW,  # command
        0,  # confirmation
        degrees,  # Param 1, yaw in degrees
        0,  # Param 2, yaw speed deg/s
        1,  # Param 3, Direction -1 ccw, 1 cw
        is_relative,  # Param 4, relative offset 1, absolute angle 0
        0, 0, 0)  # Param 5-7 not used
    vehicle.send_mavlink(msg)
    vehicle.flush()


def dummy_yaw_initializer():
    lat = vehicle.location.global_relative_frame.lat
    lon = vehicle.location.global_relative_frame.lon
    alt = vehicle.location.global_relative_frame.alt

    aLocation = LocationGlobalRelative(lat, lon, alt)

    msg = vehicle.message_factory.set_position_target_global_int_encode(
        0,
        0, 0,
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
        0b0000111111111000,
        aLocation.lat * 1e7,
        aLocation.lon * 1e7,
        aLocation.alt,
        0,
        0,
        0,
        0, 0, 0,
        0, 0)
    vehicle.send_mavlink(msg)
    vehicle.flush()


def distance_to_size( desire_distance):
    if desire_distance <= 1:
        area = 22500
    elif desire_distance <= 2:
        area = 5500
    elif desire_distance <= 3:
        area = 3000
    elif desire_distance <= 4:
        area = 1600
    elif desire_distance <= 5:
        area = 1000
    else:
        area = 700
    return area


def values_for_balloon_centered(detected_boxes, frame_center_x, frame_center_y, desire_area):
    (X, Y, W, H) = detected_boxes
    drone_x, drone_y, drone_z = 0, 0, 0
    balloon_center_x = X + (W / 2)
    balloon_center_y = Y + (H / 2)
    balloon_area = W * H
    diff_x = frame_center_x - balloon_center_x
    diff_y = frame_center_y - balloon_center_y
    if balloon_area < desire_area:
        if diff_x < -30:  # todo: in diferent Thread - make closer func
            drone_y = -30
        if diff_x > 30:
            drone_y = 30
        if diff_y < -15:
            drone_y = -30
        if diff_y > 15:
            drone_y = 30
        if balloon_area < desire_area:
            drone_x = 30

        return drone_x, drone_y, drone_z

