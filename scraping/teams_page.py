import logging
from typing import Dict, Any

from scraping.utils import ParsingError, ScrappingError, parse_urls, scrape_api_request, scrape_url


##########################################	GLOBAL SCOPE	#######################################
# logs
logger = logging.getLogger(__name__)

##########################################	FUNCTIONS	###########################################

def scrape_team_pages(espn_id_league: int, season_year: int, limit : int = 200) -> list[Dict[str, Any]]:
    """
    Scrapes team pages for a specific league and season from the ESPN API.

    This function retrieves team URLs for a given league and season, then scrapes the individual
    team pages.

    Args:
        espn_id_league (int): The ESPN ID of the league.
        season_year (int): The year of the season to scrape.
        limit (int, optional): The maximum number of team URLs to retrieve. Defaults to 200.

    Returns:
        list[Dict[str, Any]]: A list of dictionaries, each containing data for a single team page.

    Raises:
        ScrappingError: If there's an error during the scraping process.
        ParsingError: If there's an error parsing the scraped data.
        Exception: For any unexpected errors during the scraping process.

    Note:
        This function relies on external functions for API requests and URL parsing.
    """
    try:
        team_urls_page = scrape_api_request(
            "team_urls",
            url_params={
                "id_league": espn_id_league,
                "season": season_year,
            },
            query_params= {"limit": limit}
        )
        team_urls = parse_urls(team_urls_page)
        team_pages = []
        for team_url in team_urls : 
            team_pages.append(scrape_url(team_url))
        return team_pages
    except ScrappingError:
        logger.error(f"Scraping error.")
        raise
    except ParsingError:
        logger.error(f"Parsing error.")
        raise
    except Exception as e:
        logger.error(f"An unexpected error has occurred: {e}")
        raise