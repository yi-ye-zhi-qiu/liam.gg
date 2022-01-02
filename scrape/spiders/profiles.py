import scrapy
import json
import pandas as pd
import numpy as np

class Profiles(scrapy.Spider):

    name = "profile"
    url = "https://u.gg/api"

    fp = "/Users/liamisaacs/src/zeke/2022-01-01-leaderboards.csv"

    headers = {
      'authority': 'u.gg',
      'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
      'sec-ch-ua-mobile': '?0',
      'authorization': '',
      'x-is-ssr': 'false',
      'content-type': 'application/json',
      'accept': '*/*',
      'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
      'sec-ch-ua-platform': '"macOS"',
      'origin': 'https://u.gg',
      'sec-fetch-site': 'same-origin',
      'sec-fetch-mode': 'cors',
      'sec-fetch-dest': 'empty',
      'referer': 'https://u.gg/lol/profile/na1/thresh/overview',
      'accept-language': 'en-US,en;q=0.9',
    }

    def api(self, profile_name):

        payload = json.dumps({
            'operationName': "FetchMatchSummaries",
            'variables': {
                'regionId': 'na1',
                'summonerName': profile_name,
                'queueType': [],
                'seasonIds': [
                    17,
                    16
                ],
                'championId': []
                },
              "query": "query FetchMatchSummaries($championId: [Int], $page: Int, $queueType: [Int], $regionId: String!, $role: [Int], $seasonIds: [Int]!, $summonerName: String!) {\n  fetchPlayerMatchSummaries(\n    championId: $championId\n    page: $page\n    queueType: $queueType\n    regionId: $regionId\n    role: $role\n    seasonIds: $seasonIds\n    summonerName: $summonerName\n  ) {\n    finishedMatchSummaries\n    totalNumMatches\n    matchSummaries {\n      assists\n      championId\n      cs\n      damage\n      deaths\n      gold\n      items\n      jungleCs\n      killParticipation\n      kills\n      level\n      matchCreationTime\n      matchDuration\n      matchId\n      maximumKillStreak\n      primaryStyle\n      queueType\n      regionId\n      role\n      runes\n      subStyle\n      summonerName\n      summonerSpells\n      psHardCarry\n      psTeamPlay\n      lpInfo {\n        lp\n        placement\n        promoProgress\n        promoTarget\n        promotedTo {\n          tier\n          rank\n          __typename\n        }\n        __typename\n      }\n      teamA {\n        championId\n        summonerName\n        teamId\n        role\n        hardCarry\n        teamplay\n        __typename\n      }\n      teamB {\n        championId\n        summonerName\n        teamId\n        role\n        hardCarry\n        teamplay\n        __typename\n      }\n      version\n      visionScore\n      win\n      __typename\n    }\n    __typename\n  }\n}\n"
         })

        return scrapy.Request(url=self.url,headers=self.headers,callback=self.parse,method="POST",body=payload)

    def start_requests(self):
        df = pd.read_csv(self.fp)
        profile_names = np.unique(df.summonerName.values)
        print(len(profile_names))
        for i in range(len(profile_names)):
            if i in range(10):
                api = self.api(profile_name = profile_names[i])
                yield api


    def parse(self, response):
        yield json.loads(response.text)
