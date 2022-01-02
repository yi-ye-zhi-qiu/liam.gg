from datetime import datetime
import pandas as pd

def main(fp): 

    df = pd.read_json(fp) 

    df["matches"] = (df
                     .data
                     .map(
                            lambda x: x['fetchPlayerMatchSummaries']
                         )
                     .map(
                            lambda x: x['matchSummaries']
                         )
                     )

    df = df.explode('matches') 

    df = pd.json_normalize(df.matches) 

    def export(nickname, payload): 

        d = datetime.now().strftime('%Y-%m-%d') 
        fp = f'{d}-{nickname}.csv' 
        payload.to_csv(fp, index=False)

    export("profiles", df)

    return df

if __name__ == "__main__": 

    main()
