###############################        Defines & Imports       #######################################
import logging, time, argparse, configparser
#checking

# parser use to get the location of the app
parser = argparse.ArgumentParser()
parser.add_argument('--d', nargs=1, default=None)
args = parser.parse_args()

# the app directory location
APP_DIR = args.d[0] if args.d != None else "./"
# the location to the configuration file
CONFIGURATIONS = APP_DIR + 'configuration.ini'

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        # create the log files inside the logs directory. 
        logging.FileHandler(APP_DIR + 'logs/main app | ' + str(time.asctime()) + '.log'),
        logging.StreamHandler() ])


config = configparser.ConfigParser()
if len(config.read(CONFIGURATIONS)) == 0:
    logging.error("Could Not Read Configurations File: " + CONFIGURATIONS)
    sys.exit()  

DRONE_ID = config['drone']['id']
HOST_IP = config['cloud-app']['ip'] 
VIDEO_PORT = int(config['cloud-app']['video-port'])

GRAYSCALE = config['video']['grayscale'].lower() == 'true'
FRAMES_PER_SECOND = int(config['video']['fps'])
JPEG_QUALITY = int(config['video']['quality'])
WIDTH = int(config['video']['width'])
HEIGHT = int(config['video']['height'])

#######################################      Main      ################################################  
if __name__ == '__main__':
    logging.debug('droneapp has started! THE directory is: %s', APP_DIR)
    logging.info('FPS: %s Quality: %s Width: %s Height: %s Grayscale: %s',
                 str(FRAMES_PER_SECOND), str(JPEG_QUALITY), str(WIDTH), str(HEIGHT), GRAYSCALE)           
    logging.info('Drone ID: %s Video Recipient: %s, %s', str(DRONE_ID), str(HOST_IP), str(VIDEO_PORT))
# logging.basicConfig(filename='./logs/' + str(time.asctime()) + '.log',
#                     filemode='w',
#                     level=logging.DEBUG,
#                     format='%(asctime)s %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')