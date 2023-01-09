![droneShield](https://user-images.githubusercontent.com/72104254/168979002-b660370d-bc6e-4410-b8e4-0f8d48daffaf.gif)


**Droneshield is a fully autonomous laser drone that works remotely, using its laser to eliminate incendiary balloons. The droneShield is a quadcopter that I built and designed entirely on my own.**

## 1.  [General](#General)
   - [Background](#background)
   - [droneShield](#droneshield)
   - [Prolog](#Prolog)
   - [Architecture](#Architecture)
## 2. [Hardware](#Hardware)
   - [Motors](#Motors)
   - [Propellers](#Propellers)
   - [Battery](#Battery)
   - [Frame](#Frame)
   - [Flight_Control](#Flight_Control)
   - [Companion_computer](#Companion_computer)
   - [ESC](#ESC)
   - [RC_and_Telemetry](#RC_and_Telemetry)
   - [GPS_and_Optical_Flow](#GPS_and_Optical_Flow)
   - [Laser](#Laser)
## 3. [GroundStation](#GroundStation)
   - [QgroundControl](#QgroundControl)
   - [Mission_Planner](#Mission_Planner)
   - [Overall](#Overall)
## 4. [Algorithms](#Algorithms)
   - [state_machines](#state_machines)
        - [Waiting](#Waiting)
        - [Takeoff](#Takeoff)
        - [Reached](#Reached)
        - [Searching](#Searching)
        - [Detecting](#Detecting)
        - [Back](#Back)
## 5. [Media](#Media)
   - [Building_Photos](https://github.com/eldar702/droneShield/tree/main/Video/Building_Photos)
   - [Bloopers](https://github.com/eldar702/droneShield/tree/main/Video/Bloopers)
   - [FINAL_VIDEO](https://www.youtube.com/watch?v=eI0JDhAvPLg&t=2s)
## 6. [Dependencies](#Dependencies) 



# General
<img src="https://user-images.githubusercontent.com/72104254/171228942-f92f020f-45a0-41a7-beea-6eb9b94bdb23.png" width="1050" height="400">

## Background
It's no secret that Israel has a problem that causes thousands of dunams of Israeli territory to be burned every year - that problem is the problem of incendiary balloons. For the most part, terrorist organizations, including Hamas in particular, are using helium balloons to inflate explosive devices from the West Bank to the State of Israel in general and the surrounding settlements in particular. There is enormous economic and safety damage caused by these fires: hundreds of thousands of acres are burned every year, and the safety of hundreds of thousands of residents is at stake. As a result of this situation, balloons scare children instead of arousing the opposite response. There are a number of solutions available: Laser systems can be used to blow up incendiary balloons with a very high probability, but they are quite expensive, and thus dominate only a few areas of the envelope. It is also possible to use drones as a military solution, but piloting a drone requires prior knowledge and specialized training. There is also the issue that not everyone is technologically oriented. Therefore, this solution is marketed as a business-to-business solution, as was the previous one. As such, it should be noted once more that this is a complicated solution that could only provide a partial resolution - and that using soldiers to fly the drone is a historical practice that dates back thousands of years. It is worth noting that there are other solutions, but these are merely the "same thing disguised as another". So what if a student of computer science is unable to develop a solution that addresses all three shortcomings that other solutions are incapable of addressing? It's time to say hello to droneShield.

# droneShield
<img src="https://user-images.githubusercontent.com/72104254/171169294-3d556cac-ccf1-4b30-9806-515de5c29d10.jpeg" width="700" height="400">

## Prolog
Professors Ariel Roth and Asi Barak asked me to come up with a problem and find a solution. It's up to me which problem I want to solve, and in what way I want to solve it. Now that you've seen the problem, here is the solution: Droneshield is a fully autonomous laser drone that operates from a ground control and uses its laser to eliminate incendiary balloons. Quadcopter droneShield is one of my own designs and builds. The droneShield is powered by the ground station. Image processing is used by droneShield to identify balloons and state machine architecture is used for autonomous operation. A droneShield is activated by clicking the button on the groundstation, and flies to an area marked on the map, scans for incendiary balloons, and destroys them if they are detected through the laser. When all that is not enough, he returns to the starting point and awaits further instructions after the scan.

## Architecture
<img src="https://user-images.githubusercontent.com/72104254/171357482-aff573f5-616d-4413-b7fb-471a80f1cfed.png" width="1000" height="400">


# Hardware
<img src="https://user-images.githubusercontent.com/72104254/171169896-b5397ded-3721-4c29-bd08-aa990861935f.jpg" width="450" height="400">

As a starting point, I would like to present you with a copy of all the components and considerations that I have chosen for the drone.

#### **Motors**:
Perhaps one of the most important parts of a drone. There is a direct connection and tradeoff between speed and torque. The faster the motor, the less torque it produces.
Motors  of drones are commercially registered as follows: 2016 1000k, i.e:

4 digit numbers when the 2 first digits are the width of the rotor in mm.
So this motor has 20 mm wide rotor.
The last two digits are the height of the rotor in mm, so this motor has a 6 mm tall rotor.

And the KV rating tells you how fast the shaft will spin per volt with no load:
Higer kv means the motor will spin faster while lover kv means you have more torque.

<img src="https://user-images.githubusercontent.com/72104254/171284605-c0e2c5af-dbcb-4514-8434-e41f59196c8d.png" width="220" height="280">

#### **Propellers**
Selection propeller should be done with motor and battery selection in mind. Different prop specs can produce drastically different current draws and torque.
Specs of the props will be provided in 4 digits of numbers, for example, 1245.
The first 2 numbers are for the diameter of the prop in inches. So a 1245 prop is 12 inches long. 
The last two numbers are for the pitch of the prop. Imagine a screw turning into wood. The more aggressive the pitch the farther the screw will turn into the wood in one turn.
Going back to drones (yay!), 45 (of the 1245 propellor) indicates the prop would turn 4.5 inches in one complete turn if it were able to turn into a solid medium.
The higher the pitch, the more torque you will generate.
There is a tradeoff between current draw (which here will be the main influencer to torque)
And the size of the propellor.
So you can think that if you want more torque (head up – droneShield is really heavy drone – Weight 1.6kg!) so you need to choose as much as big propellor as you can get. This assumption is obviously wrong. First of all – you are limited by the size of the frame you have chosed. Furthermore and maybe more important – bigger props produce more heat. For example: you cant use 810kv motors with 1445 props and 3s battery, but you can use it with 1245 props.

<img src="https://user-images.githubusercontent.com/72104254/171285874-c80aadec-dc2d-40a3-b471-0cb6c2c8604d.jpg" width="220" height="240">

#### **Battery**
In drones we make use of lipo batteries. This choice is simple – They have very high specific energy, they very cheap and they weight less than other options.
When choosing a battery, you need to take in to account few things:
Capacity: is the measure of the amount of electric charge, that is stored within the battery. We measured it with the unit mAh, which stand for milli amp per hour.
C-rating: gives us knowledge of the maximum current draw that the battery can safely endure.
Units of C are inverse hours (1/hour)
Example with 50C battery and 4000mah:
4000mAh = 4Ah
So the maximum current this battery can draw is  (4Ah)(50C) = 200A.
So in other words, this battery can safely have 200 amps continuously drawn from it.
The s': the number of lipo cells the battery contains. This is measured by digis and 's after, for example 3's is a lipo battery contains 3 lipo cells.
	Every cell produce voltage. Fully charge cell produce 3.7v, so for example 4s cells battery can produce (4)(3.7) = 14.8v
	The higher the volts the bigger the power the drone will have, BUT – bigger valts mean more hot the drone will produce. For example for 810kv motors with 1245 props you can use 3s battery but you can't use it with 4's battery – it will lead to overheat.
	Safe tip: the lipo batteries are flammable, so always store them in cold place inside a special case (there is cases for that all over amazon/aliexpress)

<img src="https://user-images.githubusercontent.com/72104254/171285926-49537f80-ad33-4b7d-b8da-f94bb4b60b00.png" width="300" height="150">

#### **Frame**:
Various types of drone frames exist, each with a different size, shape, and material. Most of the guides you can find on the internet recommend using 450F plastic frames when building "custom big" drones, according to most of the guides. This is not the best choice in my opinion. 
I think there are two main reasons why:
Size - there isn't enough space on the frame of the drone, so you're forced to use this space in a smart way and that makes designing the drone a little more difficult. Choosing a 500F frame would be a good option in my opinion.
Durability: Plastic is too fragile. Especially if this is your first time building a drone (which it was for me), you're going to crash a lot. It is just a bad idea to choose a frame that is too breakable. The use of a carbon frame is highly recommended. As a matter of fact, it is worth the extra dollars and extra weight from my experience. You can see some crashes I've had with droneShield in the following video.
[loopers folder](#Looper)

<img src="https://user-images.githubusercontent.com/72104254/171409323-a1220e5f-d6be-4cc0-8800-63a152584de0.png" width="260" height="260">


#### **Flight Control (FC)**
Is the control center of the drone. Meaning is the central hub that all the electronics component connect to.
I'm use here Pixhawk, and I REALY recommend using it.

<img src="https://user-images.githubusercontent.com/72104254/171284081-247d2717-dc65-42d0-aaf6-30c6e3f06753.png" width="280" height="380">

#### **Companion computer**
the fc is like small computer but not really – it control all the component but it doesn’t have computing power. So how can you use artificial intelligent like image processing with your drone? Simply – connect a companion computer (very small and thin computer) to your drone. droneShield makes use of raspberry pi 4b for the image processing and algorithms use. 

<img src="https://user-images.githubusercontent.com/72104254/171284188-73b98d57-129b-453b-88d8-2d1a947fd74f.png" width="400" height="270">

#### **ESC**
Stands for electronic speed controllers. And as the name hints, it in charge of digests the PWM sent from the FC and produces an ESC output that will drive the motors.
It connects to the motor from one side and the other connects to the electric supply (in most cases to PDB – power distribution board and not to the battery directly).
ESC's specs will tell you what types of lipos you can use with them (2-4s 30a means you can use it with a battery of max 30a and 4 lipo cells)

<img src="https://user-images.githubusercontent.com/72104254/171285848-b316d780-f357-4673-8989-ec520b151817.png" width="310" height="160">

#### **RC_and_Telemetry**:	
both of them are used to communicate data wirelessly with the drone. While Telemetry communication is bi directional, rc communication is unidirectional. 
Telemetry is used for communicate with ground station. In our case – droneShield communicate with QGroundControl

   <img src="https://user-images.githubusercontent.com/72104254/171285896-dc0f9d33-5a12-43b4-b4f6-3c4d3d25a09c.png" width="200" height="240">
   
#### **GPS_and_Optical_Flow**
For autonomous drone mission. We need a way for the drone to determine its position in 3D space:
1.	GPS
2.	Optical flow


#### **GPS**
Used in conjunction with a magnetometer. The gps make the drone know his location. So for travel to another location, simply travel from know current position to target waypoint. 
There is 2 main pros for GPS that make my recommendation for the component for  
		orientation in space.
1.	Self adjusts its errors (example: if a gust of wind blows the drone off course, a new reading will simply show where the new location of the drone is on 3D space).
2.	Cheap
BUT, GPS must be outside to access satellites, so for inside use – its preffer to use optical flow.

<img src="https://user-images.githubusercontent.com/72104254/171285855-c39c5fa1-074b-40e2-a3d1-511424a63ea7.png" width="190" height="250">

#### **Laser**
There is no doubt that working with lasers is a very dangerous undertaking, and therefore it is important to wear the appropriate protective equipment when working with them. There is no mistaking this for a joke. In addition, I recommend that you avoid working with lasers. Lasers are the hardest and most dangerous solution available to this problem.
My passion for mechanical and electrical engineering was not sparked while I was studying computer science. I believe the design and build of the drone "closed the corner" on the machines for me, but it wasn't enough to close the electrical gap between the two machines.
As a result, I decided to add a laser to the design.

## GroundStation:
<img src="https://user-images.githubusercontent.com/72104254/171227222-9c5f6923-e0f5-46cf-8156-c09caf74724d.jpg" width="1050" height="450">

The drone must be able to communicate with the operator via some form of "channel". The droneShield can communicate via remote control, and it is certainly capable of being operated via remote control. However, there is an obvious problem with this communication channel - the operator must have a working knowledge of glider flight and, as noted, this method violates one of the three main principles by which I create and make decisions. As we stated, you should be able to operate the drone autonomously without any prior experience. In addition, there are 2 open source programs which have a very strong community and provide an insane amount of functionality.

### QgroundControl
A ground control station (GCS) for UAVs, QGroundControl (QGC), is a powerful and intuitive ground control station. A primary objective of QGC is to make it easy for users to use, whether they are first-time users or professionals. With it, you are able to control and plan flights for any drone equipped with MAVLink, as well as configure vehicles using both PX4 and ArduPilot technology. 
In the User Manual you will find instructions for using QGroundControl, though you may not need them since the user interface is very intuitive. https://github.com/mavlink/qgroundcontrol


### Mission_Planner
ArduPilot's Mission Planner ground station application offers a full range of features for working with autopilots. On this page, you will find information about Mission Planner's background and how it is organized. There are three types of ground control stations: plane, helicopter, and rover. There is only a Windows version available. As a configuration tool or as a dynamic control supplement to your autonomous vehicle, Mission Planner can be used in a number of ways. The following are just a few of the things you can do with Mission Planner: 
Link to documentation: https://ardupilot.org/planner/

### Overall 
There is no doubt that both are highly recommended. I prefer the first, which is also attached to the installation file of the QgroundControl folder. If necessary, I would recommend consulting the documentation for QgroundControl or mission planner.

## Algorithms:
<img src="https://user-images.githubusercontent.com/72104254/171230368-f63b18c1-05cb-4cd8-b1d1-bff4802220d8.png" width="1000" height="450">
In order for droneShield to be as autonomous as possible, I used state machine architecture. So I defined a situation state, where each one includes a target task and a "transition function". A combination of these is called state.
The different states:

### **Waiting**
•	**Description**: Initial state when the drone is turned on. As droneShield waits for the user to click the suspected area, it is waiting for the user to click it.

•	**Transitions func**: The takeoff state.

•	**Goal**: start the party (not really, droneShield isn't a party animal, but he is loyal; he is waiting for user commands to begin).

### **Takeoff** 
•	**Description**: Taking off is the first step in executing a given mission.

•	**Transitions** func: reached the destination state.

•	**Goal**: Attained the desired meters height.


###	**Reached**
•	**Description**: Drones can be flown to any location you choose. A "desired location" is an area the user clicks on the map to suggest is the suspected area.

•	**Transitions func**: Searching state.

•	**Goal**: reached the given point.


###	**Searching**

•	**Description**: Trying to find incendiary balloons.

•	**Transitions func**: Detecting the current state and the previous state.

•	**Goal**: Locate a balloon.


###	**Detecting**

•	**Description**: When droneShield finds the balloon in the Searching state, it turns on the laser and makes sure that it has exploded.

•	**Transitions func**: Searching and returning to the previous state.

•	**Goal**: to blow up all balloons that had popped.

###	**Back**

•	**Description**: Returning to the point where the drone took off.

•	**Transitions func**: Entering "takeoff" state.

•	**Goal**: Arrived at the "home" point and landed there to prepare for the next mission.


## Media
On the recommendation of my lecturer, I documented the [various stages of construction](https://github.com/eldar702/droneShield/blob/main/Video/Building_Photos/README.md),as well as [Bloopers](https://github.com/eldar702/droneShield/tree/main/Video/Bloopers) whos happend up the road. and even videos of my [first flight](https://www.youtube.com/watch?v=rWjGpgpi1M0) and [second flight](https://www.youtube.com/watch?v=i7E_WeZ5Nn4) :)
And even one of my [first autonomous flights](https://www.youtube.com/watch?v=UYRIvbps6jE), which ended hilarious. 

And finally, after a long, instructive and intriguing journey - [My final video](https://www.youtube.com/watch?v=eI0JDhAvPLg&t=13s).

## Dependencies
* [Python 3.6+](https://www.python.org/downloads/)
* [NumPy](https://numpy.org/install/)
* [dronekit](https://github.com/dronekit/dronekit-python)
* [pymavlink](https://github.com/ArduPilot/pymavlink)
* [cv2](https://pypi.org/project/opencv-python/)
* [scipy](https://scipy.org/)
* [RPi.GPIO](https://pypi.org/project/RPi.GPIO/)

