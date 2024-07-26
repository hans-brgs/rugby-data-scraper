import os
import json

import logging

##########################################	GLOBAL SCOPE	#######################################
# logs
logger = logging.getLogger(__name__)

##########################################	FUNCTIONS	###########################################

def get_root_dir():
    """
        Get the root path.
  
        Returns:
            root_path (str) : root path
    """
    dir = os.path.dirname(__file__)
    root_path = os.path.abspath(os.path.join(dir, os.pardir))
    return(root_path)

#--------------------------------------------------------------------------------------------------

def get_config_file():
    """
        Get the config file path.
  
        Returns:
            config_path (str) : config file path
    """
    config_path = os.path.join(get_root_dir(),"config/api_endpoints.json")
    return(config_path)

#--------------------------------------------------------------------------------------------------

def get_urls_core_api():
    """
        Get the core api base url and endpoints from config file.
  
        Returns:
            api_base (str) : url of API base.
            endpoints (dict) : dictionnary of endpoints API.
                                endpoints : 
                                - team_info
                                - team_stats_standing
                                - team_stats_by_match
                                - match_duration
                                - player_stats_by_match
            params (dict) : dictionary of URL api parameters
    """
    # Get json config file with url parts
    with open(get_config_file(), "r") as f:
        configs = json.load(f)
    
    # Create api url to get league information
    api_base = configs["API"]["core_api_base"]
    endpoints = configs["API"]["core_endpoints"]
    return (api_base, endpoints)