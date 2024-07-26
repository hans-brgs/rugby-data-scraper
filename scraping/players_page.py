import logging
from typing import Dict, Any
from datetime import datetime
from scraping.utils import ParsingError, ScrappingError, parse_urls, scrape_api_request, scrape_url


##########################################	GLOBAL SCOPE	#######################################
# logs
logger = logging.getLogger(__name__)

##########################################	FUNCTIONS	###########################################

def scrape_roster_pages(event_pages : list[Dict[str, Any]]) -> list[Dict[str, Any]]:
    """
    Scrapes roster pages for each competitor in the provided event pages.

    This function extracts roster URLs from event pages and scrapes the corresponding roster data.
    If roster data is missing for a competitor, it logs a warning and continues with the next.

    Args:
        event_pages (list[Dict[str, Any]]): A list of dictionaries containing event page data.

    Returns:
        list[Dict[str, Any]]: A list of dictionaries, each containing roster data for a team.

    Raises:
        KeyError: If required keys are missing from the event page data.
        ValueError: If there's an issue with data values during processing.
        Exception: For any unexpected errors during the scraping process.

    Note:
        This function relies on external functions for URL scraping.
    """
    roster_pages = []
    try:
        for page in event_pages:
            # Get Competitors
            competitions = page["competitions"][0]
            competitors = competitions["competitors"]

            for competitor in competitors :
                # Check if roster exist
                roster_url = competitor.get("roster", {}).get("$ref", None)
                if roster_url is None :
                    logger.warning(f"Roster data missing in ESPN database for match '{page['name']}' (ID: {page['id']}).")
                    continue
                roster_page = scrape_url(roster_url)
                roster_pages.append(roster_page)

    except KeyError as key_err:
        logger.error(f"Dict parse KeyError: {key_err}")
        raise
    except ValueError as val_err:
        logger.error(f"ValueError : {val_err}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error has occurred: {e}")
        raise
    return roster_pages