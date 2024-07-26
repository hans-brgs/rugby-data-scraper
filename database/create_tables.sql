DROP DATABASE IF EXISTS rugby_db;
CREATE DATABASE IF NOT EXISTS rugby_db;
USE rugby_db;
-- Create tables if they don't exist
CREATE TABLE IF NOT EXISTS LEAGUES (
   `uid` VARCHAR(16) PRIMARY KEY,
   espnId INT NOT NULL,
   `name` VARCHAR(100) NOT NULL,
   abbreviationName VARCHAR(50) NOT NULL,
   season YEAR NOT NULL,
   startDate DATETIME,
   endDate DATETIME,
   hasGroups BOOLEAN,
   hasStandings BOOLEAN,
   UNIQUE (espnId, season)
);
CREATE TABLE IF NOT EXISTS STADIUMS (
   espnId INT PRIMARY KEY,
   `name` VARCHAR(100) NOT NULL,
   grass BOOLEAN,
   indoor BOOLEAN,
   city VARCHAR(100),
   `state` VARCHAR(100)
   -- I removed the UNIQUE constraint on `name`,*
   -- because in the ESPN database there are duplicate stadiums with different unique `espnId`.
);
CREATE TABLE IF NOT EXISTS TEAMS (
   espnId INT PRIMARY KEY,
   `name` VARCHAR(100) NOT NULL,
   abbreviationName VARCHAR(50) NOT NULL,
   color VARCHAR(16),
   logoUrl VARCHAR(100),
   UNIQUE(`name`)
);
CREATE TABLE IF NOT EXISTS STANDINGS (
   `uid` VARCHAR(16) PRIMARY KEY,
   teamEspnId INT NOT NULL,
   leagueUid VARCHAR(16) NOT NULL,
   groupId INT,
   gamesPlayed DECIMAL(8,3),
   gamesWon DECIMAL(8,3),
   gamesLost DECIMAL(8,3),
   gamesDrawn DECIMAL(8,3),
   gamesBye DECIMAL(8,3),
   OTWins DECIMAL(8,3),
   OTLosses DECIMAL(8,3),
   points DECIMAL(8,3),
   pointsFor DECIMAL(8,3),
   pointsAgainst DECIMAL(8,3),
   pointsDifference DECIMAL(8,3),
   avgPointsFor DECIMAL(8,3),
   avgPointsAgainst DECIMAL(8,3),
   `differential` DECIMAL(8,3),
   triesFor DECIMAL(8,3),
   triesAgainst DECIMAL(8,3),
   triesDifference DECIMAL(8,3),
   `rank` DECIMAL(8,3),
   playoffSeed DECIMAL(8,3),
   winPercent DECIMAL(8,3),
   divisionWinPercent DECIMAL(8,3),
   leagueWinPercent DECIMAL(8,3),
   gamesBehind DECIMAL(8,3),
   bonusPoints DECIMAL(8,3),
   bonusPointsTry DECIMAL(8,3),
   bonusPointsLosing DECIMAL(8,3),
   streak DECIMAL(8,3),
   UNIQUE (teamEspnId, leagueUid),
   FOREIGN KEY (teamEspnId) REFERENCES TEAMS(espnId),
   FOREIGN KEY (leagueUid) REFERENCES LEAGUES(`uid`) -- Not the espn ID, the unique league Id By Season
);
CREATE TABLE IF NOT EXISTS MATCHES (
   espnId INT PRIMARY KEY,
   `date` DATETIME NOT NULL,
   `name` VARCHAR(255) NOT NULL,
   abbreviationName VARCHAR(50) NOT NULL,
   leagueUid VARCHAR(16),
   homeTeamEspnId INT,
   awayTeamEspnId INT,
   winnerEspnId INT,
   loserEspnId INT,
   stadiumEspnId INT,
   winnerScore INT,
   loserScore INT,
   totalPlayTime DECIMAL(8,3),
   -- unit in seconds
   UNIQUE(`date`, `name`),
   FOREIGN KEY (leagueUid) REFERENCES LEAGUES(`uid`),
   -- Not the espn ID, the unique league Id By Season
   FOREIGN KEY (homeTeamEspnId) REFERENCES TEAMS(espnId),
   FOREIGN KEY (awayTeamEspnId) REFERENCES TEAMS(espnId),
   FOREIGN KEY (winnerEspnId) REFERENCES TEAMS(espnId),
   FOREIGN KEY (loserEspnId) REFERENCES TEAMS(espnId),
   FOREIGN KEY (stadiumEspnId) REFERENCES STADIUMS(espnId)
);
-- Junction table (many-to-many)
CREATE TABLE IF NOT EXISTS TEAM_MATCH_STATS (
   `uid` VARCHAR(16) PRIMARY KEY,
   matchEspnId INT NOT NULL,
   teamEspnId INT NOT NULL,
   opponentEspnId INT,
   linescore1stHalf INT,
   linescore2ndHalf INT,
   linescore20min INT,
   linescore60min INT,
   -- Offensive Stats
   passes DECIMAL(8,3),
   runs DECIMAL(8,3),
   metres DECIMAL(8,3),
   attackingKicks DECIMAL(8,3),
   offload DECIMAL(8,3),
   cleanBreaks DECIMAL(8,3),
   defendersBeaten DECIMAL(8,3),
   breakAssist DECIMAL(8,3),
   carriesMetres DECIMAL(8,3),
   carriesCrossedGainLine DECIMAL(8,3),
   carriesNotMadeGainLine DECIMAL(8,3),
   carriesSupport DECIMAL(8,3),
   averageGain DECIMAL(8,3),
   dummyHalfMetres DECIMAL(8,3),
   hitUps DECIMAL(8,3),
   hitUpMetres DECIMAL(8,3),
   runFromDummyHalf DECIMAL(8,3),
   tackleBusts DECIMAL(8,3),
   attackingEventsZoneA DECIMAL(8,3),
   attackingEventsZoneB DECIMAL(8,3),
   attackingEventsZoneC DECIMAL(8,3),
   attackingEventsZoneD DECIMAL(8,3),
   completeSets DECIMAL(8,3),
   incompleteSets DECIMAL(8,3),
   -- Defensive Stats
   tackles DECIMAL(8,3),
   tackleSuccess DECIMAL(8,3),
   missedTackles DECIMAL(8,3),
   turnoverWon DECIMAL(8,3),
   turnoversConceded DECIMAL(8,3),
   turnoverOppHalf DECIMAL(8,3),
   turnoverOwnHalf DECIMAL(8,3),
   turnoverLostInRuckOrMaul DECIMAL(8,3),
   turnoverKnockOn DECIMAL(8,3),
   turnoverForwardPass DECIMAL(8,3),
   turnoverCarriedInTouch DECIMAL(8,3),
   turnoverCarriedOver DECIMAL(8,3),
   turnoverKickError DECIMAL(8,3),
   turnoverBadPass DECIMAL(8,3),
   markerTackles DECIMAL(8,3),
   ballWonZoneA DECIMAL(8,3),
   ballWonZoneB DECIMAL(8,3),
   ballWonZoneC DECIMAL(8,3),
   ballWonZoneD DECIMAL(8,3),
   -- Scoring Stats
   points DECIMAL(8,3),
   tries DECIMAL(8,3),
   penaltyTries DECIMAL(8,3),
   tryAssists DECIMAL(8,3),
   tryBonusPoints DECIMAL(8,3),
   losingBonusPoints DECIMAL(8,3),
   conversionGoals DECIMAL(8,3),
   dropGoalsConverted DECIMAL(8,3),
   dropGoalMissed DECIMAL(8,3),
   goals DECIMAL(8,3),
   missedConversionGoals DECIMAL(8,3),
   missedGoals DECIMAL(8,3),
   penaltyGoals DECIMAL(8,3),
   missedPenaltyGoals DECIMAL(8,3),
   -- Discipline Stats
   freeKickConcededAtLineout DECIMAL(8,3),
   freeKickConcededAtScrum DECIMAL(8,3),
   freeKickConcededInGeneralPlay DECIMAL(8,3),
   freeKickConcededInRuckOrMaul DECIMAL(8,3),
   freeKickConceded DECIMAL(8,3),
   penaltiesConceded DECIMAL(8,3),
   penaltyConcededCollapsingMaul DECIMAL(8,3),
   penaltyConcededCollapsingOffense DECIMAL(8,3),
   penaltyConcededCollapsing DECIMAL(8,3),
   penaltyConcededDelibKnockOn DECIMAL(8,3),
   penaltyConcededDissent DECIMAL(8,3),
   penaltyConcededEarlyTackle DECIMAL(8,3),
   penaltyConcededFoulPlay DECIMAL(8,3),
   penaltyConcededHandlingInRuck DECIMAL(8,3),
   penaltyConcededHighTackle DECIMAL(8,3),
   penaltyConcededKillingRuck DECIMAL(8,3),
   penaltyConcededLineoutOffence DECIMAL(8,3),
   penaltyConcededObstruction DECIMAL(8,3),
   penaltyConcededOffside DECIMAL(8,3),
   penaltyConcededOppHalf DECIMAL(8,3),
   penaltyConcededOther DECIMAL(8,3),
   penaltyConcededOwnHalf DECIMAL(8,3),
   penaltyConcededScrumOffence DECIMAL(8,3),
   penaltyConcededStamping DECIMAL(8,3),
   penaltyConcededWrongSide DECIMAL(8,3),
   totalFreeKicksConceded DECIMAL(8,3),
   onReport DECIMAL(8,3),
   redCards DECIMAL(8,3),
   yellowCards DECIMAL(8,3),
   -- Kicking Stats
   kicks DECIMAL(8,3),
   kickFromHandMetres DECIMAL(8,3),
   kicksFromHand DECIMAL(8,3),
   kickChargedDown DECIMAL(8,3),
   tryKicks DECIMAL(8,3),
   kickTryScored DECIMAL(8,3),
   kickOutOfPlay DECIMAL(8,3),
   kickInTouch DECIMAL(8,3),
   kickOppnCollection DECIMAL(8,3),
   kickPossessionLost DECIMAL(8,3),
   kickPossessionRetained DECIMAL(8,3),
   kickTouchInGoal DECIMAL(8,3),
   kickPenaltyBad DECIMAL(8,3),
   kickPenaltyGood DECIMAL(8,3),
   totalKicks DECIMAL(8,3),
   totalKicksSucceeded DECIMAL(8,3),
   kickPercentSuccess DECIMAL(8,3),
   pcKickPercent DECIMAL(8,3),
   kickSuccess DECIMAL(8,3),
   kickReturns DECIMAL(8,3),
   kickReturnMetres DECIMAL(8,3),
   fortyTwenty DECIMAL(8,3),
   penaltyKickForTouchMetres DECIMAL(8,3),
   -- Possession and Control Stats
   ballPossessionLast10Mins DECIMAL(8,3),
   pcPossessionFirst DECIMAL(8,3),
   pcPossessionSecond DECIMAL(8,3),
   pcTerritoryFirst DECIMAL(8,3),
   pcTerritorySecond DECIMAL(8,3),
   possession DECIMAL(8,3),
   territory DECIMAL(8,3),
   territoryLast10Mins DECIMAL(8,3),
   collectionFailed DECIMAL(8,3),
   collectionFromKick DECIMAL(8,3),
   collectionInterception DECIMAL(8,3),
   collectionLooseBall DECIMAL(8,3),
   collectionSuccess DECIMAL(8,3),
   retainedKicks DECIMAL(8,3),
   trueRetainedKicks DECIMAL(8,3),
   restart22m DECIMAL(8,3),
   restartErrorNotTen DECIMAL(8,3),
   restartErrorOutOfPlay DECIMAL(8,3),
   restartHalfway DECIMAL(8,3),
   restartOppError DECIMAL(8,3),
   restartOppPlayer DECIMAL(8,3),
   restartOwnPlayer DECIMAL(8,3),
   restartsLost DECIMAL(8,3),
   restartsSuccess DECIMAL(8,3),
   restartsWon DECIMAL(8,3),
   handlingError DECIMAL(8,3),
   phaseNumber DECIMAL(8,3),
   playTheBall DECIMAL(8,3),
   -- Set Pieces Stats
   scrumsWonFreeKick DECIMAL(8,3),
   scrumsWonOutright DECIMAL(8,3),
   scrumsWonPenalty DECIMAL(8,3),
   scrumsWonPenaltyTry DECIMAL(8,3),
   scrumsWonPushoverTry DECIMAL(8,3),
   scrumsLostFreeKick DECIMAL(8,3),
   scrumsLostOutright DECIMAL(8,3),
   scrumsLostPenalty DECIMAL(8,3),
   scrumsLostReversed DECIMAL(8,3),
   scrumsLost DECIMAL(8,3),
   scrumsReset DECIMAL(8,3),
   scrumsSuccess DECIMAL(8,3),
   scrumsTotal DECIMAL(8,3),
   scrumsWon DECIMAL(8,3),
   lineoutsToOppPlayer DECIMAL(8,3),
   lineoutsWon DECIMAL(8,3),
   lineoutSuccess DECIMAL(8,3),
   lineoutsLost DECIMAL(8,3),
   lineoutsInfringeOpp DECIMAL(8,3),
   lineoutsInfringeOwn DECIMAL(8,3),
   lineoutThrowWonClean DECIMAL(8,3),
   lineoutThrowWonFreeKick DECIMAL(8,3),
   lineoutThrowWonPenalty DECIMAL(8,3),
   lineoutThrowWonTap DECIMAL(8,3),
   lineoutThrowLostFreeKick DECIMAL(8,3),
   lineoutThrowLostHandlingError DECIMAL(8,3),
   lineoutThrowLostNotStraight DECIMAL(8,3),
   lineoutThrowLostOutright DECIMAL(8,3),
   lineoutThrowLostPenalty DECIMAL(8,3),
   lineoutsToOwnPlayer DECIMAL(8,3),
   lineoutThrowNotStraight DECIMAL(8,3),
   lineoutWonOwnThrow DECIMAL(8,3),
   lineoutWonSteal DECIMAL(8,3),
   totalLineouts DECIMAL(8,3),
   setPieceWon DECIMAL(8,3),
   -- Ruck and Maul Stats
   rucksLost DECIMAL(8,3),
   rucksWon DECIMAL(8,3),
   rucksTotal DECIMAL(8,3),
   ruckSuccess DECIMAL(8,3),
   maulsWon DECIMAL(8,3),
   maulsLost DECIMAL(8,3),
   maulsTotal DECIMAL(8,3),
   maulsWonOutright DECIMAL(8,3),
   maulsLostOutright DECIMAL(8,3),
   maulsWonPenalty DECIMAL(8,3),
   maulsLostTurnover DECIMAL(8,3),
   maulsWonPenaltyTry DECIMAL(8,3),
   maulsWonTry DECIMAL(8,3),
   maulingMetres DECIMAL(8,3),
   -- General Stats
   matches DECIMAL(8,3),
   won DECIMAL(8,3),
   lost DECIMAL(8,3),
   drawn DECIMAL(8,3),
   numberOfTeams DECIMAL(8,3),
   startingMatches DECIMAL(8,3),
   replacementMatches DECIMAL(8,3),
   UNIQUE(matchEspnId, teamEspnId),
   FOREIGN KEY (matchEspnId) REFERENCES MATCHES(espnId),
   FOREIGN KEY (teamEspnId) REFERENCES TEAMS(espnId),
   FOREIGN KEY (opponentEspnId) REFERENCES TEAMS(espnId)
);
CREATE TABLE IF NOT EXISTS PLAYERS (
   espnId INT PRIMARY KEY,
   firstName VARCHAR(100),
   lastName VARCHAR(100),
   weight DECIMAL(8,3),
   -- Units in lb
   height DECIMAL(8,3),
   -- Units in meter
   birthDate DATE,
   birthPlace VARCHAR(100),
   -- Country
   positionName VARCHAR(50),
   UNIQUE(firstName, lastName, birthDate)
);
-- Junction table (many-to-many)
CREATE TABLE IF NOT EXISTS PLAYER_TEAM (
   `uid` VARCHAR(16) PRIMARY KEY,
   playerEspnId INT NOT NULL,
   teamEspnId INT NOT NULL,
   season YEAR,
   UNIQUE (playerEspnId, teamEspnId, season),
   FOREIGN KEY (playerEspnId) REFERENCES PLAYERS(espnId),
   FOREIGN KEY (teamEspnId) REFERENCES TEAMS(espnId)
);
-- Junction table (many-to-many)
CREATE TABLE IF NOT EXISTS PLAYER_MATCH_STATS (
   `uid` VARCHAR(16) PRIMARY KEY,
   playerTeamUid VARCHAR(16) NOT NULL,
   matchEspnId INT NOT NULL,
   jersey INT,
   positionName VARCHAR(50),
   isFirstChoice BOOLEAN,
   -- Offensive Stats
   passes DECIMAL(8,3),
   runs DECIMAL(8,3),
   metres DECIMAL(8,3),
   attackingKicks DECIMAL(8,3),
   offload DECIMAL(8,3),
   cleanBreaks DECIMAL(8,3),
   defendersBeaten DECIMAL(8,3),
   breakAssist DECIMAL(8,3),
   carriesMetres DECIMAL(8,3),
   gainLine DECIMAL(8,3),
   carriesCrossedGainLine DECIMAL(8,3),
   carriesNotMadeGainLine DECIMAL(8,3),
   carriesSupport DECIMAL(8,3),
   averageGain DECIMAL(8,3),
   dummyHalfMetres DECIMAL(8,3),
   hitUps DECIMAL(8,3),
   hitUpMetres DECIMAL(8,3),
   runFromDummyHalf DECIMAL(8,3),
   tackleBusts DECIMAL(8,3),
   -- Defensive Stats
   tackles DECIMAL(8,3),
   tackleSuccess DECIMAL(8,3),
   missedTackles DECIMAL(8,3),
   markerTackles DECIMAL(8,3),
   -- Scoring Stats
   points DECIMAL(8,3),
   tries DECIMAL(8,3),
   tryAssists DECIMAL(8,3),
   tryBonusPoints DECIMAL(8,3),
   losingBonusPoints DECIMAL(8,3),
   conversionGoals DECIMAL(8,3),
   dropGoalsConverted DECIMAL(8,3),
   dropGoalMissed DECIMAL(8,3),
   goals DECIMAL(8,3),
   missedConversionGoals DECIMAL(8,3),
   missedGoals DECIMAL(8,3),
   penaltyGoals DECIMAL(8,3),
   missedPenaltyGoals DECIMAL(8,3),
   goalsFromMark DECIMAL(8,3),
   -- Discipline Stats
   freeKickConcededAtLineout DECIMAL(8,3),
   freeKickConcededAtScrum DECIMAL(8,3),
   freeKickConcededInGeneralPlay DECIMAL(8,3),
   freeKickConcededInRuckOrMaul DECIMAL(8,3),
   penaltiesConceded DECIMAL(8,3),
   penaltyConcededCollapsingMaul DECIMAL(8,3),
   penaltyConcededCollapsingOffense DECIMAL(8,3),
   penaltyConcededDelibKnockOn DECIMAL(8,3),
   penaltyConcededDissent DECIMAL(8,3),
   penaltyConcededEarlyTackle DECIMAL(8,3),
   penaltyConcededFoulPlay DECIMAL(8,3),
   penaltyConcededHandlingInRuck DECIMAL(8,3),
   penaltyConcededHighTackle DECIMAL(8,3),
   penaltyConcededKillingRuck DECIMAL(8,3),
   penaltyConcededLineoutOffence DECIMAL(8,3),
   penaltyConcededObstruction DECIMAL(8,3),
   penaltyConcededOffside DECIMAL(8,3),
   penaltyConcededOppHalf DECIMAL(8,3),
   penaltyConcededOther DECIMAL(8,3),
   penaltyConcededOwnHalf DECIMAL(8,3),
   penaltyConcededScrumOffence DECIMAL(8,3),
   penaltyConcededStamping DECIMAL(8,3),
   penaltyConcededWrongSide DECIMAL(8,3),
   totalFreeKicksConceded DECIMAL(8,3),
   onReport DECIMAL(8,3),
   redCards DECIMAL(8,3),
   yellowCards DECIMAL(8,3),
   -- Kicking Stats
   kicks DECIMAL(8,3),
   kickMetres DECIMAL(8,3),
   kickFromHandMetres DECIMAL(8,3),
   kicksFromHand DECIMAL(8,3),
   kickChargedDown DECIMAL(8,3),
   tryKicks DECIMAL(8,3),
   kickTryScored DECIMAL(8,3),
   kickOutOfPlay DECIMAL(8,3),
   kickInField DECIMAL(8,3),
   kickInTouch DECIMAL(8,3),
   kickOppnCollection DECIMAL(8,3),
   kickPossessionLost DECIMAL(8,3),
   kickPossessionRetained DECIMAL(8,3),
   kickTouchInGoal DECIMAL(8,3),
   kickPenaltyBad DECIMAL(8,3),
   kickPenaltyGood DECIMAL(8,3),
   kickPercentSuccess DECIMAL(8,3),
   pcKickPercent DECIMAL(8,3),
   kickReturns DECIMAL(8,3),
   kickReturnMetres DECIMAL(8,3),
   fortyTwenty DECIMAL(8,3),
   penaltyKickForTouchMetres DECIMAL(8,3),
   -- Possession and Control Stats
   collectionFailed DECIMAL(8,3),
   collectionFromKick DECIMAL(8,3),
   collectionInterception DECIMAL(8,3),
   collectionLooseBall DECIMAL(8,3),
   collectionSuccess DECIMAL(8,3),
   retainedKicks DECIMAL(8,3),
   trueRetainedKicks DECIMAL(8,3),
   restart22m DECIMAL(8,3),
   restartErrorNotTen DECIMAL(8,3),
   restartErrorOutOfPlay DECIMAL(8,3),
   restartHalfway DECIMAL(8,3),
   restartOppError DECIMAL(8,3),
   restartOppPlayer DECIMAL(8,3),
   restartOwnPlayer DECIMAL(8,3),
   restartsLost DECIMAL(8,3),
   restartsSuccess DECIMAL(8,3),
   restartsWon DECIMAL(8,3),
   handlingError DECIMAL(8,3),
   droppedCatch DECIMAL(8,3),
   badPasses DECIMAL(8,3),
   ballOutOfPlay DECIMAL(8,3),
   pickup DECIMAL(8,3),
   catchFromKick DECIMAL(8,3),
   turnoverWon DECIMAL(8,3),
   turnoversConceded DECIMAL(8,3),
   turnoverOppHalf DECIMAL(8,3),
   turnoverOwnHalf DECIMAL(8,3),
   turnoverLostInRuckOrMaul DECIMAL(8,3),
   turnoverKnockOn DECIMAL(8,3),
   turnoverForwardPass DECIMAL(8,3),
   turnoverCarriedInTouch DECIMAL(8,3),
   turnoverCarriedOver DECIMAL(8,3),
   turnoverKickError DECIMAL(8,3),
   turnoverBadPass DECIMAL(8,3),
   -- Set Pieces Stats
   scrumsWonFreeKick DECIMAL(8,3),
   scrumsWonOutright DECIMAL(8,3),
   scrumsWonPenalty DECIMAL(8,3),
   scrumsWonPenaltyTry DECIMAL(8,3),
   scrumsWonPushoverTry DECIMAL(8,3),
   scrumsLostFreeKick DECIMAL(8,3),
   scrumsLostOutright DECIMAL(8,3),
   scrumsLostPenalty DECIMAL(8,3),
   scrumsLostReversed DECIMAL(8,3),
   lineoutsWon DECIMAL(8,3),
   lineoutSuccess DECIMAL(8,3),
   lineoutsLost DECIMAL(8,3),
   lineoutsInfringeOpp DECIMAL(8,3),
   lineoutThrowWonClean DECIMAL(8,3),
   lineoutThrowWonFreeKick DECIMAL(8,3),
   lineoutThrowWonPenalty DECIMAL(8,3),
   lineoutThrowWonTap DECIMAL(8,3),
   lineoutThrowLostFreeKick DECIMAL(8,3),
   lineoutThrowLostHandlingError DECIMAL(8,3),
   lineoutThrowLostNotStraight DECIMAL(8,3),
   lineoutThrowLostOutright DECIMAL(8,3),
   lineoutThrowLostPenalty DECIMAL(8,3),
   lineoutsToOwnPlayer DECIMAL(8,3),
   lineoutNonStraight DECIMAL(8,3),
   lineoutWonOppThrow DECIMAL(8,3),
   lineoutWonOwnThrow DECIMAL(8,3),
   lineoutWonSteal DECIMAL(8,3),
   totalLineouts DECIMAL(8,3),
   -- Ruck and Maul Stats
   rucksLost DECIMAL(8,3),
   rucksWon DECIMAL(8,3),
   maulsWon DECIMAL(8,3),
   maulsLost DECIMAL(8,3),
   maulsWonOutright DECIMAL(8,3),
   maulsLostOutright DECIMAL(8,3),
   maulsWonPenalty DECIMAL(8,3),
   maulsLostTurnover DECIMAL(8,3),
   maulsWonPenaltyTry DECIMAL(8,3),
   maulsWonTry DECIMAL(8,3),
   -- General Stats
   matches DECIMAL(8,3),
   won DECIMAL(8,3),
   lost DECIMAL(8,3),
   drawn DECIMAL(8,3),
   numberOfTeams DECIMAL(8,3),
   startingMatches DECIMAL(8,3),
   replacementMatches DECIMAL(8,3),
   mintuesPlayedBeforeFirstHalfExtra DECIMAL(8,3),
   minutesPlayedBeforeFirstHalf DECIMAL(8,3),
   minutesPlayedBeforePenaltyShootOut DECIMAL(8,3),
   minutesPlayedBeforeSecondHalfExtra DECIMAL(8,3),
   minutesPlayedBeforeSecondHalf DECIMAL(8,3),
   minutesPlayedFirstHalf DECIMAL(8,3),
   minutesPlayedFirstHalfExtra DECIMAL(8,3),
   minutesPlayedSecondHalf DECIMAL(8,3),
   minutesPlayedSecondHalfExtra DECIMAL(8,3),
   minutesPlayedTotal DECIMAL(8,3),
   UNIQUE (playerTeamUid, matchEspnId),
   FOREIGN KEY (playerTeamUid) REFERENCES PLAYER_TEAM(`uid`),
   FOREIGN KEY (matchEspnId) REFERENCES MATCHES(espnId)
);
-- ########## VIEW ##########
-- view_standings
CREATE VIEW IF NOT EXISTS view_standings AS
SELECT l.name AS leagueName,
   l.season,
   t.name,
   t.abbreviationName,
   s.gamesPlayed,
   s.gamesWon,
   s.gamesLost,
   s.gamesDrawn,
   s.gamesBye,
   s.OTWins,
   s.OTLosses,
   s.points,
   s.pointsFor,
   s.pointsAgainst,
   s.pointsDifference,
   s.avgPointsFor,
   s.differential,
   s.triesFor,
   s.triesAgainst,
   s.triesDifference,
   s.`rank`,
   s.playoffSeed,
   s.winPercent,
   s.divisionWinPercent,
   s.leagueWinPercent,
   s.gamesBehind,
   s.bonusPoints,
   s.bonusPointsTry,
   s.bonusPointsLosing,
   s.streak
