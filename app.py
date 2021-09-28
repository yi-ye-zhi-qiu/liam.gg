#Import flask
from flask import *
from flask import Flask, render_template, request, jsonify, make_response

#import models
from models.liamometer import get_movie_data
from models.liam_gg import game_info_by_match_id

#import this for lieum.gg/liam.gg to work
from riotwatcher import LolWatcher, ApiError
import pandas as pd

from models.liam_gg_ml import give_shap_plot

#Shap visualization

import shap
from shap.plots._force_matplotlib import draw_additive_plot


app = Flask(__name__)

#Lieum.gg SEARCH page
@app.route('/league')
def show_league():
    return render_template('league.html')

#Lieum.gg POST-SEARCH page
@app.route('/league', methods=["GET", "POST"])
def riot_api_call():
    """
    Calls Riot API for recent n=10 games of user. Works only for NA region. (Can easily be changed via the 'region' variable defined below)
    Displays mostly-complete OP.gg clone, with a few features (like historical data for past seasons) missing.
    Runs Logistic Regression machine-learning model for each user game. The steps of that model are, for EACH game:
    - Check user rank (Gold I, etc.)
    - Check basic information (like rank and champion name, and CC Score)
    - Pass rank and champion name to liam_gg_ml.py
    - Construct dataframe by padding that user game with games from two tiers above and below current division Gold II, Gold III, Plat IV, and Plat III
    *(NOTE: for Challenger players, this would only be from Master, Diamond I)*
    - Filter by champion (i.e. Nocturne)
    - Filter by jungler or not (has smite or not) -- if so, add in 100 other Jungler games
    *(NOTE: If it's not jungle there is currently a major issue where data will be insufficient)*
    - Run a train/test split and logistic regression model (hyperparameters are not going to be tuned at all)
    - Use longest time living as % of the game as a primary key to search our model to find the game we want to make a SHAP plot for
    *(ASSUMPTION: Longest time spent living is such a unique number that you will not get multiple/duplicates in a dataframe the size of around 300 rows)*
    - Pass the model back to app.py, along with an index value that's for that specific game
    - Run a _force_plot_html function to generate a SHAP force plot for that specific game (displayed when user clicks 'BOOST STATS')
    """

    #Check if post method, if so store username searched as "name" variable
    if request.method == 'POST':
        form = request.form
    for key in form:
        name = form[key]

    #Define requisite variables for riot api call
    api_key = '' #get one @ https://developer.riotgames.com/
    region = 'na1' #this is only functional right now for North American data (LoL has European, Chinese, etc. servers)
    watcher = LolWatcher(api_key)
    #Define the user using python wrapper RiotWatcher for League of Legends data
    user = watcher.summoner.by_name('na1', name)
    #Get matchlist of the user
    matches = watcher.match.matchlist_by_account(region, user['accountId'])

    #get most recent 10 games of that user and the relevant GameIDs
    #change to 20, 30 if you want to display more data on the page
    #You may run into an API limit error doing that, though
    game_ids = []
    for i in range(0,10):
        game_ids.append(matches['matches'][i]['gameId'])

    ranked_info = game_info_by_match_id(api_key, name, region, game_ids[0]).rank_stats()
    ranked_info = pd.DataFrame(ranked_info)

    if ranked_info.empty:
        ranked_info = pd.DataFrame({'tier': ['unranked']})
    rank_league = ranked_info['tier'].values[0].lower()

    if rank_league == 'unranked':
        rank = "static/images/ranked-emblems/hamster_cam.jpeg"
    else:
        rank = "static/images/ranked-emblems/"+rank_league+".png"

    #Assemble dataframes for each GameID (1 api request per game)
    try:
        dfs = {}
        for gameid in game_ids:
            dfs[gameid] = game_info_by_match_id(api_key,
                                              name, region,
                                              gameid).match_data()
    except:
        return 'Sorry can you please try again in a few minutes? The non-developer process for Riot games is super slow and only allows one person at a time. Thanks...'


    #Assemble SHAP plots for each GameID (this is revealed by the show stats button)
    shap_plots = {}
    below_shap_html = {}
    show_below_plot = {}

    df_index = 0

    def _force_plot_html(explainer, shap_values, Xt, ind, champ, num_games, window, how_many_games_added):
        """
        We use a force plot, since no other graphs (beeswarm, bar plots for instance) can be generated.

        This code results in error:
        force_plot = shap.plots.beeswarm(shap_values)
        I think that no .html() method has been written for beeswarm plots.
        This code results in error:
        force_plot = shap.plots.bar(shap_values[ind])
        I think that no .html() method has been written for bar force plots.

        """
        try:
            ind = list(ind)[0]
            force_plot = shap.plots.force(shap_values[ind], matplotlib=False)
            shap_html = f"<head>{shap.getjs()}</head><body>{force_plot.html()}</body>"
            if count_given ==1:
                below_shap_html = '<button class="shap_plot_explanation"> What is this? </button><div class="explain_model is-hidden"><p>Analysis is of '+str(300-how_many_games_added)+' games as '+champ+' padded with ' + str(how_many_games_added) +' other games (if jungle => of junglers else nothing is padded) in divisions '+str(window)+'. The number on top of the graph represents: how likely or unlikely was this game to happen at all, given our data model?</p><p>Data is based off your past game data combined with anyone within 2 divisions of your rank (last updated patch 11.4), and 20-30% of sample data is just for that champion.</p><p>The <span style="background-color: rgb(255, 13, 87); color: white;">red bars</span> and their relative sizes indicate which things about this game DID help your log-odds chances of winning this game and by how much, and the <span style="background-color: rgb(30, 136, 229); color: white;">blue bars</span> are what aspects DID NOT help your log-odds chances and by how much.</p></div>'
            elif count_given ==0:
                below_shap_html = '<button class="shap_plot_explanation"> What is this? </button><div class="explain_model is-hidden"><p>Analysis is of '+str(how_many_games_added)+' games as '+champ+' padded with ' + str(0) +' other games (if jungle => of junglers else nothing is padded) in divisions '+str(window)+'. The number on top of the graph represents: how likely or unlikely was this game to happen at all, given our data model?</p><p>Data is based off your past game data combined with anyone within 2 divisions of your rank (last updated patch 11.4), and 20-30% of sample data is just for that champion.</p><p>The <span style="background-color: rgb(255, 13, 87); color: white;">red bars</span> and their relative sizes indicate which things about this game DID help your log-odds chances of winning this game and by how much, and the <span style="background-color: rgb(30, 136, 229); color: white;">blue bars</span> are what aspects DID NOT help your log-odds chances and by how much.</p></div>'
            show_below_plot = 1
            return shap_html, below_shap_html, show_below_plot
        except:
            shap_html = ''
            below_shap_html = '<div class="explain_model"><p>Since this is not a ranked game, no advanced stats are computed. </br> 由于这个游戏不是ranked的类型，没有stats。</p></div>'
            show_below_plot = 0
            return shap_html, below_shap_html, show_below_plot

    for b in dfs:
        a = dfs[b]
        print('[PASSED VARIABLE] Champion: ', a.loc[a['summonerName'] == name]['championName'].values[0])
        print('[PASSED VARIABLE] Longest time living as % of game (primary key):', a.loc[a['summonerName'] == name]['longestTimeSpentLiving'].values[0])
        champ = a.loc[a['summonerName'] == name]['championName'].values[0]
        primary_key = a.loc[a['summonerName'] == name]['longestTimeSpentLiving'].values[0]

        model, Xt, Xv, X_, index_label, num_games, window, how_many_games_added, count_given = give_shap_plot(name, dfs[b], ranked_info, df_index, dfs, champ, primary_key)
        #If you're running XGBoost, RandomForest:
        #explainer = shap.TreeExplainer(model)
        #shap_values = explainer.shap_values(Xv)
        explainer = shap.Explainer(model, X_, feature_names=Xt.columns)
        shap_values = explainer(X_)
        shap_plots[b], below_shap_html[b], show_below_plot[b] = _force_plot_html(explainer, shap_values, X_, index_label, champ, num_games, window, how_many_games_added)

    #load liam.gg.html, but pass all of our variables as needed by Django
    return render_template('public/liam.gg.html', rank=rank,
                                                  ranked_info=ranked_info,
                                                  game_ids = game_ids,
                                                  form = form,
                                                  dfs=dfs,
                                                  shap_plots = shap_plots,
                                                  below_shap_html = below_shap_html,
                                                  show_below_plot = show_below_plot,
                                                  name=name)


if __name__ == '__main__':
    app.run()
