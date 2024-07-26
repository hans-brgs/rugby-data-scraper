import logging
from typing import Dict, Any

from scraping.utils import ParsingError, ScrappingError, parse_urls, scrape_api_request, scrape_url


##########################################	GLOBAL SCOPE	#######################################
# logs
logger = logging.getLogger(__name__)

##########################################	FUNCTIONS	###########################################

def scrape_group_pages(espn_id_league: int, season_year: int) -> list[Dict[str, Any]]:
    """
    Scrapes group pages for a specific league and season from the ESPN API.

    This function retrieves group URLs for a given league and season, then scrapes the individual
    group pages. It's particularly useful for leagues that have multiple groups or pools.

    Args:
        espn_id_league (int): The ESPN ID of the league.
        season_year (int): The year of the season to scrape.

    Returns:
        list[Dict[str, Any]]: A list of dictionaries, each containing data for a single group page.

    Raises:
        ScrappingError: If there's an error during the scraping process.
        ParsingError: If there's an error parsing the scraped data.
        Exception: For any unexpected errors during the scraping process.

    Note:
        This function relies on external functions for API requests and URL parsing.
    """
    try:
        group_urls_page = scrape_api_request(
            "group_urls",
            url_params={
                "id_league": espn_id_league,
                "season": season_year,
			}
        )
        group_urls = parse_urls(group_urls_page)
        group_pages = []
        for group_url in group_urls : 
            group_pages.append(scrape_url(group_url))
        return group_pages
    except ScrappingError:
        logger.error(f"Scraping error.")
        raise
    except ParsingError:
        logger.error(f"Parsing error.")
        raise
    except Exception as e:
        logger.error(f"An unexpected error has occurred: {e}")
        raise

def scrape_standing_pages(espn_id_league: int, season_year: int) -> list[Dict[str, Any]]:
    """
    Scrapes standing pages for a specific league and season from the ESPN API.

    This function first scrapes group pages to check if the league has multiple groups/pools.
    It then retrieves standings for each group. If standings data is missing, it logs a warning
    and continues with the next group.

    Args:
        espn_id_league (int): The ESPN ID of the league.
        season_year (int): The year of the season to scrape.

    Returns:
        list[Dict[str, Any]]: A list of dictionaries, each containing standings data for a group.

    Raises:
        KeyError: If required keys are missing from the scraped data.
        Exception: For any unexpected errors during the scraping process.

    Note:
        This function relies on the scrape_group_pages function and external scraping functions.
    """
    try:
        # Scrape `groups` to check whether the league is a tournament with different pools/groups.
        # In this case, each standings belongs to a specific group.
        group_pages = scrape_group_pages(espn_id_league, season_year)

        standings_pages = []
        for page in group_pages:
            # Scrape standings from group page
            standings_intermediate_page = scrape_url(page["standings"]["$ref"])
            standings_page = scrape_url(standings_intermediate_page["items"][0]["$ref"])
            # Check if standing exist, if None continue
            if standings_page.get("standings") is None :
                logger.warning(f"Standings data missing in ESPN database for league {espn_id_league} and season {season_year}.")
                continue
            standings_pages.append(standings_page)
        return standings_pages
    except KeyError as key_err:
        logger.error(f"Key not found in dictionary: {key_err}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error has occurred: {e}")
        raise