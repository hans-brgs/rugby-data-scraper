import getpass
from pymysql.cursors import DictCursor
from os import system, name
from typing import Dict
from click import pause

import logging

##########################################	GLOBAL SCOPE	#######################################
# logs
logger = logging.getLogger(__name__)

##########################################	FUNCTIONS	###########################################

def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

def ui_db_config():
    """
    Asks the user for database connection information.
    
    Returns: dict: A dictionary containing the connection information.
    """
    clear()
    print("------ Please enter your database connection information ------")
    user_config = {
        "database": input("Database: "),
        "user": input("User: "),
        "password": getpass.getpass("password: ")
    }
    pause()
    clear()
    return user_config

def set_db_config(user_config: Dict) :
    db_config = {
        'host': 'localhost',
        'user': user_config["user"],
        'password': user_config["password"],
        'database': user_config["database"],
        'port': 3306,  # Port par défaut de MySQL, ajustez si nécessaire
        'charset': 'utf8mb4',
        'cursorclass': DictCursor
    }
    return db_config