FROM standings s
   JOIN leagues l ON s.leagueUid = l.uid
   JOIN teams t ON s.teamEspnId = t.espnId;
-- view_matches
CREATE VIEW IF NOT EXISTS view_matches AS
SELECT m.espnId AS matchEspnId,
   m.date AS matchDate,
   m.name AS matchName,
   m.abbreviationName AS matchAbbreviationName,
   l.name AS leagueName,
   l.season,
   homeTeam.name AS homeTeamName,
   awayTeam.name AS awayTeamName,
   winnerTeam.name AS winnerTeamName,
   loserTeam.name AS loserTeamName,
   m.winnerScore,
   m.loserScore,
   m.totalPlayTime
FROM matches m
   JOIN leagues l ON m.leagueUid = l.uid
   JOIN teams homeTeam ON m.homeTeamEspnId = homeTeam.espnId
   JOIN teams awayTeam ON m.awayTeamEspnId = awayTeam.espnId
   JOIN teams winnerTeam ON m.winnerEspnId = winnerTeam.espnId
   JOIN teams loserTeam ON m.loserEspnId = loserTeam.espnId;
-- view_team_match_stats
CREATE VIEW IF NOT EXISTS view_team_match_stats AS
SELECT m_view.leagueName,
   m_view.season,
   m_view.matchName,
   m_view.matchAbbreviationName,
   m_view.matchDate,
   team.name AS teamName,
   team.abbreviationName AS teamAbbreviationName,
   team.color AS teamColor,
   team.logoUrl AS teamLogoUrl,
   opponentTeam.name AS opponentTeamName,
   m_view.totalPlayTime,
   CASE
      WHEN team.name = m_view.winnerTeamName THEN TRUE
      ELSE FALSE
   END AS isWinner,
   CASE
      WHEN team.name = m_view.homeTeamName THEN TRUE
      ELSE FALSE
   END AS isHome,
   CASE
      WHEN team.name = m_view.winnerTeamName THEN m_view.winnerScore
      ELSE m_view.loserScore
   END AS teamScore,
   CASE
      WHEN opponentTeam.name = m_view.winnerTeamName THEN m_view.winnerScore
      ELSE m_view.loserScore
   END AS opponentTeamScore,
   tms.*
