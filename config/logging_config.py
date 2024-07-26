import logging
import coloredlogs
import os
from config.api_config import get_root_dir

ROOT_PATH = get_root_dir()

# Basic logging configuration with custom format
logging.basicConfig(
    level=logging.INFO, #Level of global log
    format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(os.path.join(ROOT_PATH,"logs/app.log")), #Handler to write logs in a file
        logging.StreamHandler()
    ]
)

# Setting up coloredlogs to add colors
coloredlogs.install(
    level='DEBUG',
    fmt='%(asctime)s - %(name)s.%(funcName)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level_styles={
        'debug': {'color': 'green'},
        'info': {'color': 'blue'},
        'warning': {'color': 'yellow'},
        'error': {'color': 'red'},
        'critical': {'color': 'red', 'bold': True},
    },
    field_styles={
        'asctime': {'color': 'cyan'},
        'name': {'color': 'magenta'},
		'funcName' : {'color': 'magenta'},
        'levelname': {'color': 'white', 'bold': True},
        'message': {'color': 'white'},
    }
)


