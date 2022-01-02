from datetime import datetime
import pandas as pd 

def main(fp): 

    df = pd.read_json(fp) 

    df = pd.json_normalize(
            pd.json_normazlie(df.data) 
            .explode('leaderboardPage.players')
            ['leaderboardPage.players']
         )

    def export(nickname, payload): 

        d = datetime.now().strftime('%Y-%m-%d')
        fp = f'{d}-{nickname}.csv'
        payload.to_csv(fp, index=False)

    export("leaderboards", df)


if __name__ == "__main__":

    main()
