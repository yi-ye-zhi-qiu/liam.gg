from flask import *
from flask import Flask, render_template, request, jsonify, make_response
from models.liamometer import get_movie_data
from riotwatcher import LolWatcher, ApiError
from models.liam_gg import game_info_by_match_id
from models.liam_gg_ml import give_shap_plot
import pandas as pd
import shap
import matplotlib
matplotlib.use('qt5agg')
shap.initjs()

app = Flask(__name__)

@app.route('/league')
def show_league():
    return render_template('league.html')

#on page load of liamgg.html
@app.route('/league', methods=["GET", "POST"])
def riot_api_call():
    if request.method == 'POST':
        form = request.form
    for key in form:
        name = form[key]

    api_key = 'RGAPI-a2d1e695-2000-4f49-afff-57606b210cab'
    gamemode = 'CLASSIC'
    region = 'na1'
    watcher = LolWatcher(api_key)
    user = watcher.summoner.by_name('na1', name)
    matches = watcher.match.matchlist_by_account(region, user['accountId'])

    game_ids = []

    for i in range(0,10): #display 10 games
        game_ids.append(matches['matches'][i]['gameId'])

    ranked_info = game_info_by_match_id(api_key, name, region,
                                        gamemode, game_ids[0]).rank_stats()
    ranked_info = pd.DataFrame(ranked_info)
    if ranked_info.empty:
        ranked_info = pd.DataFrame({'tier': ['unranked']})

    rank_league = ranked_info['tier'].values[0].lower()


    if rank_league == 'unranked':
        rank = "/static/images/ranked-emblems/hamster_cam.jpeg"
    else:
        rank = "/static/images/ranked-emblems/"+rank_league+".png"

    dfs = {}
    for gameid in game_ids:
        dfs[gameid] = game_info_by_match_id(api_key,
                                          name, region,
                                          gamemode, gameid).match_data()

    shap_plots = {}
    for b in dfs:
        shap_plots[b] = give_shap_plot(dfs[b], name)

    return render_template('public/liam.gg.html', rank=rank,
                                                  ranked_info=ranked_info,
                                                  game_ids = game_ids,
                                                  form = form,
                                                  dfs=dfs,
                                                  shap_plots = shap_plots,
                                                  name=name)


if __name__ == '__main__':
    app.run()
