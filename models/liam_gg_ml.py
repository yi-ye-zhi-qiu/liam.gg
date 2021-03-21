from .liam_gg import game_info_by_match_id
from .colors import colors
from riotwatcher import LolWatcher, ApiError
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import numpy as np

def give_shap_plot(name, df, ranked_info, df_index, dfs, champ, primary_key):
    rank, spells = get_info(name, df, ranked_info)
    window = create_window(rank)
    window_df = make_df(window, rank)
    padded_df = pad_window(window_df, dfs)
    padded_df_no_arams = remove_arams(padded_df)
    f_df, how_many_games_added = filter_window(padded_df_no_arams, champ, spells)
    model = generate_model(f_df, primary_key, window, how_many_games_added)
    return model

def get_info(name, df, ranked_info):
    print(colors.CWHITEBG + colors.CBLACK + '[RUNNING MODEL]')
    try:
        rank = ranked_info['tier'].values[0] + ranked_info['rank'].values[0]
    except:
        rank = 'SILVERI'
    print(colors.CWHITEBG + colors.CBLACK + 'Querying ', rank, '...')
    spells = [df.loc[df['summonerName'] == name]['spell1'].values[0],df.loc[df['summonerName'] == name]['spell2'].values[0]]
    return rank, spells

#Create window
def create_window(rank):

    tier_pos = ['I', 'II', 'III', 'IV']
    rank_pos = ['IRON', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND']

    z = []
    for i in rank_pos:
        for j in tier_pos[::-1]:
            z.append(i+j)
    z += [e for e in ['MASTERI', 'GRANDMASTERI', 'CHALLENGERI']]

    index = z.index(rank)
    try:
        window = [z[index-2],z[index-1],z[index],z[index+1],z[index+2]]
    except IndexError:
        try:
            window = [z[index-1],z[index],z[index+1]]
        except IndexError:
            window = [z[index]]
    return window

#Create df from window
def make_df(window, rank):
    window_df = pd.read_csv('/Users/liamisaacs/Desktop/github repositories/personalwebsite/data/league/'+rank+'_MatchData.csv')
    for x in window:
        if x != rank:
            window_df = pd.concat([window_df, pd.read_csv('/Users/liamisaacs/Desktop/github repositories/personalwebsite/data/league/'+x+'_MatchData.csv')])
    return window_df

#Pad window
def pad_window(df, dfs):
    print(colors.CWHITEBG + colors.CBLACK + 'Padding from',str(df.shape),'(adding info from 30 games of user, 300 rows)')
    for i in range(1, len(dfs)):
        df = df.append(dfs[list(dfs.keys())[i]])
    print(colors.CWHITEBG + colors.CBLACK +'Padded shape..'+str(df.shape))
    df['win'].replace({'失败': 'defeat', '胜利': 'victory'}, inplace=True)
    return df

#Remove ARAMs
def remove_arams(df):
    arams_number = df[df['neutralMinionsKilledEnemyJungle'] == ''].shape[0]
    print(colors.CWHITEBG + colors.CBLACK + 'Removing',arams_number,'aram games')
    df = df[df['neutralMinionsKilledEnemyJungle'] !='']
    print(colors.CWHITEBG + colors.CBLACK + 'Arams removed')
    return df

#Filter window
def filter_window(window_df, champ, spells):
    print(colors.CWHITEBG + colors.CBLACK + 'Filtering for games played in window as',champ,'...')
    df_filtered_by_champName = window_df.loc[window_df['championName'] == champ]
    #print('post-filter shape is', df_filtered_by_champName.shape[0],'rows')
    #print('datasize inadequate (model will likely overfit), trying other filter windows...')

    print(colors.CWHITEBG + colors.CBLACK + 'Spells were, ',spells)
    #print('\nchecking jungle.. (if someone took Smite or not)')
    if 11 in spells:
        df_filtered_by_jungler = window_df.loc[window_df['spell1'] == 11]
        count_needed = 300-df_filtered_by_champName.shape[0]
        print(colors.CWHITEBG + colors.CBLACK + 'JUNGLE confirmed, padding with ',count_needed, 'other Jungler games within ranked window')
        df_filtered_by_champName = df_filtered_by_champName.append(df_filtered_by_jungler[0:count_needed])

        #print('Shape is',df_filtered_by_champName.shape[0],'rows long')
        return df_filtered_by_champName, count_needed
    else:
        print(colors.CREDBG + '[WARNING] Data inadequate (continuing..)')
        count_needed =df_filtered_by_champName.shape[0]
        return df_filtered_by_champName, count_needed

def generate_model(f_df, primary_key, window, how_many_games_added):

    print(colors.CWHITEBG+ colors.CBLACK + 'You are analyzing '+str(f_df.shape[0])+' games...')
    num_games = str(f_df.shape[0])

    ML_df = f_df
    ML_df.drop(['champion', 'spell1', 'spell2', 'teamId', 'item0',
             'totalDamageDealt', 'totalDamageDealtToChampions',
             'physicalDamageDealtToChampions', 'trueDamageDealtToChampions',
             'magicDamageDealtToChampions', 'totalHeal', 'totalDamageTaken',
             'physicalDamageDealt', 'trueDamageDealt', 'magicDamageDealt',
             'largestKillingSpree', 'largestMultiKill',
             'magicalDamageTaken',
             'physicalDamageTaken', 'trueDamageTaken',
             'killingSprees', 'doubleKills', 'tripleKills', 'quadraKills', 'pentaKills',
             'item1', 'item2', 'item3', 'item4', 'item5', 'item6',
             'lane', 'perkPrimaryStyle',
             'perkSubStyle', 'profileIcon', 'championName', 'championImage',
             'itemName0', 'itemImage0', 'itemName1', 'itemImage1',
             'itemName2', 'itemImage2', 'itemName3', 'itemImage3',
             'itemName4', 'itemImage4', 'itemName5', 'itemImage5',
             'itemName6', 'itemImage6', 'spell1Image', 'spell2Image',
             'profileIconImage', 'itemImage1', 'MVP', 'gameDuration',
             'gameMode', 'gameCreation', 'kda', 'killParticipation',
             'minionsKilledPerMinute', 'teamTotalKills', 'teamTotalGold',
             'teamTotalDamage', 'playerDamageAsFractionOfTeamDamage',
              'lastGamePlayedWhen', 'goldSpent',
              'creepsPerMinDeltas', 'goldPerMinDeltas', 'towerKills',
#              'firstBlood', 'baronKills',
#              'firstTower', 'firstRiftHerald',
#              'dragonKills', 'riftHeraldKills',
             'summonerName', 'Unnamed: 0',
             'goldEarned', 'rune1', 'rune2', 'rune1Image', 'rune2Image'], axis=1, inplace=True)

    #'victory/defeat' --> 'True/False'

    ML_df['win'].replace({'失败': False, '胜利': True}, inplace=True)
    ML_df['win'].replace({'defeat': False, 'victory': True}, inplace=True)
    #True/False --> 1/0
    ToBinary = ['firstBloodKill', 'firstTowerKill', 'firstBloodAssist',
          'firstTowerAssist', 'firstBlood', 'firstTower', 'firstRiftHerald']
    for col in ToBinary:
        ML_df[col].replace({False: 0, True: 1}, inplace=True)

    #Drop target from X
    X_ = ML_df.drop(["win"], axis=1)

    #Reset index and drop "index" column
    X_ = X_.reset_index()
    X_ = X_.drop(["index"], axis=1)

    #Convert string-based features (every column) to numbers
    for col in list(X_.columns):
        X_[col] = pd.to_numeric(X_[col])

    #Define features we will convert to rates
    rate_features = [
        # "kills", "deaths", "assists", "killingSprees", "doubleKills",
        # "tripleKills", "quadraKills", "pentaKills",
        # "totalDamageDealt", "magicDamageDealtToChampions", "physicalDamageDealt", "trueDamageDealt",
        # "totalDamageDealtToChampions", "magicDamageDealtToChampions", "physicalDamageDealtToChampions", "trueDamageDealtToChampions",
        # "trueDamageDealtToChampions", "magicDamageDealt",
        # "totalHeal", "totalUnitsHealed", "damageDealtToObjectives", "totalDamageTaken",
        # "magicalDamageTaken" , "physicalDamageTaken", "trueDamageTaken", "goldSpent",
        # "totalMinionsKilled", "neutralMinionsKilled", "neutralMinionsKilledTeamJungle",
        # "neutralMinionsKilledEnemyJungle", "totalTimeCrowdControlDealt", "visionWardsBoughtInGame",
        # "wardsPlaced", "wardsKilled"
    ]

    #Convery rate features to per minute rates of the game
    for feature_name in rate_features:
        X_[feature_name] /= X_["gameDur"] / 60 # per minute rate

    X_["longestTimeSpentLiving"] /= X_["gameDur"]

    full_names = {
        "kills": "Kills",
        "deaths": "Deaths",
        "assists": "Assists",
        "longestTimeSpentLiving": "Longest time living as % of game",
        "totalHeal": "Total healing",
        "totalUnitsHealed": "Total units healed",
        "damageDealtToObjectives": "Damage to objectives",
        "totalTimeCrowdControlDealt": "Time spent with crown control per min.",
        "goldSpent": "Gold spent",
        "totalMinionsKilled": "Total minions killed",
        "neutralMinionsKilled": "CS score",
        "neutralMinionsKilledTeamJungle": "Own jungle kills (# of camps)",
        "neutralMinionsKilledEnemyJungle": "Enemy jungle kills (# of camps)",
        "totalTimeCrowdControlDealt": "Time CCed enemies",
        "visionWardsBoughtInGame": "Pink wards bought per min.",
        "wardsPlaced": "Wards placed",
        "wardsKilled": "Wards killed",
        "turretKills": "# of turret kills",
        "inhibitorKills": "# of inhibitor kills",
        "damageDealtToTurrets": "Damage to turrets",
        "largestKillingSpree": "Largest killing spree",
        "largestMultiKill": "Largest multi kill",
        "largestCriticalStrike": "Largest critical strike",
        "damageSelfMitigated": "Self-mitigated damage",
        "visionScore": "Vision score",
        "firstBloodKill": "First blood (player)",
        "firstBlood": "First blood (team)",
        "firstBloodAssist": "First blood (assist)",
        "firstTower": "First tower (team)",
        "firstTowerKill": "First tower (player)",
        "firstTowerAssist": "First tower (assist)",
        "firstInhibitorKill": "First inhibitor",
        "firstInhibitorAssist": "First inhibitor (assist)",
        "gameDur": "Game Duration (in seconds)",
        "ccScore": "CC Score",
        "champLevel": "Champion Level",
        "dragonKills": "# of dragon kills",
        "baronKills": "# of baron kills",
        "firstRiftHerald": "First Rift Herald (team)",
        "riftHeraldKills": "# of rift herald kills"
    }

    # Define friendly names for the features
    # full_names = {
    #     "kills": "Kills per min.",
    #     "deaths": "Deaths per min.",
    #     "assists": "Assists per min.",
    #     "killingSprees": "Killing sprees per min.",
    #     "longestTimeSpentLiving": "Longest time living as % of game",
    #     "doubleKills": "Double kills per min.",
    #     "tripleKills": "Triple kills per min.",
    #     "quadraKills": "Quadra kills per min.",
    #     "pentaKills": "Penta kills per min.",
    #     "totalDamageDealt": "Total damage dealt per min.",
    #     "magicDamageDealt": "Magic damage dealt per min.",
    #     "physicalDamageDealt": "Physical damage dealt per min.",
    #     "trueDamageDealt": "True damage dealt per min.",
    #     "totalDamageDealtToChampions": "Total damage to champions per min.",
    #     "magicDamageDealtToChampions": "Magic damage to champions per min.",
    #     "physicalDamageDealtToChampions": "Physical damage to champions per min.",
    #     "trueDamageDealtToChampions": "True damage to champions per min.",
    #     "totalHeal": "Total healing per min.",
    #     "totalUnitsHealed": "Total units healed per min.",
    #     "damageDealtToObjectives": "Damage to objectives per min.",
    #     "totalTimeCrowdControlDealt": "Time spent with crown control per min.",
    #     "totalDamageTaken": "Total damage taken per min.",
    #     "magicalDamageTaken": "Magic damage taken per min.",
    #     "physicalDamageTaken": "Physical damage taken per min.",
    #     "trueDamageTaken": "True damage taken per min.",
    #     "goldSpent": "Gold spent per min.",
    #     "totalMinionsKilled": "Total minions killed per min.",
    #     "neutralMinionsKilled": "Neutral minions killed per min.",
    #     "neutralMinionsKilledTeamJungle": "Own jungle kills per min.",
    #     "neutralMinionsKilledEnemyJungle": "Enemy jungle kills per min.",
    #     "totalTimeCrowdControlDealt": "Total crown control time dealt per min.",
    #     "visionWardsBoughtInGame": "Pink wards bought per min.",
    #     "wardsPlaced": "Wards placed per min.",
    #     "wardsKilled": "Wards killed per min.",
    #     "turretKills": "# of turret kills",
    #     "inhibitorKills": "# of inhibitor kills",
    #     "damageDealtToTurrets": "Damage to turrets",
    #     "largestKillingSpree": "Largest killing spree",
    #     "largestMultiKill": "Largest multi kill",
    #     "largestCriticalStrike": "Largest critical strike",
    #     "damageSelfMitigated": "Self-mitigated damage",
    #     "visionScore": "Vision score",
    #     "firstBloodKill": "First blood",
    #     "firstBloodAssist": "First blood (assist)",
    #     "firstTowerKill": "First tower",
    #     "firstTowerAssist": "First tower (assist)",
    #     "firstInhibitorKill": "First inhibitor",
    #     "firstInhibitorAssist": "First inhibitor (assist)",
    #     "gameDur": "Game duration",
    #     "ccScore": "CC Score",
    #     "champLevel": "Champion Level"
    # }

    #Replace columns with nicer names
    feature_names = [full_names.get(n, n) for n in X_.columns]
    X_.columns = feature_names

    #Define target
    y_ = ML_df["win"]

    #Run train test split

    Xt, Xv, yt, yv = train_test_split(X_, y_, test_size=0.2, random_state=10)

    #Train model
    model = clf = LogisticRegression(penalty='l2', solver='liblinear', max_iter=900, C=0.1).fit(Xt, yt)

    """
    XGBOOST
    dt = xgb.DMatrix(Xt, label=yt.values, enable_categorical=True)
    dv = xgb.DMatrix(Xv, label=yv.values)

    #tuned hyperparameters via Bayesian optimization
    params = {
        "eta": 0.5,
        "max_depth": 8,
        'min_child_weight': 1,
        "objective": "binary:logistic",
        "verbosity": 0,
        "base_score": np.mean(yt),
        "eval_metric": "logloss",
        'colsample_bytree': 0.7434869381604485,
        'gamma': 1.1053886968419446,
        'reg_alpha': 49.0,
        'reg_lambda': 0.9997899615065826
    }

    model = xgb.train(params, dt, 35, [(dt, "train"), (dv, "valid")], early_stopping_rounds=5, verbose_eval=35)
    """
    print(colors.CWHITEBG + colors.CBLACK + '[ECHO] primary key used to index shap values is longest time spent living as % of the game (column name is "longestTimeSpentLiving") ' + str(primary_key))
    index_label = X_.loc[X_['Longest time living as % of game'] == (primary_key/ X_["Game Duration (in seconds)"])].index
    print(colors.CWHITEBG + colors.CBLACK + '[ECHO] Index used correspondent to primary key is ', str(index_label))

    print(colors.CGREENBG + colors.CBLACK + 'Model passed to app.py for SHAP graph')
    return model, Xt, Xv, X_, index_label, num_games, window, how_many_games_added
