from riotwatcher import LolWatcher, ApiError
import pandas as pd
import numpy as np
import pprint
from datetime import datetime


# Fetching game data

class game_info_by_match_id():
    """
    Returns df of user info from a given match (so far).
    """
    #define private variables to use in class

    def __init__(self, api_key, name, region, gamemode, gameid):
        #upon calling the class we pass in a bunch of things to initialize^
        self.api_key = api_key
        self.name = name
        self.region = region
        self.gamemode = gamemode
        self.gameid = gameid
        watcher = LolWatcher(self.api_key)
        self.user = watcher.summoner.by_name(region, name)

    def rank_stats(self):
        watcher = LolWatcher(self.api_key)

        #league, division, games played, etc.
        encrypted_summoner_id = self.user['id']
        self.rank_stats = watcher.league.by_summoner(self.region, self.user['id'])
        return self.rank_stats

    def match_data(self):
        watcher = LolWatcher(self.api_key)

        self.matches = watcher.match.matchlist_by_account(self.region, self.user['accountId'])

        self.match_data = watcher.match.by_id(self.region, self.gameid)
        m = self.match_data

        #n is for each "participant" or player in the match
        def gd():
            n = [] #dump raw stats into here from participants
            for row in m['participants']:
                m_row = {}
                m_row['champion'] = row['championId']
                m_row['spell1'] = row['spell1Id']
                m_row['spell2'] = row['spell2Id']
                m_row['teamId'] = row['teamId']
                win_lose = row['stats']['win']
                if win_lose == True:
                    win_lose = '胜利'
                else:
                    win_lose = '失败'
                m_row['win'] = win_lose
                m_row['kills'] = row['stats']['kills']
                m_row['deaths'] = row['stats']['deaths']
                m_row['assists'] = row['stats']['assists']
                m_row['totalDamageDealt'] = row['stats']['totalDamageDealt']
                m_row['totalDamageDealtToChampions'] = row['stats']['totalDamageDealtToChampions']
                m_row['goldEarned'] = row['stats']['goldEarned']
                m_row['champLevel'] = row['stats']['champLevel']
                m_row['totalMinionsKilled'] = row['stats']['totalMinionsKilled']
                m_row['largestKillingSpree'] = row['stats']['largestKillingSpree']
                m_row['largestMultiKill'] = row['stats']['largestMultiKill']
                m_row['item0'] = row['stats']['item0']
                m_row['item1'] = row['stats']['item1']
                m_row['item2'] = row['stats']['item2']
                m_row['item3'] = row['stats']['item3']
                m_row['item4'] = row['stats']['item4']
                m_row['item5'] = row['stats']['item5']
                m_row['item6'] = row['stats']['item6']
                m_row['firstBloodKill'] = row['stats']['firstBloodKill']
                m_row['firstBloodAssist'] = row['stats']['firstBloodAssist']
                m_row['visionWardsBoughtInGame'] = row['stats']['visionWardsBoughtInGame']
                m_row['visionScore'] = row['stats']['visionScore']
                m_row['creepsPerMinDeltas'] = row['timeline']['creepsPerMinDeltas']
                m_row['goldPerMinDeltas'] = row['timeline']['goldPerMinDeltas']
                m_row['lane'] = row['timeline']['lane']
                m_row['ccScore'] = row['stats']['totalTimeCrowdControlDealt']
                m_row['perkPrimaryStyle'] = row['stats']['perkPrimaryStyle']
                m_row['perkSubStyle'] = row['stats']['perkSubStyle']
                m_row['killingSprees'] = row['stats']['killingSprees']
                m_row['longestTimeSpentLiving'] = row['stats']['longestTimeSpentLiving']
                m_row['doubleKills'] = row['stats']['doubleKills']
                m_row['tripleKills'] = row['stats']['tripleKills']
                m_row['quadraKills'] = row['stats']['quadraKills']
                m_row['pentaKills'] = row['stats']['pentaKills']
                m_row['magicDamageDealtToChampions'] = row['stats']['magicDamageDealtToChampions']
                m_row['physicalDamageDealtToChampions'] = row['stats']['physicalDamageDealtToChampions']
                m_row['physicalDamageDealtToChampions'] = row['stats']['physicalDamageDealtToChampions']
                m_row['trueDamageDealtToChampions'] = row['stats']['trueDamageDealtToChampions']
                m_row['totalHeal'] = row['stats']['totalHeal']
                m_row['totalUnitsHealed'] = row['stats']['totalUnitsHealed']
                m_row['damageDealtToObjectives'] = row['stats']['damageDealtToObjectives']
                m_row['damageDealtToTurrets'] = row['stats']['damageDealtToTurrets']
                m_row['totalDamageTaken'] = row['stats']['totalDamageTaken']
                m_row['magicalDamageTaken'] = row['stats']['magicalDamageTaken']
                m_row['physicalDamageTaken'] = row['stats']['physicalDamageTaken']
                m_row['trueDamageTaken'] = row['stats']['trueDamageTaken']
                m_row['turretKills'] = row['stats']['turretKills']
                m_row['inhibitorKills'] = row['stats']['inhibitorKills']
                m_row['firstTowerKill'] = row['stats']['firstTowerKill']
                m_row['firstTowerAssist'] = row['stats']['firstTowerAssist']
                m_row['totalDamageDealt'] = row['stats']['totalDamageDealt']
                m_row['physicalDamageDealt'] = row['stats']['physicalDamageDealt']
                m_row['trueDamageDealt'] = row['stats']['trueDamageDealt']
                m_row['magicDamageDealt'] = row['stats']['magicDamageDealt']
                m_row['goldSpent'] = row['stats']['goldSpent']
                m_row['neutralMinionsKilled'] = row['stats']['neutralMinionsKilled']
                m_row['neutralMinionsKilledTeamJungle'] = row['stats']['neutralMinionsKilledTeamJungle']
                m_row['neutralMinionsKilledEnemyJungle'] = row['stats']['neutralMinionsKilledEnemyJungle']
                m_row['totalTimeCrowdControlDealt'] = row['stats']['totalTimeCrowdControlDealt']
                m_row['wardsPlaced'] = row['stats']['wardsPlaced']
                m_row['wardsKilled'] = row['stats']['wardsKilled']
                n.append(m_row)
            return n

        n = gd()
        for i in range(0,len(n)):
            n[i]['summonerName'] = m['participantIdentities'][i]['player']['summonerName']
            n[i]['profileIcon'] = m['participantIdentities'][i]['player']['profileIcon']

        latest = watcher.data_dragon.versions_for_region(self.region)['n']['champion']
        static_champ_list = watcher.data_dragon.champions(latest, False, 'en_US')
        static_item_list = watcher.data_dragon.items(latest, 'en_US')
        static_summonerspell_list = watcher.data_dragon.summoner_spells(latest, 'en_US')

        def g_c(n): #gets summoner spells, champions, and items

            #summoner spells
            spell_url = "http://ddragon.leagueoflegends.com/cdn/11.2.1/img/spell/"

            summonerspell_dict = {}
            for key in static_summonerspell_list['data']:
                row = static_summonerspell_list['data'][key]
                summonerspell_dict[row['key']] = row['id']
                summonerspell_dict[row['key']] = spell_url + str(row['image']['full'])

            #champs
            champ_url = "https://ddragon.leagueoflegends.com/cdn/11.2.1/img/champion/"

            champ_name_dict = {}
            champ_image_dict = {}
            for key in static_champ_list['data']:
                row = static_champ_list['data'][key]
                champ_name_dict[row['key']] = row['id']
               # champ_dict[row['image']] = champ_url + str(row['image']['full'])
                champ_image_dict[row['key']] = champ_url +  str(row['image']['full'])

            #items
            item_url = "https://ddragon.leagueoflegends.com/cdn/11.2.1/img/item/"

            item_dict = {}

            for key in static_item_list['data']:
                row = static_item_list['data'][key]
                item_dict[key] = row['name']
            #add to df
            for row in n:
                #print(str(row['item1']) + ' ' + item_dict[str(row['item1'])])
                row['championName'] = champ_name_dict[str(row['champion'])]
                row['championImage'] = champ_image_dict[str(row['champion'])]
                for i in range(0,7):
                    try:
                        row['itemName' +str(i)] = item_dict[str(row['item'+str(i)])]
                        row['itemImage' + str(i)] = item_url + str(row['item'+str(i)]) + '.png'
                    except:
                        row['itemName' +str(i)] = 0
                row['spell1Image'] = summonerspell_dict[str(row['spell1'])]
                row['spell2Image'] = summonerspell_dict[str(row['spell2'])]

                row['profileIconImage'] = 'http://ddragon.leagueoflegends.com/cdn/11.2.1/img/profileicon/' + str(row['profileIcon']) + '.png'

            df = pd.DataFrame(n)

            if self.name == 'Divine Right':
                df['MVP'] = 'MVP'
            else:
                df['MVP'] = ''

            return df

        df = g_c(n)
        #add in extra columns
        df['gameDur'] = m['gameDuration']
        df['gameDuration'] = round((m['gameDuration'] / 60),2)
        df['gameMode'] = m['gameMode']
        df['gameCreation'] = m['gameCreation'] / 1000
        df['kda'] = ((df['kills'] + df['assists']) / df['deaths']).round(2)
        df['killParticipation'] = ((df['kills'] + df['assists'])/ df.groupby('teamId')['kills'].transform(np.sum) * 100).astype(int)
        df['minionsKilledPerMinute'] = (df['totalMinionsKilled'] / df['gameDuration']).round(1)
        df['teamTotalKills'] = df['teamId'].apply(lambda x: df['kills'].groupby(df['teamId']).sum().values[0] if x == 100 else df['kills'].groupby(df['teamId']).sum().values[1])        #get time since last played (in days)
        df['teamTotalGold'] = df['teamId'].apply(lambda x: df['goldEarned'].groupby(df['teamId']).sum().values[0] if x == 100 else df['goldEarned'].groupby(df['teamId']).sum().values[1])
        df['teamTotalDamage'] = df['teamId'].apply(lambda x: df['totalDamageDealtToChampions'].groupby(df['teamId']).sum().values[0] if x == 100 else df['totalDamageDealtToChampions'].groupby(df['teamId']).sum().values[1])
        df['playerDamageAsFractionOfTeamDamage'] = df['totalDamageDealtToChampions'] / df['teamTotalDamage']
        df['playerDamageAsFractionOfTeamDamage'] = round(df['playerDamageAsFractionOfTeamDamage'],2)*100

        df.loc[(df.kda == np.inf), 'kda'] = 'BEAST-MODE'

        #get time since last played (in days)

        now = datetime.now()
        last_game_played_when = df['gameCreation'].values[0]
        last_game_played_when = datetime.fromtimestamp(last_game_played_when)

        df['lastGamePlayedWhen'] = (now - last_game_played_when).days

        #get first blood, baron kills, etc.
        def g_t(df):
            def x(y):
                m_id = m['teams'][0]['teamId']
                m_team = m['teams'][0]
                return np.where(df['teamId']==m_id, m_team[y], m['teams'][0+1][y])
            l = ['firstBlood', 'baronKills', 'firstTower', 'firstRiftHerald', 'towerKills',
                 'inhibitorKills', 'dragonKills','riftHeraldKills']
            for i in l:
                df[i] = x(i)
            return df

        def game_dur(x):
            x = str(x).split('.')
            return x[0] + ' m ' + x[1] + ' s'

        df['gameDuration'] = game_dur(df['gameDuration'].values[0])

        df = g_t(df)

        return df
