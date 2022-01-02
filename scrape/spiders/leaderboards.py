import scrapy
import json

class Leaderboards(scrapy.Spider):

    name ="leaderboards"
    url = "https://u.gg/api"

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
      'referer': 'https://u.gg/leaderboards/ranking?region=na1',
      'accept-language': 'en-US,en;q=0.9'
    }

    def api(self, idx):

        payload = json.dumps({
          "operationName": "getRankedLeaderboard",
          "variables": {
            "page": idx,
            "queueType": 420,
            "regionId": "na1"
          },
          "query": "query getRankedLeaderboard($page: Int, $queueType: Int, $regionId: String!) {\n  leaderboardPage(page: $page, queueType: $queueType, regionId: $regionId) {\n    totalPlayerCount\n    topPlayerMostPlayedChamp\n    players {\n      iconId\n      losses\n      lp\n      overallRanking\n      rank\n      summonerLevel\n      summonerName\n      tier\n      wins\n      __typename\n    }\n    __typename\n  }\n}\n"
        })

        return scrapy.Request(url=self.url,headers=self.headers,method="POST",body=payload,callback=self.parse)

    def start_requests(self):

        n =10
        for i in range(1, n):
            api = self.api(i)
            yield api

    def parse(self, response):

        yield json.loads(response.text)
