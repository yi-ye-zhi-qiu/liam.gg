import pandas as pd
import numpy as np
import xgboost as xgb
import shap
from sklearn.model_selection import train_test_split
import pickle
from io import BytesIO
import matplotlib.pyplot as plt
import base64

shap.initjs()
#replace True/False with 1/0

def give_shap_plot(df, name):
    input_df = df.copy()
    t_f_col = ['win']
    binary_t_f_col = ['firstBloodKill']
    for col in t_f_col:
        input_df[col].replace({'失败': False, '胜利': True}, inplace=True)
    for col in binary_t_f_col:
        input_df[col].replace({'False': 0, '胜利': 1}, inplace=True)

    input_df.drop(['champion', 'spell1', 'spell2', 'teamId', 'item0',
                 'item1', 'item2', 'item3', 'item4', 'item5', 'item6',
                 'creepsPerMinDeltas', 'goldPerMinDeltas', 'lane', 'perkPrimaryStyle',
                 'perkSubStyle', 'profileIcon', 'championName', 'championImage',
                 'itemName0', 'itemImage0', 'itemName1', 'itemImage1',
                 'itemName2', 'itemImage2', 'itemName3', 'itemImage3',
                 'itemName4', 'itemImage4', 'itemName5', 'itemImage5',
                 'itemName6', 'itemImage6', 'spell1Image', 'spell2Image',
                 'profileIconImage', 'itemImage1', 'MVP', 'gameDuration',
                 'gameMode', 'gameCreation', 'kda', 'killParticipation',
                 'minionsKilledPerMinute', 'teamTotalKills', 'teamTotalGold',
                 'teamTotalDamage', 'playerDamageAsFractionOfTeamDamage',
                 'lastGamePlayedWhen', 'firstBlood', 'baronKills',
                 'firstTower', 'firstRiftHerald', 'towerKills',
                 'dragonKills', 'riftHeraldKills'], axis=1, inplace=True)
    #Define features we want to convert to rates
    rate_features = [
        "kills", "deaths", "assists", "killingSprees", "doubleKills",
        "tripleKills", "quadraKills", "pentaKills",
        "totalDamageDealt", "magicDamageDealtToChampions", "physicalDamageDealt", "trueDamageDealt",
        "totalDamageDealtToChampions", "magicDamageDealtToChampions", "physicalDamageDealtToChampions", "trueDamageDealtToChampions",
        "trueDamageDealtToChampions", "magicDamageDealt",
        "totalHeal", "totalUnitsHealed", "damageDealtToObjectives", "ccScore", "totalDamageTaken",
        "magicalDamageTaken" , "physicalDamageTaken", "trueDamageTaken", "goldEarned", "goldSpent",
        "totalMinionsKilled", "neutralMinionsKilled", "neutralMinionsKilledTeamJungle",
        "neutralMinionsKilledEnemyJungle", "totalTimeCrowdControlDealt", "visionWardsBoughtInGame",
        "wardsPlaced", "wardsKilled"
    ]

    #Convert all columns to numbers
    for col in rate_features:
        input_df[col] = pd.to_numeric(input_df[col])

    #Convery rate features to per minute rates of the game
    for feature_name in rate_features:
        input_df[feature_name] /= input_df["gameDur"] / 60 # per minute rate

    input_df["longestTimeSpentLiving"] /= input_df["gameDur"]

    # Define friendly names for the features
    full_names = {
        "kills": "Kills per min.",
        "deaths": "Deaths per min.",
        "assists": "Assists per min.",
        "killingSprees": "Killing sprees per min.",
        "longestTimeSpentLiving": "Longest time living as % of game",
        "doubleKills": "Double kills per min.",
        "tripleKills": "Triple kills per min.",
        "quadraKills": "Quadra kills per min.",
        "pentaKills": "Penta kills per min.",
        "totalDamageDealt": "Total damage dealt per min.",
        "magicDamageDealt": "Magic damage dealt per min.",
        "physicalDamageDealt": "Physical damage dealt per min.",
        "trueDamageDealt": "True damage dealt per min.",
        "totalDamageDealtToChampions": "Total damage to champions per min.",
        "magicDamageDealtToChampions": "Magic damage to champions per min.",
        "physicalDamageDealtToChampions": "Physical damage to champions per min.",
        "trueDamageDealtToChampions": "True damage to champions per min.",
        "totalHeal": "Total healing per min.",
        "totalUnitsHealed": "Total units healed per min.",
        "damageDealtToObjectives": "Damage to objects per min.",
        "timeCCingOthers": "Time spent with crown control per min.",
        "totalDamageTaken": "Total damage taken per min.",
        "magicalDamageTaken": "Magic damage taken per min.",
        "physicalDamageTaken": "Physical damage taken per min.",
        "trueDamageTaken": "True damage taken per min.",
        "goldEarned": "Gold earned per min.",
        "goldSpent": "Gold spent per min.",
        "totalMinionsKilled": "Total minions killed per min.",
        "neutralMinionsKilled": "Neutral minions killed per min.",
        "neutralMinionsKilledTeamJungle": "Own jungle kills per min.",
        "neutralMinionsKilledEnemyJungle": "Enemy jungle kills per min.",
        "totalTimeCrowdControlDealt": "Total crown control time dealt per min.",
        "visionWardsBoughtInGame": "Pink wards bought per min.",
        "wardsPlaced": "Wards placed per min.",
        "wardsKilled": "Wards killed per min.",
        "turretKills": "# of turret kills",
        "inhibitorKills": "# of inhibitor kills",
        "damageDealtToTurrets": "Damage to turrets",
        "largestKillingSpree": "Largest killing spree",
        "largestMultiKill": "Largest multikill"
    }
    #Replace columns with nicer names
    feature_names = [full_names.get(n, n) for n in input_df.columns]
    input_df.columns = feature_names

    df_model = pd.read_csv('/Users/liamisaacs/Desktop/github repositories/personalwebsite/data/liamgg_data.csv')
    #replace True/False with 1/0
    t_f_col = ['win']
    binary_t_f_col = ['firstBloodKill', 'firstTowerKill', 'firstBloodAssist',
              'firstTowerAssist', 'firstInhibitorKill', 'firstInhibitorAssist']
    for col in t_f_col:
        df_model[col].replace({'False': False, 'True': True}, inplace=True)
    for col in binary_t_f_col:
        df_model[col].replace({'False': 0, 'True': 1}, inplace=True)

    #Convert all columns to numbers
    for col in list(df_model.columns):
        df_model[col] = pd.to_numeric(df_model[col])


    #Define features we want to convert to rates
    rate_features = [
        "kills", "deaths", "assists", "killingSprees", "doubleKills",
        "tripleKills", "quadraKills", "pentaKills",
        "totalDamageDealt", "magicDamageDealtToChampions", "physicalDamageDealt", "trueDamageDealt",
        "totalDamageDealtToChampions", "magicDamageDealtToChampions", "physicalDamageDealtToChampions", "trueDamageDealtToChampions",
        "trueDamageDealtToChampions", "magicDamageDealt",
        "totalHeal", "totalUnitsHealed", "damageDealtToObjectives", "timeCCingOthers", "totalDamageTaken",
        "magicalDamageTaken" , "physicalDamageTaken", "trueDamageTaken", "goldEarned", "goldSpent",
        "totalMinionsKilled", "neutralMinionsKilled", "neutralMinionsKilledTeamJungle",
        "neutralMinionsKilledEnemyJungle", "totalTimeCrowdControlDealt", "visionWardsBoughtInGame",
        "wardsPlaced", "wardsKilled"
    ]

    #Convery rate features to per minute rates of the game
    for feature_name in rate_features:
        df_model[feature_name] /= df_model["gameDuration"] / 60 # per minute rate

    df_model["longestTimeSpentLiving"] /= df_model["gameDuration"]

    # Define friendly names for the features
    full_names = {
        "kills": "Kills per min.",
        "deaths": "Deaths per min.",
        "assists": "Assists per min.",
        "killingSprees": "Killing sprees per min.",
        "longestTimeSpentLiving": "Longest time living as % of game",
        "doubleKills": "Double kills per min.",
        "tripleKills": "Triple kills per min.",
        "quadraKills": "Quadra kills per min.",
        "pentaKills": "Penta kills per min.",
        "totalDamageDealt": "Total damage dealt per min.",
        "magicDamageDealt": "Magic damage dealt per min.",
        "physicalDamageDealt": "Physical damage dealt per min.",
        "trueDamageDealt": "True damage dealt per min.",
        "totalDamageDealtToChampions": "Total damage to champions per min.",
        "magicDamageDealtToChampions": "Magic damage to champions per min.",
        "physicalDamageDealtToChampions": "Physical damage to champions per min.",
        "trueDamageDealtToChampions": "True damage to champions per min.",
        "totalHeal": "Total healing per min.",
        "totalUnitsHealed": "Total units healed per min.",
        "damageDealtToObjectives": "Damage to objects per min.",
        "timeCCingOthers": "Time spent with crown control per min.",
        "totalDamageTaken": "Total damage taken per min.",
        "magicalDamageTaken": "Magic damage taken per min.",
        "physicalDamageTaken": "Physical damage taken per min.",
        "trueDamageTaken": "True damage taken per min.",
        "goldEarned": "Gold earned per min.",
        "goldSpent": "Gold spent per min.",
        "totalMinionsKilled": "Total minions killed per min.",
        "neutralMinionsKilled": "Neutral minions killed per min.",
        "neutralMinionsKilledTeamJungle": "Own jungle kills per min.",
        "neutralMinionsKilledEnemyJungle": "Enemy jungle kills per min.",
        "totalTimeCrowdControlDealt": "Total crown control time dealt per min.",
        "visionWardsBoughtInGame": "Pink wards bought per min.",
        "wardsPlaced": "Wards placed per min.",
        "wardsKilled": "Wards killed per min.",
        "turretKills": "# of turret kills",
        "inhibitorKills": "# of inhibitor kills",
        "damageDealtToTurrets": "Damage to turrets",
        "largestKillingSpree": "Largest killing spree",
        "largestMultiKill": "Largest multikill"
    }
    #Replace columns with nicer names
    feature_names = [full_names.get(n, n) for n in df_model.columns]
    df_model.columns = feature_names

    df_model= df_model.append(input_df.loc[df['summonerName'] == name], ignore_index=True)
    df_model.drop(['ccScore', 'summonerName', 'gameDur'], axis=1, inplace=True)

    X_ = df_model.drop(["win"], axis=1)
    y_ = df_model["win"]

    Xt, Xv, yt, yv = train_test_split(X_,y_, test_size=0.2, random_state=10)

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

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(Xv)

    shap_plot = shap.force_plot(explainer.expected_value, shap_values[-1:], features=Xv.iloc[-1:], feature_names=Xv.columns[0:20],
    matplotlib=True, show=False, plot_cmap=['#77dd77', '#f99191'])

    buf = BytesIO()
    plt.savefig(buf,
                format = "png",
                dpi = 150,
                bbox_inches = 'tight')
    dataToTake = base64.b64encode(buf.getbuffer()).decode("ascii")
    return dataToTake
