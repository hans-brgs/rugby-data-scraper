import logging
from typing import Dict, Any, Optional
from config.api_config import get_urls_core_api
from config.api_counter import API_request, APIRequestError

##########################################	GLOBAL SCOPE	#######################################
# logs
logger = logging.getLogger(__name__)


########################################## CLASS ##################################################
class ScrappingError(Exception):
    pass

class ParsingError(Exception):
    pass

##########################################	FUNCTIONS	###########################################

def scrape_api_request(
    endpoint_key: str,
    url_params: Optional[Dict[str, Any]] = None,
    query_params: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Prepares and executes an API request based on the provided endpoint key and parameters.

    Args:
        api_type (API): The type of API to use (WEB or CORE).
        endpoint_key (str): The key for the desired endpoint in the endpoints dictionary.
        url_params (Dict[str, Any]): A dictionary of parameters to format the URL.
        query_params (Optional[Dict[str, Any]]) : Optional query parameters to add to the request.

    Returns:
        Dict[str, Any] : The JSON response from the API as a dictionary.
    """
    try:
        api_base, endpoints = get_urls_core_api()

        endpoint = endpoints[endpoint_key]
        if url_params is None:
            url_endpoint = endpoint["url"]
        else:
            url_endpoint = endpoint["url"].format(**url_params)
        api_url = f"{api_base}{url_endpoint}"
        params = {**endpoint.get("params", {}), **(query_params or {})}
        # {**dict1, **dict2} creates a new dictionary containing all the elements of dict1 and dict2.
        # If the two dictionaries have keys in common, the values of dict2 overwrite those of dict1.

        response = API_request(api_url, params)
        return response.json()
    except KeyError as key_err:
        logger.error(f"Dict parse KeyError: {key_err}")
        raise ScrappingError
    except APIRequestError:
        logger.error(f"API_request() error.")
        raise ScrappingError
    except Exception as e:
        logger.error(f"An unexpected error has occurred: {e}")
        raise ScrappingError


# --------------------------------------------------------------------------------------------------


def parse_urls(urls_response: Dict[str, Any]) -> list[str]:
    """
    Parse the JSON response containing containing a list
    of URL.

    Args:
        urls_response (dict): A dictionary from `scrape_XXXXX_url()` containing
        the API response with all urls pointing to a specific information (team, event, ..).

    Raises:
        Exception: For any unexpected errors.
        KeyError: If there is an error parsing the JSON response.

    Returns:
        list[str]: A tupple containing the urls of all teams for a specific information (team, league, event ...).
            For example: [
                    "http://sports.core.api.espn.com/v2/sports/rugby/leagues/270559/seasons/2024/teams/25912",
                    "http://sports.core.api.espn.com/v2/sports/rugby/leagues/270559/seasons/2024/teams/25917",
                    "..."
                ]
    """
    try:
        # Parse leagues data, to get name and id
        urls = []  # dict containing the name associated with the league id.
        for url in urls_response["items"]:
            urls.append(url["$ref"])
        return urls

    except KeyError as key_err:
        logger.error(f"Dict parse KeyError: {key_err}")
        raise ParsingError
    except Exception as e:
        logger.error(f"An unexpected error has occurred: {e}")
        raise ParsingError


# --------------------------------------------------------------------------------------------------


def scrape_url(url: str) -> Dict[str, Any]:
    """
    Scrape data from a specific url.

    Args:
        url (str): A string exctracting from "parse_urls()" containing a url pointing to
                    specific information.

    Raises:
        APIRequestError: If there is an error during the API request.
        KeyError: If there is an error parsing the JSON and the expected keys are not found.
        Exception: For any unexpected errors.

    Returns:
        Dict[str, Any]: A dictionary containing the specific url response to scraper.
    """
    try:
        # Scrape team data
        response = API_request(url)  # Get request
        team_info = response.json()
        return team_info

    except APIRequestError:
        logger.error(f"API_request() error.")
        raise ScrappingError
    except KeyError as key_err:
        logger.error(f"Dict parse KeyError: {key_err}")
        raise ScrappingError
    except Exception as e:
        logger.error(f"An unexpected error has occurred: {e}")
        raise ScrappingError
