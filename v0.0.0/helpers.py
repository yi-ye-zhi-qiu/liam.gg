import re

class PageParser:

    def parse_page(self, container):

        for div in container:

            #Defeat/Victory
            res = div.find_all("div", {"class": "GameResult"})
            #Int id
            game_id = div.find_all("div", {"class": "GameItem"})
            #Length
            game_len = div.find_all("div", {"class": "GameLength"})
            #Champ
            champion = div.find_all("div", {"class": "ChampionName"})
            #Summoner spells
            spells = div.find_all("div", {"class": "Spell"})
            #Runes
            runes = div.find_all("div", {"class": "Rune"})
            #KDA
            #Kill class can be cross-applied to text like 'Triple Kill',
            #so we force it to be of digits (int) class
            #Just to be fullproof we do this for deaths, assists too
            kills = div.find_all("span", {"class": "Kill"}, text=re.compile(r'^[0-9]'))
            deaths = div.find_all("span", {"class": "Death"}, text=re.compile(r'^[0-9]'))
            assists = div.find_all("span", {"class": "Assist"}, text=re.compile(r'^[0-9]'))
            #Level
            levels = div.find_all("div", {"class": "Level"})
            #CS
            cs = div.find_all("div", {"class": "CS"})
            #KP
            kp = div.find_all("div", {"class": "CKRate tip"})
            #MMR
            #mmr = div.find_all("div", {"class": "MMR"})
            #Items
            items = div.find_all("div", {"class": "ItemList"})
            #Wards
            wards = div.find_all("span", {"class": "wards vision"})

        game_id = [x['data-game-id'] for x in game_id]

        def split_dict(d):
            """Splits div w/ 2 imgs into a list of alt tags per img"""
            #List of alt vals
            d = [x.find({'img'})['alt'] for x in d]
            #Len 40 list -> len 20 list of lists, where each el is [el[i],el[i+1]]
            d = [ [d[x], d[x+1]]  for x in range(0,len(d),2) ]
            return d

        spells = split_dict(spells)
        runes = split_dict(runes)
        #items = split_dict(items)

        def get_items(items_div):
            """Get items as list"""

            items = []

            for div in items_div:
                
                try:
                    k = div.find('img')['alt']
                    items.append(k)
                except:
                    pass

            return items

        items = get_items(items)

        d = {'game_id': {},
             'result': {},
             'game_length': {},
             'champion': {},
             'spell_0': {},
             'spell_1': {},
             'rune_0': {},
             'rune_1': {},
             'kills': {},
             'deaths': {},
             'assists': {},
             'levels': {},
             'cs': {},
             'kp': {},
             #'mmr': {},
             'items': {},
             'wards': {}
            }

        for i in range(len(res)):

            d['game_id'][i] = int(game_id[i].strip())
            d['result'][i] = res[i].text.strip()
            d['game_length'][i] = game_len[i].text.strip()
            d['champion'][i] = champion[i].text.strip()
            d['spell_0'][i] = spells[i][0]
            d['spell_1'][i] = spells[i][1]
            d['rune_0'][i] = runes[i][0]
            d['rune_1'][i] = runes[i][1]
            d['kills'][i] = kills[i].text
            d['deaths'][i] = deaths[i].text
            d['assists'][i] = assists[i].text
            d['levels'][i] = levels[i].text.strip()
            d['cs'][i] = cs[i].text.strip()
            d['kp'][i] = kp[i].text.strip()
            #d['mmr'][i] = mmr[i]
            d['items'][i] = items[i]

            try:
                d['wards'][i] = wards[i].text
            except:
                d['wards'][i] = 0

        return d
