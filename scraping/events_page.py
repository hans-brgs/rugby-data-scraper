import json
import logging
from click import pause
from typing import Dict, Any
from datetime import datetime
from scraping.utils import ParsingError, ScrappingError, parse_urls, scrape_api_request, scrape_url


##########################################   GLOBAL SCOPE   #######################################
# logs
logger = logging.getLogger(__name__)

#########################################      CLASS      #########################################
class DateFormatError(Exception):
    pass

#########################################    FUNCTIONS    #########################################

def filter_valid_event_pages(event_pages: list[Dict[str, Any]]) -> list[Dict[str, Any]] :
    """
    Filters out invalid or duplicate event pages based on the 'timeValid' field.

    This function checks the integrity of event pages by examining the 'timeValid' field.
    Pages with 'timeValid' set to False are considered duplicates or incomplete and are excluded.

    Args:
        event_pages (list[Dict[str, Any]]): A list of dictionaries containing event page data.

    Returns:
        list[Dict[str, Any]]: A filtered list of valid event pages.

    Note:
        - Logs a warning for each invalid page encountered.
        - Uses the 'pause()' function after logging each warning (ensure this function is defined).
    """
    valid_event_pages = []
    for event_page in event_pages :
        if event_page["timeValid"] == True :
            valid_event_pages.append(event_page)
        else :
            logger.warning(
                f"""It seems that this event page is duplicated or incomplete. 
                url : '{event_page["$ref"]}'. \nContent page : \n{json.dumps(event_page, indent = 4)})."""
            )
            pause()
    return valid_event_pages
        
#--------------------------------------------------------------------------------------------------

def date_format(date: str) -> str :
    """
    Converts a date string from "%Y-%m-%d %H:%M:%S" format to "%Y%m%d" format.

    Args:
        date (str): The input date string in "%Y-%m-%d %H:%M:%S" format.

    Returns:
        str: The formatted date string in "%Y%m%d" format.

    Raises:
        DateFormatError: If the input date string is in an invalid format.

    Note:
        - Uses strptime and strftime for date parsing and formatting.
        - Logs an error message before raising DateFormatError.
    """
    try:
        # convert dates format "%Y-%m-%d %H:%M:%S" to "%Y%m%d"
        formated_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%Y%m%d")
        return formated_date
    
    except ValueError as ValErr:
        logger.error(f"Input date error : {ValErr}")
        raise DateFormatError(ValErr) from ValErr

#--------------------------------------------------------------------------------------------------

def scrape_event_pages_by_date_range(espn_id_league: int, start_date: str, end_date: str, limit: int = 1000) -> list[Dict[str, Any]]:
    """
    Scrapes event pages for a specific league within a given date range.

    Args:
        espn_id_league (int): The ESPN ID of the league.
        start_date (str): The start date in "%Y-%m-%d %H:%M:%S" format.
        end_date (str): The end date in "%Y-%m-%d %H:%M:%S" format.
        limit (int, optional): The maximum number of events to retrieve. Defaults to 1000.

    Returns:
        list[Dict[str, Any]]: A list of dictionaries, each containing event page data.

    Raises:
        DateFormatError: If there's an error in date formatting.
        ScrappingError: If there's an error during the scraping process.
        ParsingError: If there's an error parsing the scraped data.
        Exception: For any unexpected errors.

    Note:
        - Uses date_format() to format dates.
        - Relies on external functions: scrape_api_request(), parse_urls(), and scrape_url().
    """
    # Set formated dates
    formated_start_date = date_format(start_date)
    formated_end_date = date_format(end_date)
    dates = formated_start_date + "-" + formated_end_date

    try:
        event_urls_page = scrape_api_request(
            "events_url_by_dates",
            url_params={"id_league": espn_id_league},
            query_params={
                "seasontypes": 1,
                "dates": dates,
                "limit": limit,
                }
        )
        event_urls = parse_urls(event_urls_page)
        event_pages = [scrape_url(event_url) for event_url in event_urls]
        return event_pages
    except DateFormatError:
        logger.error(f"Date format error.")
        raise
    except ScrappingError:
        logger.error(f"Scraping error.")
        raise
    except ParsingError:
        logger.error(f"Parsing error.")
        raise
    except Exception as e:
        logger.error(f"An unexpected error has occurred: {e}")
        raise

#--------------------------------------------------------------------------------------------------

def scrape_event_pages_for_gameday(espn_id_league: int, date: str, limit: int = 1000) -> list[Dict[str, Any]]:
    """
    Scrapes event pages for a specific league on a given date.

    Args:
        espn_id_league (int): The ESPN ID of the league.
        date (str): The date to scrape events for, in "%Y-%m-%d %H:%M:%S" format.
        limit (int, optional): The maximum number of events to retrieve. Defaults to 1000.

    Returns:
        list[Dict[str, Any]]: A list of dictionaries, each containing event page data.

    Raises:
        DateFormatError: If there's an error in date formatting.
        ScrappingError: If there's an error during the scraping process.
        ParsingError: If there's an error parsing the scraped data.
        Exception: For any unexpected errors.

    Note:
        - Uses date_format() to format the input date.
        - Relies on external functions: scrape_api_request(), parse_urls(), and scrape_url().
    """
    if date :
        formated_date = date_format(date)

    try:
        event_urls_page = scrape_api_request(
            "events_url_by_dates",
            url_params={"id_league": espn_id_league},
            query_params={
                "seasontypes": 1,
                "dates": formated_date,
                "limit": limit,
                }
        )
        event_urls = parse_urls(event_urls_page)
        event_pages = [scrape_url(event_url) for event_url in event_urls]
        return event_pages
    except DateFormatError:
        logger.error(f"Date format error.")
        raise
    except ScrappingError:
        logger.error(f"Scraping error.")
        raise
    except ParsingError:
        logger.error(f"Parsing error.")
        raise
    except Exception as e:
        logger.error(f"An unexpected error has occurred: {e}")
        raise