FROM team_match_stats tms
   JOIN view_matches m_view ON tms.matchEspnId = m_view.matchEspnId
   JOIN teams team ON tms.teamEspnId = team.espnId
   JOIN teams opponentTeam ON tms.opponentEspnId = opponentTeam.EspnId;
-- view_player_match_stats
CREATE VIEW IF NOT EXISTS view_player_match_stats AS
SELECT p.firstName,
   p.lastName,
   p.weight,
   p.height,
   tms_view.teamName,
   tms_view.teamAbbreviationName,
   tms_view.teamColor,
   tms_view.teamLogoUrl,
   tms_view.matchName,
   tms_view.matchDate,
   tms_view.teamScore,
   tms_view.opponentTeamScore,
   tms_view.isHome,
   tms_view.leagueName,
   tms_view.season,
   tms_view.opponentTeamName,
   pms.*
FROM player_match_stats pms
   JOIN player_team pt ON pms.playerTeamUid = pt.uid
   JOIN players p ON pt.playerEspnId = p.espnId
   JOIN view_team_match_stats tms_view ON pt.teamEspnId = tms_view.teamEspnId
   AND pms.matchEspnId = tms_view.matchEspnId;
-- TEAM_MATCH_STATS
-- view_team_match_offensive_stats
CREATE VIEW IF NOT EXISTS VIEW_TEAM_MATCH_OFFENSIVE_STATS AS
SELECT -- Informations
   `uid`,
   leagueName,
   season,
   matchName,
   matchAbbreviationName,
   matchDate,
   teamName,
   teamAbbreviationName,
   teamColor,
   teamLogoUrl,
   opponentTeamName,
   totalPlayTime,
   isWinner,
   isHome,
   teamScore,
   opponentTeamScore,
   -- Stats
   passes,
   runs,
   metres,
   attackingKicks,
   offload,
   cleanBreaks,
   defendersBeaten,
   breakAssist,
   carriesMetres,
   carriesCrossedGainLine,
   carriesNotMadeGainLine,
   carriesSupport,
   averageGain,
   dummyHalfMetres,
   hitUps,
   hitUpMetres,
   runFromDummyHalf,
   tackleBusts,
   attackingEventsZoneA,
   attackingEventsZoneB,
   attackingEventsZoneC,
   attackingEventsZoneD,
   completeSets,
   incompleteSets
