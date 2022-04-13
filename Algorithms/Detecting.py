##################   imports & defines     ##################   
import cv2
from centroidtracker import CentroidTracker
import DroneFunc


class Detect:
    def __init__(self):
        self.threshold = 0.25  # Threshold to detect object
        self.nms = 0.2
        self.Height, self.Weight = 640, 480
        self.frame_center_x = self.Height / 2
        self.frame_center_y = self.Weight / 2

        self.desire_area = DroneFunc.distance_to_size(2)  # the number is in meters, can be float

        self.classNames = []
        self.tracker = CentroidTracker(maxDisappeared=10)
        self.tracked_objects = ['sports ball']

        classFile = "/home/pi/Desktop/Object_Detection_Files/neural_network_files/coco.names"
        configPath = "/home/pi/Desktop/Object_Detection_Files/neural_network_files/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
        weightsPath = "/home/pi/Desktop/Object_Detection_Files/neural_network_files/frozen_inference_graph.pb"
        with open(classFile, "rt") as f:
            self.classNames = f.read().rstrip("\n").split("\n")

        # Init neural network variables:
        self.net = cv2.dnn_DetectionModel(weightsPath, configPath)
        self.net.setInputSize(320, 320)
        self.net.setInputScale(1.0 / 127.5)
        self.net.setInputMean((127.5, 127.5, 127.5))
        self.net.setInputSwapRB(True)

    def getBoxes(self, img):
        boxes = []
        classIds, confs, bbox = self.net.detect(img, confThreshold=self.threshold, nmsThreshold=self.nms)
        if len(classIds) != 0:
            for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
                className = self.classNames[classId - 1]
                if className in self.tracked_objects:
                    boxes.append(box)
                    cv2.rectangle(img, box, color=(0, 255, 0), thickness=1)
        return boxes

    def detecting(self):
        cap = cv2.VideoCapture(0)
        cap.set(3, self.Height)
        cap.set(4, self.Weight)
        # cap.set(10,70)

        while True:
            success, img = cap.read()
            detected_boxes = self.getBoxes(img)
            objects = self.tracker.update(detected_boxes)
            detected_flag = len(objects)
            # moving the drone so the balloon will be in the middle of the frame (= in front of the drone)
            if detected_flag:
                drone_x, drone_y, drone_z = DroneFunc.values_for_balloon_centered(detected_boxes[0], self.frame_center_x,
                                                                                  self.frame_center_y, self.desire_area)
                DroneFunc.send_local_ned_velocity(drone_x, drone_y, drone_z)
            # loop over the tracked objects and write details on screen (rectangle and id).
            for (objectID, centroid) in objects.items():
                # draw the ID and the centroid of the object
                text = "ID {}".format(objectID)
                cv2.putText(img, text, (centroid[0] - 10, centroid[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0),
                            2)
                cv2.circle(img, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

            cv2.imshow("Output", img)
            cv2.waitKey(1)


def write_details_on_screen(img, objects):
    for (objectID, centroid) in objects.items():
        # draw the ID and the centroid of the object
        text = "ID {}".format(objectID)
        cv2.putText(img, text, (centroid[0] - 10, centroid[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.circle(img, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)


if __name__ == "__main__":
    detect = Detect()
    detect.detecting()
