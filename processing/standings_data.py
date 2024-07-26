import logging
from typing import Dict, Any, Tuple
from dateutil import parser

from processing.utils import generate_deterministic_uid, get_number_field

##########################################	GLOBAL SCOPE	#######################################
# logs
logger = logging.getLogger(__name__)

##########################################	FUNCTIONS	###########################################


def process_standings_data(
    standings_pages: list[Dict[str, Any]], league_uid: str
) -> list[Dict[str, Any]]:
    """
    Processes and extracts standings data for a specific league and season.

    This function retrieves and processes standings information for each team in the league,
    including group/pool data if applicable. It handles cases where standings data might not
    be available for certain leagues or seasons.

    Args:
        standings_pages (list[Dict[str, Any]]): A list of dictionaries containing standing page data
        for each group of a league. Standing page containing url to each team's page of a league.

    Returns:
        list[Dict[str, Any]]: A list of dictionaries, each containing processed standing 
        information for a team. Each dictionary is structured as follows:
        {
            "uid": str,                  # Unique identifier for this standing entry
            "teamEspnId": int,           # ESPN ID of the team
            "leagueUid": str,            # Unique identifier of the league
            "groupId": int,              # ID of the group/pool (if applicable)
            "OTLosses": float,           # Overtime losses
            "OTWins": float,             # Overtime wins
            "avgPointsAgainst": float,   # Average points conceded per game
            "avgPointsFor": float,       # Average points scored per game
            "differential": float,       # Point differential
            "divisionWinPercent": float, # Win percentage within division
            "gamesBehind": float,        # Games behind the leader
            "gamesPlayed": float,        # Total games played
            "leagueWinPercent": float,   # Win percentage in the league
            "gamesLost": float,          # Number of games lost
            "playoffSeed": float,        # Playoff seeding
            "pointsDifference": float,   # Total point difference
            "points": float,             # Total points
            "pointsAgainst": float,      # Total points conceded
            "pointsFor": float,          # Total points scored
            "streak": float,             # Current streak
            "gamesDrawn": float,         # Number of games drawn
            "winPercent": float,         # Overall win percentage
            "gamesWon": float,           # Number of games won
            "bonusPoints": float,        # Bonus points
            "gamesBye": float,           # Number of bye games
            "bonusPointsLosing": float,  # Bonus points from losses
            "rank": float,               # Team's rank in standings
            "triesAgainst": float,       # Tries conceded
            "bonusPointsTry": float,     # Bonus points from tries
            "triesDifference": float,    # Difference in tries scored and conceded
            "triesFor": float            # Tries scored
        }
        Note: Some fields may be absent if not applicable to the specific league or season.

    Raises:
        KeyError: If required keys are missing from the scraped standings data.
        Exception: For any unexpected errors during the scraping or processing of standings data.

    Note:
        - This function relies on external scraping functions to fetch raw data from ESPN.
        - It handles cases where standings data might not be available (e.g., for rugby 7s).
        - The function generates a unique identifier (UID) for each standing entry.
    """

    try:
        standings_data = []
        for page in standings_pages:

            group_id = get_number_field(page["$ref"], 3)

            for standing in page["standings"] : 
               
                team_espn_id = get_number_field(standing["team"]["$ref"], -1)

                # Create standing header for each team
                standing_data = {
                    "uid": generate_deterministic_uid([league_uid, team_espn_id]),
                    "teamEspnId": team_espn_id,
                    "leagueUid": league_uid,
                    "groupId": group_id,
                }

                # Get standings stats for each team
                standing_stats = standing["records"][0]["stats"]
                for standing_stat in standing_stats:
                    stat = {standing_stat["name"]: standing_stat["value"]}
                    standing_data.update(stat)

                standings_data.append(standing_data)

        return standings_data

    except KeyError as key_err:
        logger.error(f"Key not found in dictionary: {key_err}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error has occurred: {e}")
        raise
