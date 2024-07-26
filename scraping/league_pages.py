import logging
from typing import Dict, Any

from scraping.utils import ParsingError, ScrappingError, parse_urls, scrape_api_request, scrape_url


##########################################	GLOBAL SCOPE	#######################################
# logs
logger = logging.getLogger(__name__)

##########################################	FUNCTIONS	###########################################

def scrape_league_pages(limit: int = 1000) -> list[Dict[str, Any]]:
    """
    Scrapes league pages from the ESPN API.

    This function retrieves league URLs and then scrapes individual league pages.
    It handles pagination through the 'limit' parameter.

    Args:
        limit (int, optional): The maximum number of league URLs to retrieve. Defaults to 1000.

    Returns:
        list[Dict[str, Any]]: A list of dictionaries, each containing data for a single league page.

    Raises:
        ScrappingError: If there's an error during the scraping process.
        ParsingError: If there's an error parsing the scraped data.
        Exception: For any unexpected errors during the scraping process.

    Note:
        This function relies on external functions for API requests and URL parsing.
    """
    try:
        league_urls_page = scrape_api_request(
            "league_urls",
            query_params={"limit": limit}
        )
        league_urls = parse_urls(league_urls_page)
        leagues_page = []
        for league_url in league_urls : 
            leagues_page.append(scrape_url(league_url))
        return leagues_page
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

def scrape_league_season_urls_page(espn_id_league: int, limit: int = 1000) -> Dict[str, Any]:
    """
    Scrapes a page containing league season URLs for a specific league from the ESPN API.

    This function retrieves a page with URLs for different seasons of a given league.
    It handles pagination through the 'limit' parameter.

    Args:
        espn_id_league (int): The ESPN ID of the league.
        limit (int, optional): The maximum number of season URLs to retrieve. Defaults to 1000.

    Returns:
        Dict[str, Any]: A dictionary containing the league season URLs page data.

    Raises:
        ScrappingError: If there's an error during the scraping process.
        ParsingError: If there's an error parsing the scraped data.
        Exception: For any unexpected errors during the scraping process.

    Note:
        This function relies on external functions for API requests.
    """
    try:
        league_season_urls_page = scrape_api_request(
            "league_season_urls",
            url_params={"id_league": espn_id_league},
            query_params={"limit": limit}
        )
        return league_season_urls_page
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

def scrape_league_page(espn_id_league: int) -> Dict[str, Any]:
    """
    Scrapes a league information page for a specific league from the ESPN API.

    This function retrieves detailed information about a given league.

    Args:
        espn_id_league (int): The ESPN ID of the league.

    Returns:
        Dict[str, Any]: A dictionary containing the league information.

    Raises:
        ScrappingError: If there's an error during the scraping process.
        Exception: For any unexpected errors during the scraping process.

    Note:
        This function relies on external functions for API requests.
    """
    try:
        league_page = scrape_api_request(
            "league_info",
            url_params={"id_league": espn_id_league}
            )
        return league_page
    except ScrappingError:
        logger.error(f"Scraping error.")
        raise
    except Exception as e:
        logger.error(f"An unexpected error has occurred: {e}")
        raise

#--------------------------------------------------------------------------------------------------

def scrape_league_season_page(espn_id_league: int, season_year: int) -> Dict[str, Any]:
    """
    Scrapes a league season information page for a specific league and season from the ESPN API.

    This function retrieves detailed information about a given league for a specific season.

    Args:
        espn_id_league (int): The ESPN ID of the league.
        season_year (int): The year of the season to scrape.

    Returns:
        Dict[str, Any]: A dictionary containing the league season information.

    Raises:
        ScrappingError: If there's an error during the scraping process.
        Exception: For any unexpected errors during the scraping process.

    Note:
        This function relies on external functions for API requests.
    """
    try:
        league_season_page = scrape_api_request(
            "league_season_info",
            url_params={
                "id_league": espn_id_league,
                "season": season_year,
            }
            )
        return league_season_page
    except ScrappingError:
        logger.error(f"Scraping error.")
        raise
    except Exception as e:
        logger.error(f"An unexpected error has occurred: {e}")
        raise

#--------------------------------------------------------------------------------------------------

def scrape_calendar_page(espn_id_league: int, season_year: int) -> Dict[str, Any]:
    """
    Scrapes a calendar page for a specific league and season from the ESPN API.

    This function retrieves the calendar information for a given league and season.

    Args:
        espn_id_league (int): The ESPN ID of the league.
        season_year (int): The year of the season to scrape.

    Returns:
        Dict[str, Any]: A dictionary containing the calendar information.

    Raises:
        ScrappingError: If there's an error during the scraping process.
        Exception: For any unexpected errors during the scraping process.

    Note:
        This function relies on external functions for API requests.
    """
    try:
        calendar_page = scrape_api_request(
            "league_calendar_by_season",
            url_params={
                "id_league": espn_id_league,
                "season": season_year}
            )
        return calendar_page
    except ScrappingError:
        logger.error(f"Scraping error.")
        raise
    except Exception as e:
        logger.error(f"An unexpected error has occurred: {e}")
        raise