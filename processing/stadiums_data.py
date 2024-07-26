import logging
from typing import Dict, Any

##########################################	GLOBAL SCOPE	#######################################
# logs
logger = logging.getLogger(__name__)

##########################################	FUNCTIONS	###########################################

def process_stadiums_data(event_pages : list[Dict[str, Any]]) -> list[Dict[str, Any]]:
    """
    Processes stadium data from a list of event pages and returns unique stadium information.

    This function extracts stadium details from each event page, ensuring that each stadium
    is only processed once. It handles cases where stadium information might be missing or
    incomplete.

    Args:
        event_pages (list[Dict[str, Any]]): A list of dictionaries containing event page data.

    Returns:
        list[Dict[str, Any]]: A list of dictionaries, each containing data for a unique stadium.
        Each dictionary has the following structure:
        {
            "espnId": int,              # ESPN ID of the stadium
            "name": str,                # Full name of the stadium
            "grass": bool,              # True if the stadium has a grass field, False otherwise
            "indoor": bool,             # True if the stadium is indoor, False otherwise
            "city": str or None,        # City where the stadium is located (if available)
            "state": str or None        # State where the stadium is located (if available)
        }

    Raises:
        KeyError: If required keys are missing from the event page data.
        Exception: For any unexpected errors during the processing of stadium data.

    Note:
        - This function uses a set to track processed stadium IDs to avoid duplicates.
        - City and state information may be None if not available in the venue data.
    """
    stadiums_data : list[Dict[str, Any]] = []
    stadiums_ids = set()

    try:
        for page in event_pages:
            # Get stadium information if exist
            venue = page["competitions"][0].get("venue", None)
            if venue is None :
                continue

            # Extract stadium id
            stadium_id = int(venue["id"])

            # Check if stadium has already processed
            if stadium_id in stadiums_ids:
                continue # if true skip

            try :
                city = venue["address"]["city"]
                state = venue["address"]["state"]
            except KeyError:
                city = None
                state = None
            
            # fill the table pattern
            stadium_data = {
                "espnId": stadium_id,
                "name": venue["fullName"],
                "grass": venue["grass"],
                "indoor": venue["indoor"],
                "city": city,
                "state": state,
            }

            stadiums_data.append(stadium_data)
            stadiums_ids.add(stadium_id)

    except KeyError as key_err:
        logger.error(f"Dict parse KeyError: {key_err}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error has occurred: {e}")
        raise

    return stadiums_data