FROM VIEW_TEAM_MATCH_STATS;
-- VIEW_TEAM_MATCH_DEFENSIVE_STATS
CREATE VIEW IF NOT EXISTS VIEW_TEAM_MATCH_DEFENSIVE_STATS AS
SELECT -- Informations
   `uid`,
   leagueName,
   season,
   matchName,
   matchAbbreviationName,
   matchDate,
   teamName,
   teamAbbreviationName,
   teamColor,
   teamLogoUrl,
   opponentTeamName,
   totalPlayTime,
   isWinner,
   isHome,
   teamScore,
   opponentTeamScore,
   -- Stats
   tackles,
   tackleSuccess,
   missedTackles,
   markerTackles
FROM VIEW_TEAM_MATCH_STATS;
-- VIEW_TEAM_MATCH_DEFENSIVE_STATS
CREATE VIEW IF NOT EXISTS VIEW_TEAM_MATCH_DEFENSIVE_STATS AS
SELECT -- Informations
   `uid`,
   leagueName,
   season,
   matchName,
   matchAbbreviationName,
   matchDate,
   teamName,
   teamAbbreviationName,
   teamColor,
   teamLogoUrl,
   opponentTeamName,
   totalPlayTime,
   isWinner,
   isHome,
   teamScore,
   opponentTeamScore,
   -- Stats
   points,
   tries,
   penaltyTries,
   tryAssists,
   tryBonusPoints,
   losingBonusPoints,
   conversionGoals,
   dropGoalsConverted,
   dropGoalMissed,
   goals,
   missedConversionGoals,
   missedGoals,
   penaltyGoals,
   missedPenaltyGoals
