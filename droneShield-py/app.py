###############################        Defines & Imports       #######################################
import logging, time, argparse
#checking

# parser use to get the location of the app
parser = argparse.ArgumentParser()
parser.add_argument('--d', nargs=1, default=None)
args = parser.parse_args()

# the app directory location
APP_DIR = args.d[0] if args.d != None else "./"


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(APP_DIR + 'logs/main app | ' + str(time.asctime()) + '.log'),
        logging.StreamHandler() ])


#######################################      Main      ################################################  
if __name__ == '__main__':
    logging.debug('droneapp has started! THE directory is %s', APP_DIR)
                    

# logging.basicConfig(filename='./logs/' + str(time.asctime()) + '.log',
#                     filemode='w',
#                     level=logging.DEBUG,
#                     format='%(asctime)s %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')