from ast import Tuple

import logging
from typing import Dict, Any, Tuple

from processing.utils import (
    convert_inches_to_meters,
    convert_lbs_to_kg,
    extract_stats,
    generate_deterministic_uid,
    get_number_field,
    convert_date_time_to_MySQL,
)
from scraping.utils import scrape_url

##########################################	GLOBAL SCOPE	#######################################
# logs
logger = logging.getLogger(__name__)

player_position_map = {
    0: "default",
    1: "fullback",
    2: "wing",
    3: "centre",
    4: "fly-half",
    5: "scrum-half",
    6: "prop",
    7: "hooker",
    8: "lock",
    9: "flanker",
    10: "no. 8",
    20: "replacement",
    30: "back",
    31: "utility back",
    32: "three-quarters",
    33: "extra back",
    34: "outside back",
    35: "five-eighth",
    36: "outside-half",
    37: "halfback",
    38: "inside-half",
    40: "forward",
    41: "utility forward",
    42: "front-row",
    43: "second-row",
    44: "wing-forward",
    45: "back-row",
    46: "forwards",
    47: "backs",
    48: "tight-five",
    49: "loose-forwards",
    50: "full-back",
    51: "three-quarters",
    52: "halves",
    53: "reserve",
}

##########################################	FUNCTIONS	###########################################


def process_players_data(roster_pages: list[Dict[str, Any]]) -> list[Dict[str, Any]]:
    """
    Processes player data from a list of roster pages and returns a list of player information.

    This function extracts detailed player information from roster pages, including personal details
    and physical attributes. It handles duplicate players and converts measurements to metric units.

    Args:
        roster_pages (list[Dict[str, Any]]): A list of dictionaries containing roster page data.

    Returns:
        list[Dict[str, Any]]: A list of dictionaries, each containing data for a single player.
        Each dictionary has the following structure:
        {
            "espnId": int,              # ESPN ID of the player
            "firstName": str,           # Player's first name
            "lastName": str,            # Player's last name
            "weight": float or None,    # Player's weight in kg (if available)
            "height": float or None,    # Player's height in meters (if available)
            "birthDate": str,           # Player's birth date in MySQL format
            "birthPlace": str or None,  # Player's birth country (if available)
            "positionName": str         # Player's position name
        }

    Raises:
        KeyError: If required keys are missing from the roster page data.
        Exception: For any unexpected errors during the processing of player data.

    Note:
        - This function uses external functions for unit conversion and date formatting.
        - It skips duplicate players based on their ESPN ID.
    """
    if roster_pages == []:
        raise ValueError(f"Roster pages is empty.")

    players_data: list[Dict[str, Any]] = []
    players_id = set()

    try:
        for page in roster_pages:
            # Get Competitors
            entries = page["entries"]
            for entry in entries:
                athlete_espn_id = int(entry["playerId"])

                # Skip on duplicate athlete
                if athlete_espn_id in players_id:
                    continue

                athlete_page = scrape_url(entry["athlete"]["$ref"])

                # Get birth place
                birth_place = athlete_page.get("birthPlace", {}).get("country", None)

                # Get birth date
                birth_date = (
                    convert_date_time_to_MySQL(athlete_page["dateOfBirth"])
                    if "dateOfBirth" in athlete_page
                    else None
                )

                # Get Weight and Height
                weight = (
                    convert_lbs_to_kg(athlete_page["weight"])
                    if "weight" in athlete_page
                    else None
                )
                height = (
                    convert_inches_to_meters(athlete_page["height"])
                    if "height" in athlete_page
                    else None
                )

                # Get position
                position_name = athlete_page.get("position", {}).get("name", None)

                # fill the table pattern
                player_data = {
                    "espnId": athlete_espn_id,
                    "firstName": athlete_page["firstName"],
                    "lastName": athlete_page["lastName"],
                    "weight": weight,
                    "height": height,
                    "birthDate": birth_date,
                    "birthPlace": birth_place,
                    "positionName": position_name,
                }
                players_data.append(player_data)
                players_id.add(athlete_espn_id)

    except KeyError as key_err:
        logger.error(f"Dict parse KeyError: {key_err}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error has occurred: {e}")
        raise

    return players_data


