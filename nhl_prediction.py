#
# NHL Game Predicting Algorithm
#
# Purpose of this script is to read in .xlsx files and predict
# the winner of the provided matchups
# 
# Creation Date: 2/4/2020
# Created by Kyle Davey with analytical insight from Nick Consolazio
#


class TeamStats:
    def __init__(self,
                name,
                isBackupIn,
                isPlayingB2b,
                isPlayingB2bA,
                powerPlayPercentage,
                penaltyKillPercentage,
                goalsForPerGame,
                goalsAgainstPerGame,
                gsaa,
                gaa,
                corsiFor,
                winsInLastTen,
                homeWinPercentage,
                awayWinPercentage,
                h2hWins,
                isHome,
                pimPerGame):

                self.name = name
                self.isBackupIn = isBackupIn
                self.isPlayingB2b = isPlayingB2b
                self.isPlayingB2bA = isPlayingB2bA
                self.powerPlayPercentage = powerPlayPercentage
                self.penaltyKillPercentage = penaltyKillPercentage
                self.goalsForPerGame = goalsForPerGame
                self.goalsAgainstPerGame = goalsAgainstPerGame
                self.gsaa = gsaa
                self.gaa = gaa
                self.corsiFor = corsiFor
                self.winsInLastTen = winsInLastTen
                self.homeWinPercentage = homeWinPercentage
                self.awayWinPercentage = awayWinPercentage
                self.h2hWins = h2hWins
                self.isHome = isHome
                self.pimPerGame = pimPerGame

               # self.gfDifference = xGF - aGF #Lower number better
                self.goalRatio = goalsForPerGame / goalsAgainstPerGame
                self.totalScore = 0 #Start at 0

    def displayAll(self):

        print('Name', self.name)
        print('Backup In', self.isBackupIn)
        print('B2B', self.isPlayingB2b)
        print('B2BA', self.isPlayingB2bA)
        print('PP', self.powerPlayPercentage)
        print('PK', self.penaltyKillPercentage)
        print('GAPG', self.goalsAgainstPerGame)
        print('GFPG', self.goalsForPerGame)
        print('GSAA', self.gsaa)
        print('GAA', self.gaa)
        print('CF%', self.corsiFor)
        print('Wins in Last 10', self.winsInLastTen)
        print('Goal Ratio', self.goalRatio)
        print('Total Score', self.totalScore)
        
def calcInitialScore(teams):
    #Stat weights
    backupWeight = -3
    b2bWeight = -1
    b2baWeight = -3 #This totals -4 
    # corsiWeight = 3 
    winsInLastTenWeight = 4 #Only if wins = 7 or above
    negativeWinsInLastTen = -2 #Only if wins = 2 or less

    for team in teams:
        if team.isBackupIn == 1:
            team.totalScore+=backupWeight
        
        if team.isPlayingB2b == 1:
            team.totalScore+=b2bWeight
        
        if team.isPlayingB2bA == 1:
            team.totalScore+=b2baWeight

        if team.winsInLastTen >= 7:
            team.totalScore+=winsInLastTenWeight
        elif team.winsInLastTen <=2:
            team.totalScore+=negativeWinsInLastTen
        
        print(team.name, " Initial Score: ", team.totalScore)


