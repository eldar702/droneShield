![droneShield](https://user-images.githubusercontent.com/72104254/168979002-b660370d-bc6e-4410-b8e4-0f8d48daffaf.gif)

1. [General](#General)
    - [Background](#background)
2. [droneShield](#droneshield)
    - [Hardware](#Hardware)
    - [GroundStation](#GroundStation)
    - [Algorithms](#Algorithms)
3. [Dependencies](#dependencies) 



## General
### Background
In Israel, there is a problem, which causes the burning of thousands of dunams of Israeli territory - the problem of incendiary balloons.
Terrorist organizations, and for the most Hamas organization, have found a patent: they tie explosive devices to helium balloons and inflate them from the West Bank to the State of Israel in general and the surrounding settlements in particular.
The economic and safety damages are enormous: thousands of acres are burned each year and the safety of hundreds of thousands of residents of the affected envelope. The situation is absurd: balloons scare children instead of arousing the opposite emotion.
 There are several solutions: There are systems that use laser and blow up the incendiary balloons with a very high probability, but their price is so high and therefore dominates a few areas in the envelope. Another military solution is to use gliders, but flying a glider requires prior knowledge and special training. Also - not everyone has the technological orientation for this. As a result - this solution, like the previous one, is marketed as B2G. That is to say again - this is a complicated solution that provides a partial solution - also that using soldiers to fly the glider is a historic pre-historic. There are a number of other solutions but they are just the "same thing in a different guise".
So what - a computer science student can not create a solution that meets all three shortcomings that the other solutions fail to address? 
Say hello to droneShield.

## droneShield
### Background
I was asked by my 2 lecturers at the university, Dr. Ariel Roth and Asi Barak, to choose a problem and find a solution to it. Which problem I want, in which way I want. I presented the problem to you, now I presented the solution:
Droneshield is a fully autonomous laser drone, working from a groundcontrol and using its laser to eliminate the incendiary balloons.
droneShield is a skimmer that I designed and built myself.
droneShield is fully powered from the groundstation.
droneShield uses image processing to identify the balloons and uses state machine architecture to operate autonomously.
In a nutshell - with the click of a droneShield button activated, it flies to an area marked on a map located on the groundstation, scans for incendiary balloons, and destroys them, using the build-in laser if it finds any. And if that is not enough, after the scan he returns to the starting point, where he will wait for further instructions.

### Hardware
We will now scan all the components I have selected for the drone, as well as various considerations
#### **Motors**:
Perhaps one of the most important parts of a drone. There is a direct connection and tradeoff between speed and torque. The faster the motor, the less torque it produces.
Motors  of drones are commercially registered as follows: 2016 1000k, i.e:

4 digit numbers when the 2 first digits are the width of the rotor in mm.
So this motor has 20 mm wide rotor.
The last two digits are the height of the rotor in mm, so this motor has a 6 mm tall rotor.

And the KV rating tells you how fast the shaft will spin per volt with no load:
Higer kv means the motor will spin faster while lover kv means you have more torque.

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

#### **Frame**:  there is a lot of frames for drones, distinguish from one to other in size, shape and material. For building "custom big" drone, most of the guides in the internet recommend using a 450F plastic frame. I think it is a bad choice because of two main reasons:
1.	Size – there is no enough space on frame of the drone, so it force you use the space to smart and in most cases just make it little harder to design.
I would recommend choosing a 500F frame 
2.	Durability: plastic is to breakable. If it your first build of drone (as was for me) you are going to crash a lot of times. Too breakable frame will just be bad choice.
I would reccomand using of carbon frame. From my experience, it really worth the extra dollars and extra weight. You can look in few crashes I had with droneShield in the "loopers" folder

#### **Flight Control (FC)**
Is the control center of the drone. Meaning is the central hub that all the electronics component connect to.
I'm use here Pixhawk, and I REALY recommend using it.

#### **Companion computer**
the fc is like small computer but not really – it control all the component but it doesn’t have computing power. So how can you use artificial intelligent like image processing with your drone? Simply – connect a companion computer (very small and thin computer) to your drone. droneShield makes use of raspberry pi 4b for the image processing and algorithms use. 

#### **ESC**
Stands for electronic speed controllers. And as the name hints, it in charge of digests the PWM sent from the FC and produces an ESC output that will drive the motors.
It connects to the motor from one side and the other connects to the electric supply (in most cases to PDB – power distribution board and not to the battery directly).
ESC's specs will tell you what types of lipos you can use with them (2-4s 30a means you can use it with a battery of max 30a and 4 lipo cells)

#### **RC and Telemetry**:	
both of them are used to communicate data wirelessly with the drone. While Telemetry communication is bi directional, rc communication is unidirectional. 
Telemetry is used for communicate with ground station. In our case – droneShield communicate with QGroundControl
   
#### **GPS and Optical Flow**
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


## GroundStation:
For the drone to communicate with the operator, some "channel" is needed. It can communicate via remote control, the droneShield can definitely be operated via remote control. But the problem with this communication channel is understandable - requires the operator to know how to fly a glider and as I noted - violates one of the 3 main principles by which I worked and made decisions. We said that the drone should be autonomous and not require any prior knowledge.
2 programs are open source that include a very strong community and an insane amount of functionality.
1. QgroundControl
2. mission planner

Both are highly recommended. The first is more "clean" and intuitive so I chose to use it mainly, also attached to the Qgroundcontrol folder installation file, but if necessary I would recommend going into the QgroudControl or mission planner documentation

## Algorithms:
In order for droneShield to be as autonomous as possible, I used state machine architecture. So I defined a situation state, where each one includes a target task and a "transition function". A combination of these is called state.
The different states:
1.	**Takeoff**: 
Description: start executing a given mission by takeoff 
Transitions func: reached to location state
Goal: reached to desire meters height.

2.	**Reached to location**
Description: fly the drone to the desired location. “desire location”: is the suspected area, given by the user by clicking on the map.
Transitions func: Searching state
Goal: reached the given point.

3.	**Searching**
Description: looking for incendiary balloons.
Transitions func: Detecting state and back state
Goal: found a balloon.

4.	**Detecting**
Description: After the balloons is found in the Searching state, droneShield will aim at it and turn on the laser and make sure the balloon has indeed exploded
Transitions func:  Searching state and back state
Goal: to blow all the balloons that had founded 

5.	**Back**
Description: back to the point where the drone took off. when
Transitions func: the “takeoff” state
Goal: reached the “home” point and landed there, waiting to execute the next mission.

