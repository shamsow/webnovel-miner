# Load our configuration
import os
from configparser import ConfigParser
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_data = ConfigParser()
config_data.read(os.path.join(BASE_DIR, 'miner', 'config.ini'))