#Tean One: Home 
#Team Two: Away        
def evaluateMatchup(teamOne, teamTwo, leagueAvg):
    #Include powerplay comparison. goalRatio comparison
    ppAboveWeight = 2
    goalRatioWeightHigh = 4 #if Ratio is larger than .2
    goalRatioWeightLow = 2 #if Ratio is .2 or less
    gsaaWeight = 2
    gaaWeight = 1

    if teamOne.powerPlayPercentage > leagueAvg.powerPlayPercentage and teamTwo.penaltyKillPercentage < leagueAvg.penaltyKillPercentage:
        teamOne.totalScore+=ppAboveWeight
        print('PP Advantage, New Score for ', teamOne.name, ': ', teamOne.totalScore)
    elif teamTwo.powerPlayPercentage > leagueAvg.powerPlayPercentage and teamOne.penaltyKillPercentage < leagueAvg.penaltyKillPercentage:
        teamTwo.totalScore+=ppAboveWeight
        print('PP Advantage, New Score for ', teamTwo.name, ': ', teamTwo.totalScore)

    matchupGoalRatio = teamOne.goalRatio - teamTwo.goalRatio
    if matchupGoalRatio > 0: #Team one has higher ratio
        if matchupGoalRatio > 0.2:
            teamOne.totalScore+=goalRatioWeightHigh
            print('Goal Ratio Advantage High, New Score for ', teamOne.name, ': ', teamOne.totalScore)
        else:
            teamOne.totalScore+=goalRatioWeightLow
            print('Goal Ratio Advantage Low, New Score for ', teamOne.name, ': ', teamOne.totalScore)
    else: #Team two has higher ratio
        matchupGoalRatio = abs(matchupGoalRatio)
        if matchupGoalRatio > 0.2:
            teamTwo.totalScore+=goalRatioWeightHigh
            print('Goal Ratio Advantage High, New Score for ', teamTwo.name, ': ', teamTwo.totalScore)
        else:
            teamTwo.totalScore+=goalRatioWeightLow
            print('Goal Ratio Advantage Low, New Score for ', teamTwo.name, ': ', teamTwo.totalScore)


    if teamOne.gsaa > teamTwo.gsaa:
        teamOne.totalScore+=gsaaWeight
        print('GSAA Advantage, New Score for ', teamOne.name, ': ', teamOne.totalScore)
    else:
        teamTwo.totalScore+=gsaaWeight
        print('GSAA Advantage, New Score for ', teamTwo.name, ': ', teamTwo.totalScore)

    if teamOne.gaa < teamTwo.gaa:
        teamOne.totalScore+=gaaWeight
        print('GAA Advantage, New Score for ', teamOne.name, ': ', teamOne.totalScore)
    else:
        teamTwo.totalScore+=gaaWeight
        print('GAA Advantage, New Score for ', teamTwo.name, ': ', teamTwo.totalScore)
    
    corsiDif = teamOne.corsiFor - teamTwo.corsiFor
    if corsiDif > 0: #Team one higher
        if corsiDif <= 1.5:
            teamOne.totalScore+=1
            print('Corsi Advantage, New Score for ', teamOne.name, ': ', teamOne.totalScore)
        else:
            teamOne.totalScore+=3
            print('Corsi Advantage, New Score for ', teamOne.name, ': ', teamOne.totalScore)
    else:
        corsiDif = abs(corsiDif)
        if corsiDif <= 1.5:
            teamTwo.totalScore+=1
            print('Corsi Advantage, New Score for ', teamTwo.name, ': ', teamTwo.totalScore)
        else:
            teamTwo.totalScore+=2
            print('Corsi Advantage, New Score for ', teamTwo.name, ': ', teamTwo.totalScore)

    if teamOne.homeWinPercentage >= 64:
        teamOne.totalScore+=4
        print('Big Home Advantage, New Score for ', teamOne.name, ': ', teamOne.totalScore)
    elif teamOne.homeWinPercentage >= 60:
        teamOne.totalScore+=2
        print('Medium Home Advantage, New Score for ', teamOne.name, ': ', teamOne.totalScore)
    elif teamOne.homeWinPercentage >= leagueAvg.homeWinPercentage:
        teamOne.totalScore+=1
        print('Small Home Advantage, New Score for ', teamOne.name, ': ', teamOne.totalScore)
    else:
        teamOne.totalScore-=1
        print('Home disadvantage, New Score for ', teamOne.name, ': ', teamOne.totalScore)

    if teamTwo.awayWinPercentage >= 57:
        teamTwo.totalScore+=3
        print('Big Away Advantage, New Score for ', teamTwo.name, ': ', teamTwo.totalScore)
    elif teamTwo.awayWinPercentage >= 53:
        teamTwo.totalScore+=2
        print('Med Away Advantage, New Score for ', teamTwo.name, ': ', teamTwo.totalScore)
    elif teamTwo.awayWinPercentage >= leagueAvg.awayWinPercentage:
        teamTwo.totalScore+=1
        print('Small Away Advantage, New Score for ', teamTwo.name, ': ', teamTwo.totalScore)
    else:
        teamTwo.totalScore-=2
        print('Away disadvantage, New Score for ', teamTwo.name, ': ', teamTwo.totalScore)

    if teamOne.h2hWins > teamTwo.h2hWins:
        teamOne.totalScore+=1
        print('H2H Advantage, New Score for ', teamOne.name, ': ', teamOne.totalScore)
    
    if teamOne.h2hWins < teamTwo.h2hWins:
        teamTwo.totalScore+=1
        print('H2H Advantage, New Score for ', teamTwo.name, ': ', teamTwo.totalScore)

    if teamOne.pimPerGame > teamTwo.pimPerGame:
        teamTwo.totalScore+=1
        print('PIM Per Game Advantage, New Score for ', teamTwo.name, ': ', teamTwo.totalScore)
    else:
        teamOne.totalScore+=1
        print('PIM Per Game Advantage, New Score for ', teamOne.name, ': ', teamOne.totalScore)

    teamOneResult, teamTwoResult = teamOne.totalScore, teamTwo.totalScore
    print('-------------------------------------------')
    print(teamOne.name, " Score: ", teamOneResult)
    print(teamTwo.name, " Score: ", teamTwoResult)

    if teamOneResult > teamTwoResult:
        print(teamOne.name, " is the predicted winner!")
        print('-------------------------------------------')
    else:
        print(teamTwo.name, " is the predicted winner!")
        print('-------------------------------------------')



