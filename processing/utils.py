import logging
from typing import Dict, Any
import hashlib
import re

from datetime import datetime
from dateutil import parser
from scraping.utils import scrape_url

##########################################	GLOBAL SCOPE	#######################################
# logs
logger = logging.getLogger(__name__)

##########################################	FUNCTIONS	###########################################

def extract_stats(stat_url : str) -> Dict[str, int] :
    """
    Extracts statistical data from a given dictionary containing API response data.

    This function fetches detailed statistics from a provided URL reference within the input data,
    processes the statistics, and returns them in a structured dictionary format.

    Args:
        data (Dict[str, Any]): A dictionary containing the API response data. It is expected to
                               have a nested dictionary with a key "statistics" containing a URL 
                               reference to the detailed statistics.

    Raises:
        KeyError: If a key is not found in the provided dictionary.
        Exception: For any unexpected errors during the process.

    Returns:
        Dict[str, int]: A dictionary containing the extracted statistics where the keys are the
                        names of the statistics and the values are their corresponding values.
                        For example:
                        {
                            "tries": 3,
                            "conversions": 2,
                            "penalties": 4,
                            ...
                        }
    """
    try :
        scrape_statistics = scrape_url(stat_url)
        statistics = {}
        for group_stat in scrape_statistics["splits"]["categories"][0]["stats"]:
                stat = {group_stat["name"] : group_stat["value"]}
                statistics.update(stat)
        return statistics
    except KeyError as KeyErr:
        logger.error(f"Dict parse KeyError: {KeyErr}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error has occurred: {e}")
        raise

#--------------------------------------------------------------------------------------------------

def extract_linescores(linescore_url: str) -> Dict[str, Any]:
    """
    Extracts linescore data from a given URL containing linescore information.

    This function fetches linescore data from the provided URL, processes the information,
    and returns it in a structured dictionary format.

    Args:
        linescore_url (str): A URL string pointing to the linescore data resource.

    Raises:
        KeyError: If a required key is not found in the scraped data structure.
        Exception: For any unexpected errors during the scraping or processing.

    Returns:
        Dict[str, Any]: A dictionary containing the extracted linescores where the keys represent
                        different periods of the game and the values are the corresponding scores.
                        The dictionary includes the following keys:
                        - "linescore1stHalf": Score for the first half (period 1)
                        - "linescore2ndHalf": Score for the second half (period 2)
                        - "linescore20min": Score at 20 minutes
                        - "linescore60min": Score at 60 minutes
                        Any of these values may be None if not available in the source data.

    Note:
        This function relies on an external 'scrape_url' function to fetch data from the provided URL.
    """
    try :
        scrape_linescores = scrape_url(linescore_url)
        linescores = {
            "linescore1stHalf": None,
            "linescore2ndHalf": None,
            "linescore20min": None,
            "linescore60min": None
        }
        for linescore in scrape_linescores["items"]:
                period = linescore["period"]
                value = linescore["value"]
                match period :
                    case 1 :
                        linescores["linescore1stHalf"] = value
                    case 2 :
                        linescores["linescore2ndHalf"] = value
                    case 20 :
                        linescores["linescore20min"] = value
                    case 60 :
                       linescores["linescore60min"] = value
        return linescores
    except KeyError as KeyErr:
        logger.error(f"Dict parse KeyError: {KeyErr}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error has occurred: {e}")
        raise

#--------------------------------------------------------------------------------------------------

def get_number_field(url, index_field) -> int :
    """
    Extracts a numeric field from a given URL at a specified index.

    This function parses the URL to find all numeric fields, then returns the number
    at the specified index position.

    Args:
        url (str): The URL string to parse for numeric fields.
        index_field (int): The index of the desired numeric field to extract, starting at index 0.

    Raises:
        ValueError: If the URL is invalid or contains no numeric fields.
        IndexError: If the specified index is out of range of the available numeric fields.
        Exception: For any unexpected errors during the process.

    Returns:
        int: The numeric value extracted from the URL at the specified index.
    """
    try :
        # Extraire tous les nombres de l'URL
        numbers = re.findall(r'/(\d+)', url)
        if not numbers:
            raise ValueError(f"URL is invalid or contains no numeric fields: {url}")
        
        # Tenter d'accéder à l'index spécifié
        return int(numbers[index_field])
    
    except IndexError:
        error_msg = f"Index ({index_field}) is out of range. Available indices: 0 to {len(numbers) - 1}"
        logger.error(error_msg)
        raise
    except ValueError as ve:
        logger.error(str(ve))
        raise
    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}")
        raise

#--------------------------------------------------------------------------------------------------

def generate_deterministic_uid(unique_keys: list[Any]) -> str:
    """
    Generates a deterministic unique identifier (UID) based on a list of unique keys.

    This function creates a 16-character hexadecimal UID by combining and hashing the provided unique keys.
    The generated UID is consistent for the same input, making it deterministic.

    Args:
        unique_keys (list[Any]): A list of values to be used as unique keys for generating the UID.
                                 These can be of any type that can be converted to a string.

    Raises:
        ValueError: If the unique_keys list is empty.
        Exception: For any unexpected errors during the process.

    Returns:
        str: A 16-character hexadecimal string representing the generated UID.
    """
    try :
        if not unique_keys:
            raise ValueError("unique_keys dictionary cannot be empty")
        
        # Convert all elements to strings
        str_keys = [str(key) for key in unique_keys]

        # Sort keys to ensure constant order
        sorted_keys = sorted(str_keys)

        # Combining unique keys into a single string
        combined_key = "_".join(sorted_keys)
        
        # Using SHA256 to generate a hash
        hash_object = hashlib.sha256(combined_key.encode('utf-8'))
        hash_hex = hash_object.hexdigest()
        
        # We take the first 16 characters of the hash for a shorter ID
        return hash_hex[:16]
    
    except ValueError as ValErr:
        logger.error(ValErr)
        raise
    except Exception as e:
        logger.error(f"An unexpected error has occurred: {e}")
        raise

#--------------------------------------------------------------------------------------------------

def convert_lbs_to_kg(mass: float) -> float:
    convertor = 2.211
    return mass/convertor

#--------------------------------------------------------------------------------------------------

def convert_inches_to_meters(length: float) -> float:
    convertor = 39.37
    return length/convertor

#--------------------------------------------------------------------------------------------------

def convert_date_time_to_MySQL(date : str):
    try :
        # Parser la chaîne ISO
        parse_date = parser.parse(date)
        # Convertir en format MySQL datetime
        date_MySQL = parse_date.strftime('%Y-%m-%d %H:%M:%S')
    except parser.ParserError as ParsErr:
        logger.error(f"Date format error has occurred : {ParsErr}")
        raise
    return date_MySQL
