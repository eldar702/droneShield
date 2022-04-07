##################   imports & defines     ##################   
import cv2
from centroidtracker import CentroidTracker
import DroneFunc
# Init global variables:
threshold = 0.25  # Threshold to detect object
nms = 0.2
(Height, Weight) = (640, 480)
frame_center_x = Height / 2
frame_center_y = Weight / 2

desire_area = DroneFunc.distance_to_size(2) # the number is in meters, can be float

classNames = []
tracker = CentroidTracker(maxDisappeared=10)
tracked_objects = ['sports ball']

classFile = "/home/pi/Desktop/Object_Detection_Files/neural_network_files/coco.names"
configPath = "/home/pi/Desktop/Object_Detection_Files/neural_network_files/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "/home/pi/Desktop/Object_Detection_Files/neural_network_files/frozen_inference_graph.pb"
with open(classFile, "rt") as f:
	classNames = f.read().rstrip("\n").split("\n")

# Init neural network variables:
net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)


def getBoxes(img):
	boxes = []
	classIds, confs, bbox = net.detect(img, confThreshold=threshold, nmsThreshold=nms)
	if len(classIds) != 0:
		for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
			className = classNames[classId - 1]
			if className in tracked_objects:
				boxes.append(box)
				cv2.rectangle(img, box, color=(0, 255, 0), thickness=1)
	return boxes


def detecting():
	cap = cv2.VideoCapture(0)
	cap.set(3, Height)
	cap.set(4, Weight)
	# cap.set(10,70)

	while True:
		success, img = cap.read()
		detected_boxes = getBoxes(img)
		objects = tracker.update(detected_boxes)
		detected_flag = len(objects)
		# moving the drone so the balloon will be in the middle of the frame (= in front of the drone)
		if detected_flag:
			drone_x, drone_y, drone_z = DroneFunc.values_for_balloon_centered(detected_boxes[0], frame_center_x, frame_center_y, desire_area)
			DroneFunc.send_local_ned_velocity(drone_x, drone_y, drone_z)
		# loop over the tracked objects and write details on screen (rectangle and id).
		for (objectID, centroid) in objects.items():
			# draw the ID and the centroid of the object
			text = "ID {}".format(objectID)
			cv2.putText(img, text, (centroid[0] - 10, centroid[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
			cv2.circle(img, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

		cv2.imshow("Output", img)
		cv2.waitKey(1)


if __name__ == "__main__":
	detecting()