FROM VIEW_TEAM_MATCH_STATS;
-- VIEW_TEAM_MATCH_DISCIPLINE_STATS
CREATE VIEW IF NOT EXISTS VIEW_TEAM_MATCH_DISCIPLINE_STATS AS
SELECT -- Informations
   `uid`,
   leagueName,
   season,
   matchName,
   matchAbbreviationName,
   matchDate,
   teamName,
   teamAbbreviationName,
   teamColor,
   teamLogoUrl,
   opponentTeamName,
   totalPlayTime,
   isWinner,
   isHome,
   teamScore,
   opponentTeamScore,
   -- Stats
   freeKickConcededAtLineout,
   freeKickConcededAtScrum,
   freeKickConcededInGeneralPlay,
   freeKickConcededInRuckOrMaul,
   freeKickConceded,
   penaltiesConceded,
   penaltyConcededCollapsingMaul,
   penaltyConcededCollapsingOffense,
   penaltyConcededCollapsing,
   penaltyConcededDelibKnockOn,
   penaltyConcededDissent,
   penaltyConcededEarlyTackle,
   penaltyConcededFoulPlay,
   penaltyConcededHandlingInRuck,
   penaltyConcededHighTackle,
   penaltyConcededKillingRuck,
   penaltyConcededLineoutOffence,
   penaltyConcededObstruction,
   penaltyConcededOffside,
   penaltyConcededOppHalf,
   penaltyConcededOther,
   penaltyConcededOwnHalf,
   penaltyConcededScrumOffence,
   penaltyConcededStamping,
   penaltyConcededWrongSide,
   totalFreeKicksConceded,
   onReport,
   redCards,
   yellowCards
