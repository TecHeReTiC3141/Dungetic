from scripts.Maths import *
import logging

logging.basicConfig(level=logging.INFO, filename='../logs.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(module)s - %(funcName)s: %(message)s',
                    datefmt='%H:%M:%S')
logging.info('The game has started')
