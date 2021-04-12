## liam.gg ![Python version](https://img.shields.io/badge/python-%E2%89%A53.6-blue.svg?style=flat-square&logo=python&logoColor=white)

### League of Legends (LoL) win interpreter WebApp with the aim of connecting LoL players with their data using logistic regression

![Metis logo](static/images/metis.png) Metis data-science bootcamp project 3, **Jan. 23 - Feb 10 2021**

[See the final product](http://liamisaacs.com/league)

[Read the blog post](https://yeqiuu.medium.com/the-heartfelt-story-of-me-building-a-league-of-legends-win-interpreter-for-hard-stuck-silver-ii-36684c99facc)

(*Note*: as I apply for a production key, it's likely that since my API requests are so limited you might have to retry over and over again.)

Project was presented, [slides!](final_presentation.pdf)

**Summary:**  FlaskApp where users can search by League of Legends username and view baseline match data (like op.gg) that's fetched from the RiotWatcher League of Legends API; in addition, users can click "boost stats" which will reveal a SHAP force plot of features that interpret a logistic regression model trained on data that's local to that user (based off rank, champion, role).

----

Contributors:
- Liam

----

Requirements to run locally:
- `Python 3.6` or greater
- `jupyter notebook`
- `RiotWatcher` `Riot APIs`
- `Flask`
- `shap`
- `logistic regression`
- other modules: `pandas` `scikit-learn` `numpy`

----

The data:

- Please message me if you're interested in the source data used.

----

The process:

- The basic idea is a Flask form submission of the user name in `templates/league.html`
- Using that name, in `app.py` we:
```
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
```

----

The WebApp itself:

- The FlaskApp is running on Ubuntu on an AWS AmazonLightsail server (more on that in my [personalwebsite repository](https://github.com/yi-ye-zhi-qiu/personalwebsite)), but you can easily reproduce on local host by running `Flask run app.py` or, if you use Atom IDE, `Command+i` in the `app.py` file