FROM VIEW_TEAM_MATCH_STATS;
-- VIEW_TEAM_MATCH_KICKING_STATS
CREATE VIEW IF NOT EXISTS VIEW_TEAM_MATCH_KICKING_STATS AS
SELECT -- Informations
   `uid`,
   leagueName,
   season,
   matchName,
   matchAbbreviationName,
   matchDate,
   teamName,
   teamAbbreviationName,
   teamColor,
   teamLogoUrl,
   opponentTeamName,
   totalPlayTime,
   isWinner,
   isHome,
   teamScore,
   opponentTeamScore,
   -- Stats
   kicks,
   kickFromHandMetres,
   kicksFromHand,
   kickChargedDown,
   tryKicks,
   kickTryScored,
   kickOutOfPlay,
   kickInTouch,
   kickOppnCollection,
   kickPossessionLost,
   kickPossessionRetained,
   kickTouchInGoal,
   kickPenaltyBad,
   kickPenaltyGood,
   totalKicks,
   totalKicksSucceeded,
   kickPercentSuccess,
   pcKickPercent,
   kickSuccess,
   kickReturns,
   kickReturnMetres,
   fortyTwenty,
   penaltyKickForTouchMetres
FROM VIEW_TEAM_MATCH_STATS;
-- VIEW_TEAM_MATCH_POSSESSION_CONTROL_STATS
CREATE VIEW IF NOT EXISTS VIEW_TEAM_MATCH_POSSESSION_CONTROL_STATS AS
SELECT -- Informations
   `uid`,
   leagueName,
   season,
   matchName,
   matchAbbreviationName,
   matchDate,
   teamName,
   teamAbbreviationName,
   teamColor,
   teamLogoUrl,
   opponentTeamName,
   totalPlayTime,
   isWinner,
   isHome,
   teamScore,
   opponentTeamScore,
   -- Stats
   ballPossessionLast10Mins,
   pcPossessionFirst,
   pcPossessionSecond,
   pcTerritoryFirst,
   pcTerritorySecond,
   possession,
   territory,
   territoryLast10Mins,
   collectionFailed,
   collectionFromKick,
   collectionInterception,
   collectionLooseBall,
   collectionSuccess,
   retainedKicks,
   trueRetainedKicks,
   restart22m,
   restartErrorNotTen,
   restartErrorOutOfPlay,
   restartHalfway,
   restartOppError,
   restartOppPlayer,
   restartOwnPlayer,
   restartsLost,
   restartsSuccess,
   restartsWon,
   handlingError,
   phaseNumber,
   playTheBall,
   turnoverWon,
   turnoversConceded,
   turnoverOppHalf,
   turnoverOwnHalf,
   turnoverLostInRuckOrMaul,
   turnoverKnockOn,
   turnoverForwardPass,
   turnoverCarriedInTouch,
   turnoverCarriedOver,
   turnoverKickError,
   turnoverBadPass,
   ballWonZoneA,
   ballWonZoneB,
   ballWonZoneC,
   ballWonZoneD
