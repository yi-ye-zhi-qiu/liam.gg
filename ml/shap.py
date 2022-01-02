import pandas as pd 
import sklearn 
from sklearn.model_selection import train_test_split
import numpy as np 
import shap 

shap.initjs() 

fp = ""

def load(fp): 

    df = pd.read_csv(fp) 

    cols = {"assists",
            "championId",
            "cs",
            "damage",
            "deaths",
            "gold",
            #"items",
            "jungleCs",
            "killParticipation",
            "kills",
            "level",
            #"matchCreationTime",
            "matchDuration",
            #"matchId",
            "maximumKillStreak",
            #"primaryStyle",
            #"psHardCarry",
            #"psTeamPlay",
            #"queueType",
            #"regionId",
            "role",
            #"runes",
            "subStyle",
            #"summonerName",
            #"summonerSpells",
            #"teamA",
            #"teamB",
            #"version",
            "visionScore",
            "win"
           }

    df = df [
            set(
                df.columns.tolist()
            ).intersection(cols)
         ]

    return df

df = load(fp) 

target = "win" 
y = df[target] 
df = df.drop(target, axis=1)

X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=0.2, random_state=7)

model = sklearn.linear_model.LogisticRegression(penalty="l2", C=0.1)
model.fit(X_train, y_train)
explainer = shap.Explainer(model, X_train, feature_names=X_train.columns)
shap_values = explainer(X_test)
