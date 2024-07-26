
import logging
from typing import Dict, Any

from processing.utils import get_number_field, convert_date_time_to_MySQL
from scraping.utils import parse_urls


##########################################	GLOBAL SCOPE	#######################################
# logs
logger = logging.getLogger(__name__)

##########################################	FUNCTIONS	###########################################


def parse_leagues_id(league_pages: list[Dict[str, int]]) -> Dict[str, int]:
    """
    Parses league IDs from a list of league page dictionaries.

    This function extracts the name and ID (slug) of each league from the provided league pages.

    Args:
        league_pages (list[Dict[str, Any]]): A list of dictionaries, each containing data about a league.

    Returns:
        Dict[str, int]: A dictionary where the keys are league names and the values are their corresponding ESPN IDs (slugs).

    Raises:
        KeyError: If the required keys ('name' or 'slug') are missing from any league page dictionary.
        Exception: For any unexpected errors during the parsing process.

    Note:
        - The function assumes that each league page dictionary contains at least 'name' and 'slug' keys.
        - The 'slug' is converted to an integer and used as the league's ESPN ID.
    """
    try:
        leagues_id = {}
        for page in league_pages:
            leagues_id[page["name"]] = int(page["slug"])
        return leagues_id

    except KeyError as KeyErr:
        logger.error(f"Key not found in dictionary: {KeyErr}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error has occurred: {e}")
        raise


def parse_seasons_year(league_season_urls_page: Dict[str, int]) -> list[int]:
    """
    Parses season years from a dictionary of league season URLs.

    This function extracts the year from each season URL and returns a list of these years.

    Args:
        league_season_urls_page (Dict[str, int]): A dictionary containing league season URL data.

    Returns:
        list[int]: A list of integers representing the years of the seasons extracted from the URLs.

    Raises:
        Exception: For any unexpected errors during the parsing process, including issues with URL parsing or data extraction.

    Note:
        - This function relies on external 'parse_urls' and 'get_number_field' functions to process the URLs.
        - It assumes that the year is the last numeric field in each URL.
    """
    try:
        urls = parse_urls(league_season_urls_page)
        seasons_year = []
        for url in urls:
            seasons_year.append(int(get_number_field(url, -1)))
        return seasons_year

    except Exception as e:
        logger.error(f"An unexpected error has occurred: {e}")
        raise


def parse_calendar_dates(calendar_page: Dict[str, Any]) -> list[str]:
    """
    Parses and formats calendar dates from a calendar page dictionary.

    This function extracts dates from the calendar page data and formats them into MySQL-compatible date strings.

    Args:
        calendar_page (Dict[str, Any]): A dictionary containing calendar page data, expected to have an 'eventDate' key with a 'dates' list.

    Returns:
        list[str]: A list of formatted date strings in MySQL format.

    Raises:
        KeyError: If the required keys are missing from the calendar page dictionary.
        Exception: For any unexpected errors during the date parsing and formatting process.

    Note:
        - This function relies on an external 'convert_date_time_to_MySQL' function to format the dates.
        - It assumes that the 'eventDate' key in the calendar page contains a 'dates' list with valid date information.
    """
    try:
        dates = []
        for date in calendar_page["eventDate"]["dates"]:
            formating_date = convert_date_time_to_MySQL(date)
            dates.append(formating_date)
        return dates

    except KeyError as KeyErr:
        logger.error(f"Key not found in dictionary: {KeyErr}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error has occurred. {e}")
        raise
