import logging
import requests
from typing import List

###### GLOBAL SCOPE ######

# logs
logger = logging.getLogger(__name__)

##########################################	CLASS	###########################################

class APICounter:
    """
        A singleton class for counting API calls in an application.

        This class provides a method for incrementing a counter and a method
        to obtain the counter's current value. It is designed to be used
        as a singleton, ensuring that only one instance of the counter exists
        in the entire application.

        Attributes:
            count (int): The total number of API calls counted.

        Methods:
            increment(): Increment the counter by 1.
            get_count(): Returns the current counter value.

    """
    _instance = None
    count = 0

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def increment(self):
        self.count += 1

    def get_count(self):
        return self.count


class SessionManager:
    _instance = None

    def __init__(self) -> None:
        self.session: requests.Session
        self.user_agents: List[str]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
            cls._instance.__init__()
            cls._instance.session = requests.Session()

        return cls._instance

    def get_session(self) -> requests.Session:
        # Rotate User-Agent
        return self.session



##########################################	FUNCTIONS	###########################################

# Utility function to obtain counter instance
def get_counter():
    return APICounter()

# Custom exception for API request errors.
class APIRequestError(Exception):
    pass

# API Request with counter
def API_request(url, params=None):
    """
    Makes a GET request to the specified URL and increments the API counter.

    Args:
        url (str): The URL of the request.
        params (dict, optional): The request params. Default None.

    Returns:
        requests.Response: The request response object.

    Raises:
        APIRequestError: If an error occurs during the request.

    Note:
        The API counter is incremented only in the event of a successful request.
    """
    session = SessionManager().get_session()
    try:
        # request headers
        headers = {'User-Agent': 
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0'} 

        response = session.get(url, headers=headers, timeout=10, params=params)
        response.raise_for_status()
        if not response.json():
            raise APIRequestError(f"Request error : The response JSON is empty. Check url : {url}")
        get_counter().increment()
        return(response)

    except requests.exceptions.RequestException as e:
        error_message = f"Request error: {e}. Response : {response.content}"
        logger.error(error_message)
        raise APIRequestError
    except Exception as e :
        error_message = f"An unexpected error has occurred: {e}"
        logger.error(error_message)
        raise APIRequestError
