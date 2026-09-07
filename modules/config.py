import socket
from configparser import ConfigParser, ExtendedInterpolation, NoSectionError
cfg = ConfigParser(interpolation=ExtendedInterpolation(), allow_no_value=True)

from modules.initializer import config_file

try:
    cfg.read("./modules/config.cfg")
    DEBUGGING = cfg.getboolean("Main", "debugging")
except NoSectionError:
    config_file()
    cfg.read("./modules/config.cfg")
    DEBUGGING = cfg.getboolean("Main", "debugging")
    
DEBUGGING_SOCKET = socket.gethostname()
DEBUGGING_PORT = 8080
SSL_CERT = None
SSL_KEY = None
PORT = 80 if not SSL_CERT else 443