FROM VIEW_TEAM_MATCH_STATS;
-- VIEW_TEAM_MATCH_SET_PIECES_STATS
CREATE VIEW IF NOT EXISTS VIEW_TEAM_MATCH_SET_PIECES_STATS AS
SELECT -- Informations
   `uid`,
   leagueName,
   season,
   matchName,
   matchAbbreviationName,
   matchDate,
   teamName,
   teamAbbreviationName,
   teamColor,
   teamLogoUrl,
   opponentTeamName,
   totalPlayTime,
   isWinner,
   isHome,
   teamScore,
   opponentTeamScore,
   -- Stats
   scrumsWonFreeKick,
   scrumsWonOutright,
   scrumsWonPenalty,
   scrumsWonPenaltyTry,
   scrumsWonPushoverTry,
   scrumsLostFreeKick,
   scrumsLostOutright,
   scrumsLostPenalty,
   scrumsLostReversed,
   scrumsLost,
   scrumsReset,
   scrumsSuccess,
   scrumsTotal,
   scrumsWon,
   lineoutsToOppPlayer,
   lineoutsWon,
   lineoutSuccess,
   lineoutsLost,
   lineoutsInfringeOpp,
   lineoutsInfringeOwn,
   lineoutThrowWonClean,
   lineoutThrowWonFreeKick,
   lineoutThrowWonPenalty,
   lineoutThrowWonTap,
   lineoutThrowLostFreeKick,
   lineoutThrowLostHandlingError,
   lineoutThrowLostNotStraight,
   lineoutThrowLostOutright,
   lineoutThrowLostPenalty,
   lineoutsToOwnPlayer,
   lineoutThrowNotStraight,
   lineoutWonOwnThrow,
   lineoutWonSteal,
   totalLineouts,
   setPieceWon
FROM VIEW_TEAM_MATCH_STATS;
-- VIEW_TEAM_MATCH_RUCK_AND_MAUL_STATS
CREATE VIEW IF NOT EXISTS VIEW_TEAM_MATCH_RUCK_AND_MAUL_STATS AS
SELECT -- Informations
   `uid`,
   leagueName,
   season,
   matchName,
   matchAbbreviationName,
   matchDate,
   teamName,
   teamAbbreviationName,
   teamColor,
   teamLogoUrl,
   opponentTeamName,
   totalPlayTime,
   isWinner,
   isHome,
   teamScore,
   opponentTeamScore,
   -- Stats
   rucksLost,
   rucksWon,
   rucksTotal,
   ruckSuccess,
   maulsWon,
   maulsLost,
   maulsTotal,
   maulsWonOutright,
   maulsLostOutright,
   maulsWonPenalty,
   maulsLostTurnover,
   maulsWonPenaltyTry,
   maulsWonTry,
   maulingMetres
FROM VIEW_TEAM_MATCH_STATS;
-- VIEW_TEAM_MATCH_GENERAL_STATS
CREATE VIEW IF NOT EXISTS VIEW_TEAM_MATCH_GENERAL_STATS AS
SELECT -- Informations
   `uid`,
   leagueName,
   season,
   matchName,
   matchAbbreviationName,
   matchDate,
   teamName,
   teamAbbreviationName,
   teamColor,
   teamLogoUrl,
   opponentTeamName,
   totalPlayTime,
   isWinner,
   isHome,
   teamScore,
   opponentTeamScore,
   -- Stats
   matches,
   won,
   lost,
   drawn,
   numberOfTeams,
   startingMatches,
   replacementMatches
FROM VIEW_TEAM_MATCH_STATS;
-- PLAYER_MATCH_STATS
-- VIEW_PLAYER_MATCH_OFFENSIVE_STATS
CREATE VIEW IF NOT EXISTS VIEW_PLAYER_MATCH_OFFENSIVE_STATS AS
SELECT -- Informations
   `uid`,
   firstName,
   lastName,
   weight,
   height,
   teamName,
   teamAbbreviationName,
   teamColor,
   teamLogoUrl,
   matchName,
   matchDate,
   teamScore,
   opponentTeamScore,
   isHome,
   leagueName,
   season,
   opponentTeamName,
   -- Stats
   passes,
   runs,
   metres,
   attackingKicks,
   offload,
   cleanBreaks,
   defendersBeaten,
   breakAssist,
   carriesMetres,
   gainLine,
   carriesCrossedGainLine,
   carriesNotMadeGainLine,
   carriesSupport,
   averageGain,
   dummyHalfMetres,
   hitUps,
   hitUpMetres,
   runFromDummyHalf,
   tackleBusts
FROM VIEW_PLAYER_MATCH_STATS;
-- VIEW_PLAYER_MATCH_DEFENSIVE_STATS
CREATE VIEW IF NOT EXISTS VIEW_PLAYER_MATCH_DEFENSIVE_STATS AS
SELECT -- Informations
   `uid`,
   firstName,
   lastName,
   weight,
   height,
   teamName,
   teamAbbreviationName,
   teamColor,
   teamLogoUrl,
   matchName,
   matchDate,
   teamScore,
   opponentTeamScore,
   isHome,
   leagueName,
   season,
   opponentTeamName,
   -- Stats
   tackles,
   tackleSuccess,
   missedTackles,
   markerTackles
FROM VIEW_PLAYER_MATCH_STATS;
-- VIEW_PLAYER_MATCH_SCORING_STATS
CREATE VIEW IF NOT EXISTS VIEW_PLAYER_MATCH_SCORING_STATS AS
SELECT -- Informations
   `uid`,
   firstName,
   lastName,
   weight,
   height,
   teamName,
   teamAbbreviationName,
   teamColor,
   teamLogoUrl,
   matchName,
   matchDate,
   teamScore,
   opponentTeamScore,
   isHome,
   leagueName,
   season,
   opponentTeamName,
   -- Stats
   points,
   tries,
   tryAssists,
   tryBonusPoints,
   losingBonusPoints,
   conversionGoals,
   dropGoalsConverted,
   dropGoalMissed,
   goals,
   missedConversionGoals,
   missedGoals,
   penaltyGoals,
   missedPenaltyGoals,
   goalsFromMark
FROM VIEW_PLAYER_MATCH_STATS;
-- VIEW_PLAYER_MATCH_DISCIPLINE_STATS
CREATE VIEW IF NOT EXISTS VIEW_PLAYER_MATCH_DISCIPLINE_STATS AS
SELECT -- Informations
   `uid`,
   firstName,
   lastName,
   weight,
   height,
   teamName,
   teamAbbreviationName,
   teamColor,
   teamLogoUrl,
   matchName,
   matchDate,
   teamScore,
   opponentTeamScore,
   isHome,
   leagueName,
   season,
   opponentTeamName,
   -- Stats
   freeKickConcededAtLineout,
   freeKickConcededAtScrum,
   freeKickConcededInGeneralPlay,
   freeKickConcededInRuckOrMaul,
   penaltiesConceded,
   penaltyConcededCollapsingMaul,
   penaltyConcededCollapsingOffense,
   penaltyConcededDelibKnockOn,
   penaltyConcededDissent,
   penaltyConcededEarlyTackle,
   penaltyConcededFoulPlay,
   penaltyConcededHandlingInRuck,
   penaltyConcededHighTackle,
   penaltyConcededKillingRuck,
   penaltyConcededLineoutOffence,
   penaltyConcededObstruction,
   penaltyConcededOffside,
   penaltyConcededOppHalf,
   penaltyConcededOther,
   penaltyConcededOwnHalf,
   penaltyConcededScrumOffence,
   penaltyConcededStamping,
   penaltyConcededWrongSide,
   totalFreeKicksConceded,
   onReport,
   redCards,
   yellowCards
