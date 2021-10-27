import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
import time, socket, logging, configparser, argparse, sys
from utils import Utils

parser = argparse.ArgumentParser()
parser.add_argument('--d', nargs=1, default=None)
args = parser.parse_args()

APP_DIR = args.d[0] if args.d != None else "./"
CONFIGURATIONS = APP_DIR + 'configuration.ini'

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(APP_DIR + 'logs/video-streamer | ' + str(time.asctime()) + '.log'),
        logging.StreamHandler()
    ]
)                    

config = configparser.ConfigParser()

if len(config.read(CONFIGURATIONS)) == 0:
    logging.error("Could Not Read Configurations File: " + CONFIGURATIONS)
    sys.exit()     

DRONE_ID = config['drone']['id']
HOST_IP = config['cloud-app']['ip']
VIDEO_PORT = int( config['cloud-app']['video-port'])

GRAYSCALE = config['video']['grayscale'].lower() == 'true'
FRAMES_PER_SECOND = int( config['video']['fps'])
JPEG_QUALITY = int( config['video']['quality'])
WIDTH = int( config['video']['width'])
HEIGHT = int( config['video']['height'])

logging.info('FPS: %s  Quality: %s  Width %s Height %s  Grayscale: %s', 
             str(FRAMES_PER_SECOND), str(JPEG_QUALITY), str(WIDTH), str(HEIGHT), GRAYSCALE)
logging.info('Drone ID: %s  Video Recipient: %s:%s', str(DRONE_ID), str(HOST_IP), str(VIDEO_PORT))

camera = None
video_socket = None

while(True):
    try:
        camera = PiCamera()
        camera.resolution = (WIDTH, HEIGHT)
        camera.framerate = FRAMES_PER_SECOND

        rawCapture = PiRGBArray(camera, size=(WIDTH, HEIGHT))
        time.sleep(0.1)

        logging.info("Camera module initiated")
        
        video_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        video_socket.connect((HOST_IP, VIDEO_PORT))

        logging.info("Socket Opened, Video Streaming started")


        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            image_data = frame.array
            
            image_data = cv2.rotate(image_data, cv2.ROTATE_180)
            
            if GRAYSCALE:
                image_data = cv2.cvtColor(image_data, cv2.COLOR_BGR2GRAY)
            
            code, jpg_buffer = cv2.imencode(".jpg", image_data, [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY])

            datagramMsgBytes = Utils.create_datagram_message(DRONE_ID, jpg_buffer)

            video_socket.sendall(datagramMsgBytes)
            
            rawCapture.truncate(0)


    except Exception as e:
        logging.error("Video Stream Ended: "+str(e))
        
        if camera != None:
            camera.close()
        if video_socket != None:
            video_socket.close()
        
        time.sleep(2)