import csv
import pandas as pd

if __name__ == "__main__":
    
    df = pd.read_excel('nhl_all_data.xlsx', sheet_name='Main')

    teams = df.values.tolist()
    teamList = []
    for t in teams:
        teamList.append(TeamStats(*t))

    knights = next(x for x in teamList if x.name == 'Vegas Golden Knights')
    lightning = next(x for x in teamList if x.name == 'Tampa Bay Lightning')
    hurricanes = next(x for x in teamList if x.name == 'Carolina Hurricanes')
    blues = next(x for x in teamList if x.name == 'St. Louis Blues')
    oilers = next(x for x in teamList if x.name == 'Edmonton Oilers')
    coyotes = next(x for x in teamList if x.name == 'Arizona Coyotes')
    avalanche = next(x for x in teamList if x.name == 'Colorado Avalanche')
    sabres = next(x for x in teamList if x.name == 'Buffalo Sabres')
    leafs = next(x for x in teamList if x.name == 'Toronto Maple Leafs')
    canadiens = next(x for x in teamList if x.name == 'Montreal Canadiens')
    flyers = next(x for x in teamList if x.name == 'Philadelphia Flyers')
    capitals = next(x for x in teamList if x.name == 'Washington Capitals')
    kings = next(x for x in teamList if x.name == 'Los Angeles Kings')
    devils = next(x for x in teamList if x.name == 'New Jersey Devils')
    blueJackets = next(x for x in teamList if x.name == 'Columbus Blue Jackets')
    stars = next(x for x in teamList if x.name == 'Dallas Stars')
    flames = next(x for x in teamList if x.name == 'Calgary Flames')
    canucks = next(x for x in teamList if x.name == 'Vancouver Canucks')
    bruins = next(x for x in teamList if x.name == 'Boston Bruins')
    jets = next(x for x in teamList if x.name == 'Winnipeg Jets')
    senators = next(x for x in teamList if x.name == 'Ottawa Senators')
    penguins = next(x for x in teamList if x.name == 'Pittsburgh Penguins')
    panthers = next(x for x in teamList if x.name == 'Florida Panthers')
    redWings = next(x for x in teamList if x.name == 'Detroit Red Wings')
    blackhawks = next(x for x in teamList if x.name == 'Chicago Blackhawks')
    ducks = next(x for x in teamList if x.name == 'Anaheim Ducks')

    calcInitialScore(teamList)
    evaluateMatchup(redWings, bruins, teamList[0])
    evaluateMatchup(jets, blackhawks, teamList[0])
    evaluateMatchup(sabres, ducks, teamList[0])
