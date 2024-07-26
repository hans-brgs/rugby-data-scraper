import json
import logging
from typing import Dict, Any, Tuple

from parsing.leagues_data import parse_calendar_dates
from processing.utils import generate_deterministic_uid, get_number_field
from scraping.events_page import scrape_event_pages_for_gameday
from scraping.league_pages import scrape_calendar_page, scrape_league_page, scrape_league_season_page


##########################################	GLOBAL SCOPE	#######################################
# logs
logger = logging.getLogger(__name__)

##########################################	CLASS	###########################################

class DateError(Exception) :
    pass

##########################################	FUNCTIONS	###########################################

def get_event_season_year(league_espn_id: int, date: str) -> int:
    # Get all events for a specific date
    event_pages = scrape_event_pages_for_gameday(league_espn_id, date)
    # Check if events exist for this specific date
    if event_pages == [] :
        # If no events exist, return 0
        return 0
    # If an event exists, retrieve the event page and return the year of the event season
    event_page = event_pages[0]
    return get_number_field(event_page["season"]["$ref"], 1)

#---------------------------------------------------------------------------------------------------

def check_dates_validity(league_espn_id: int, season_year: int, dates: list[str]) -> Tuple[str, str] : 
    """
    Validate and find the correct start and end dates for a given league season.

    During manual data scraping, inconsistencies were discovered in the start and end dates
    referenced on league pages and calendar pages. For example, the Top 14 2024 and 2025 seasons
    showed incorrect dates on the season page, and the calendar page for the Top 14 2019 season
    contained inaccurate date listings.

    To address this issue, a two-step verification process is implemented:
    1. We prioritize the calendar list over the start and end dates referenced on the season page,
       as it tends to be more reliable. Therefore, we scrape dates from the calendar.
    2. Since errors were predominantly found in the end dates, we iterate through the date list
       from the end, scraping match events for each date and verifying the associated season.
       We select the first date that corresponds to the correct season year as the end date.

    This approach ensures more accurate season date ranges, particularly for edge cases where
    official data may be inconsistent.

    Args:
        league_espn_id (int): The ESPN ID of the league.
        season_year (int): The year of the season to validate.
        dates (list[str]): A list of potential season dates, typically scraped from the calendar.

    Returns:
        Tuple[str, str]: A tuple containing the validated start and end dates for the season.

    Raises:
        DateError: If unable to find valid start or end dates for the specified season.
    """
    
    start_date = next((date for date in dates if get_event_season_year(league_espn_id, date) == season_year), None)
    if start_date is None :
        raise DateError(f"Unable to find season start date in : {dates}")

    end_date = next((date for date in reversed(dates) if get_event_season_year(league_espn_id, date) == season_year), None)
    if end_date is None :
        raise DateError(f"Unable to find season end date in : {dates}")
    
    return start_date, end_date

#--------------------------------------------------------------------------------------------------
    
def process_league_season_data( league_espn_id: int, season_year: int ) -> Dict[str, Any]:
    """
    Processes league and season data for a specific league and year.

    This function retrieves and combines data from multiple sources to create a comprehensive
    overview of a league's season, including dates, names, and other relevant information.

    Args:
        league_espn_id (int): The ESPN ID of the league.
        season_year (int): The year of the season to process.

    Returns:
        Dict[str, Any]: A dictionary containing processed league season data with the following structure:
        {
            "uid": str,                 # Unique identifier for the league-season combination
            "espnId": int,              # ESPN ID of the league
            "name": str,                # Full name of the league
            "abbreviationName": str,    # Abbreviated name of the league
            "startDate": str,           # Start date of the season in MySQL format
            "endDate": str,             # End date of the season in MySQL format
            "season": int,              # Year of the season
            "hasGroups": bool,          # Whether the league has groups/divisions
            "hasStandings": bool        # Whether the league maintains standings
        }

    Raises:
        KeyError: If required keys are missing from the scraped data.
        ValueError: If there are issues with data validation or conversion.
        Exception: For any unexpected errors during data processing.

    Note:
        - This function relies on several external scraping functions to gather data from different sources.
        - It generates a unique identifier for each league-season combination.
        - The function corrects potential inaccuracies in league names and dates by cross-referencing multiple data sources.
    """
    try:
        # scrape league `name` and `abbreviation` from the general league page, 
        # since this data is incorrect on the individual league page for each season.
        league_page = scrape_league_page(league_espn_id)
        league_name = league_page["name"]
        league_abbrevation_name = league_page["abbreviation"]

        if season_year : # If season year is specified, scrape directly calendar page (To scrap an entire season)
            calendar_page = scrape_calendar_page(league_espn_id, season_year)
        else : # Else, retrieve firstly the year of the current season then scrape calendar page (To scrap the latest GameDay of the current season)
            season_year = league_page["season"]["year"]
            calendar_page = scrape_calendar_page(league_espn_id, season_year)
        dates = parse_calendar_dates(calendar_page)
        # See docstring the function `check_dates_validity()`
        start_date, end_date = check_dates_validity(league_espn_id, season_year, dates)

        # scrape other informations from individual league page for each season.
        league_season_page = scrape_league_season_page(league_espn_id, season_year)

        # compute deterministic id
        uid = generate_deterministic_uid([league_espn_id, season_year])
    
        processed_data = {
            "uid": uid,
            "espnId": league_espn_id,
            "name": league_name,
            "abbreviationName": league_abbrevation_name,
            "startDate": start_date,
            "endDate": end_date,
            "season": league_season_page["year"],
            "hasGroups": league_season_page["type"]["hasGroups"],
            "hasStandings": league_season_page["type"]["hasStandings"]
        }
        return processed_data

    except KeyError as key_err:
        logger.error(f"Key not found in dictionary: {key_err}")
        raise
    except ValueError as val_err:
        logger.error(f"{val_err}")
        raise
    except DateError as date_err:
        logger.error(f"{date_err}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error has occurred: {e}")
        raise