FROM VIEW_PLAYER_MATCH_STATS;
-- VIEW_PLAYER_MATCH_KICKING_STATS
CREATE VIEW IF NOT EXISTS VIEW_PLAYER_MATCH_KICKING_STATS AS
SELECT -- Informations
   `uid`,
   firstName,
   lastName,
   weight,
   height,
   teamName,
   teamAbbreviationName,
   teamColor,
   teamLogoUrl,
   matchName,
   matchDate,
   teamScore,
   opponentTeamScore,
   isHome,
   leagueName,
   season,
   opponentTeamName,
   -- Stats
   kicks,
   kickMetres,
   kickFromHandMetres,
   kicksFromHand,
   kickChargedDown,
   tryKicks,
   kickTryScored,
   kickOutOfPlay,
   kickInField,
   kickInTouch,
   kickOppnCollection,
   kickPossessionLost,
   kickPossessionRetained,
   kickTouchInGoal,
   kickPenaltyBad,
   kickPenaltyGood,
   kickPercentSuccess,
   pcKickPercent,
   kickReturns,
   kickReturnMetres,
   fortyTwenty,
   penaltyKickForTouchMetres
FROM VIEW_PLAYER_MATCH_STATS;
-- VIEW_PLAYER_MATCH_POSSESSION_CONTROL_STATS
CREATE VIEW IF NOT EXISTS VIEW_PLAYER_MATCH_POSSESSION_CONTROL_STATS AS
SELECT -- Informations
   `uid`,
   firstName,
   lastName,
   weight,
   height,
   teamName,
   teamAbbreviationName,
   teamColor,
   teamLogoUrl,
   matchName,
   matchDate,
   teamScore,
   opponentTeamScore,
   isHome,
   leagueName,
   season,
   opponentTeamName,
   -- Stats
   collectionFailed,
   collectionFromKick,
   collectionInterception,
   collectionLooseBall,
   collectionSuccess,
   retainedKicks,
   trueRetainedKicks,
   restart22m,
   restartErrorNotTen,
   restartErrorOutOfPlay,
   restartHalfway,
   restartOppError,
   restartOppPlayer,
   restartOwnPlayer,
   restartsLost,
   restartsSuccess,
   restartsWon,
   handlingError,
   droppedCatch,
   badPasses,
   ballOutOfPlay,
   pickup,
   catchFromKick,
   turnoverWon,
   turnoversConceded,
   turnoverOppHalf,
   turnoverOwnHalf,
   turnoverLostInRuckOrMaul,
   turnoverKnockOn,
   turnoverForwardPass,
   turnoverCarriedInTouch,
   turnoverCarriedOver,
   turnoverKickError,
   turnoverBadPass
FROM VIEW_PLAYER_MATCH_STATS;
-- VIEW_PLAYER_MATCH_SET_PIECES_STATS
CREATE VIEW IF NOT EXISTS VIEW_PLAYER_MATCH_SET_PIECES_STATS AS
SELECT -- Informations
   `uid`,
   firstName,
   lastName,
   weight,
   height,
   teamName,
   teamAbbreviationName,
   teamColor,
   teamLogoUrl,
   matchName,
   matchDate,
   teamScore,
   opponentTeamScore,
   isHome,
   leagueName,
   season,
   opponentTeamName,
   -- Stats
   scrumsWonFreeKick,
   scrumsWonOutright,
   scrumsWonPenalty,
   scrumsWonPenaltyTry,
   scrumsWonPushoverTry,
   scrumsLostFreeKick,
   scrumsLostOutright,
   scrumsLostPenalty,
   scrumsLostReversed,
   lineoutsWon,
   lineoutSuccess,
   lineoutsLost,
   lineoutsInfringeOpp,
   lineoutThrowWonClean,
   lineoutThrowWonFreeKick,
   lineoutThrowWonPenalty,
   lineoutThrowWonTap,
   lineoutThrowLostFreeKick,
   lineoutThrowLostHandlingError,
   lineoutThrowLostNotStraight,
   lineoutThrowLostOutright,
   lineoutThrowLostPenalty,
   lineoutsToOwnPlayer,
   lineoutNonStraight,
   lineoutWonOppThrow,
   lineoutWonOwnThrow,
   lineoutWonSteal,
   totalLineouts
FROM VIEW_PLAYER_MATCH_STATS;
-- VIEW_PLAYER_MATCH_RUCK_AND_MAUL_STATS
CREATE VIEW IF NOT EXISTS VIEW_PLAYER_MATCH_RUCK_AND_MAUL_STATS AS
SELECT -- Informations
   `uid`,
   firstName,
   lastName,
   weight,
   height,
   teamName,
   teamAbbreviationName,
   teamColor,
   teamLogoUrl,
   matchName,
   matchDate,
   teamScore,
   opponentTeamScore,
   isHome,
   leagueName,
   season,
   opponentTeamName,
   -- Stats
   rucksLost,
   rucksWon,
   maulsWon,
   maulsLost,
   maulsWonOutright,
   maulsLostOutright,
   maulsWonPenalty,
   maulsLostTurnover,
   maulsWonPenaltyTry,
   maulsWonTry
FROM VIEW_PLAYER_MATCH_STATS;
-- VIEW_PLAYER_MATCH_GENERAL_STATS
CREATE VIEW IF NOT EXISTS VIEW_PLAYER_MATCH_GENERAL_STATS AS
SELECT -- Informations
   `uid`,
   firstName,
   lastName,
   weight,
   height,
   teamName,
   teamAbbreviationName,
   teamColor,
   teamLogoUrl,
   matchName,
   matchDate,
   teamScore,
   opponentTeamScore,
   isHome,
   leagueName,
   season,
   opponentTeamName,
   -- Stats
   matches,
   won,
   lost,
   drawn,
   numberOfTeams,
   startingMatches,
   replacementMatches,
   mintuesPlayedBeforeFirstHalfExtra,
   minutesPlayedBeforeFirstHalf,
   minutesPlayedBeforePenaltyShootOut,
   minutesPlayedBeforeSecondHalfExtra,
   minutesPlayedBeforeSecondHalf,
   minutesPlayedFirstHalf,
   minutesPlayedFirstHalfExtra,
   minutesPlayedSecondHalf,
   minutesPlayedSecondHalfExtra,
   minutesPlayedTotal
FROM VIEW_PLAYER_MATCH_STATS;