# --------------------------------------------------------------------------------------------------


def process_player_match_stats_data(
    roster_pages: list[Dict[str, Any]], season_year: int
) -> Tuple[list[Dict[str, Any]], list[Dict[str, Any]]]:
    """
    Processes player match statistics data from roster pages for a specific season.

    This function extracts player-team associations and detailed match statistics for each player,
    generating unique identifiers for player-team and player-match combinations.

    Args:
        roster_pages (list[Dict[str, Any]]): A list of dictionaries containing roster page data.
        season_year (int): The year of the season for which the data is being processed.

    Returns:
        players_teams_data list[Dict[str, Any]]] : Player-team table associations containing :
           [
               {
                   "uid": str,          # Unique identifier for player-team combination
                   "playerEspnId": int, # ESPN ID of the player
                   "teamEspnId": int,   # ESPN ID of the team
                   "season": int        # Season year
               },
               ...
           ]
        players_teams_stat list[Dict[str, Any]]] : Player-match statistiques table containing :
           [
               {
                   "uid": str,          # Unique identifier for player-match combination
                   "playerTeamUid": str,# Unique identifier for player-team combination
                   "matchEspnId": int,  # ESPN ID of the match
                   "jersey": int,       # Player's jersey number
                   "positionName": str, # Player's position name
                   "isFirstChoice": bool, # Whether the player is a first-choice player
                   ... # Additional match statistics
               },
               ...
           ]

    Raises:
        KeyError: If required keys are missing from the roster page data.
        ValueError: If there's an issue with value conversion or processing.
        Exception: For any unexpected errors during the processing of data.

    Note:
        - This function uses external functions for generating UIDs and extracting statistics.
        - It handles duplicate player-team combinations by including them only once.
    """

    if roster_pages == []:
        raise ValueError(f"Roster pages is empty.")

    players_teams_data: list[Dict[str, Any]] = []
    players_matches_stat: list[Dict[str, Any]] = []
    players_teams_uid = set()
    try:

        for page in roster_pages:
            # get team & match id
            team_espn_id = get_number_field(page["$ref"], 3)
            match_espn_id = get_number_field(page["$ref"], 1)

            entries = page["entries"]
            for entry in entries:
                # get player id and compute unique player_team and player_match id
                player_espn_id = int(entry["playerId"])
                player_team_uid = generate_deterministic_uid(
                    [team_espn_id, player_espn_id, season_year]
                )
                player_match_uid = generate_deterministic_uid(
                    [player_team_uid, match_espn_id]
                )

                # Get position data
                jersey = int(entry["jersey"])
                position_id = get_number_field(entry["position"]["$ref"], 0)
                poisition_name = player_position_map[position_id]

                # starter
                is_first_choice = True if jersey <= 15 or position_id < 20 else False

                # fill the table pattern
                player_team_data = {
                    "uid": player_team_uid,
                    "playerEspnId": player_espn_id,
                    "teamEspnId": team_espn_id,
                    "season": season_year,
                }
                player_match_data = {
                    "uid": player_match_uid,
                    "playerTeamUid": player_team_uid,
                    "matchEspnId": match_espn_id,
                    "jersey": jersey,
                    "positionName": poisition_name,
                    "isFirstChoice": is_first_choice,
                }
                # Check if Statistic exist
                stat_url = entry.get("statistics", {}).get("$ref", None)
                if stat_url is None:
                    player_match_stat = player_match_data
                    logger.warning(
                        f"Player statistics missing in ESPN database for match id '{match_espn_id}' and player id `{player_espn_id}`."
                    )
                else:
                    player_match_stat = player_match_data | extract_stats(stat_url)

                # Concat
                # Skip on duplicate athlete
                if not player_team_uid in players_teams_uid:
                    players_teams_data.append(player_team_data)
                    players_teams_uid.add(player_team_uid)

                players_matches_stat.append(player_match_stat)

    except KeyError as key_err:
        logger.error(f"Dict parse KeyError: {key_err}")
        raise
    except ValueError as val_err:
        logger.error(f"ValueError : {val_err}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error has occurred: {e}")
        raise

    return players_teams_data, players_matches_stat
