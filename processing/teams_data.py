import logging
from typing import Dict, Any
import re

from processing.utils import get_number_field
from scraping.standings_page import scrape_group_pages
from scraping.teams_page import scrape_team_pages
from scraping.utils import scrape_url

##########################################	GLOBAL SCOPE	#######################################
# logs
logger = logging.getLogger(__name__)

##########################################	FUNCTIONS	###########################################

def process_teams_data(standings_pages: list[Dict[str, Any]]) -> list[Dict[str, Any]]:
    """
    Processes and extracts team data for a specific league and season.

    This function retrieves team information pages for a given league and season,
    then extracts relevant data for each team, including their ESPN ID, name,
    and abbreviation.

    Args:
        standings_pages (list[Dict[str, Any]]): A list of dictionaries containing standing page data
        for each group of a league. Standing page containing url to each team's page of a league.

    Returns:
        list[Dict[str, Any]]: A list of dictionaries, each containing data for a single team.
        Each dictionary has the following structure:
        {
            "espnId": int,              # The ESPN ID of the team
            "name": str,                # The full name of the team
            "abbreviationName": str     # The abbreviated name of the team
            "color": str                # Main color representing team identity
            "logoUrl": str              # url of logo image
        }

    Raises:
        KeyError: If required keys are missing from the scraped team data.
        Exception: For any unexpected errors during the scraping or processing of team data.

    Note:
        This function relies on an external 'scrape_standings_pages' function to fetch
        the raw team data from ESPN.
        "http://sports.core.api.espn.com/v2/sports/rugby/leagues/282/teams".
        However, please be aware that for some leagues and seasons, the teams referenced on this page 
        may not correspond accurately to the actual league and season due to known issues in the ESPN database.
        For this reason, we have chosen to retrieve data from the standings page, 
        which has proven to be more reliable based on our experience.
    """
    try:
        teams_data = []
        # Browse all standings page for each group in the tournament or league.
        for standings_page in standings_pages:
            # Get standigs information for each team
            for standing in standings_page["standings"]:
                # Scrape team URL
                team_page = scrape_url(standing["team"]["$ref"])

                # Get logos data if exist
                if team_page["logos"] == [] :
                    logo_url = None
                else :
                    logo_url = team_page["logos"][0]["href"]

                team_data = {
                    "espnId": int(team_page["id"]),
                    "name": team_page["name"],
                    "abbreviationName": team_page["abbreviation"],
                    "color": team_page["color"],
                    "logoUrl": logo_url
                }

                teams_data.append(team_data)
        return teams_data
    except KeyError as key_err:
        logger.error(f"Dict parse KeyError: {key_err}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error has occurred: {e}")
        raise

