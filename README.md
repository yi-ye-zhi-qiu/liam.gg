## lieum.gg ![Python version](https://img.shields.io/badge/python-%E2%89%A53.6-blue.svg?style=flat-square&logo=python&logoColor=white)

### League of Legends (LoL) win interpreter with the aim of connecting LoL players with their data using XGBoost classifier

![Metis logo](static/images/metis.png) Metis data-science bootcamp project 3, **Jan. 23 - Feb 10 2021**

** [See the final product](http://34.212.100.77/portfolio) ** (*Note*: as I apply for a production key, it's likely that since my API requests are so limited you might have to retry over and over again.)
** Project was presented, [slides used](final_presentation.pdf) **

**Summary:**  FlaskApp where users can search by League of Legends username and view baseline match data (like op.gg) that's fetched from the RiotWatcher League of Legends API; in addition, users can click "boost stats" which will reveal a SHAP force plot of features that interpret a XGBoost model trained on 100k rows of Korean pro solo-queue games. XGBoost's hyperparameters were tuned using hyperopt library. Other model approaches (RandomForest tuned via GridSearchCV) were evaluated.

----

Contributors:
- Liam

----

Requirements to run locally:

The data:

- [Link to Kaggle dataset](https://www.kaggle.com/gyejr95/league-of-legendslol-ranked-games-2020-ver1), ~100k rows of Korean solo-queue League games from patches 10.3 or so.

The data analysis:

- `Python 3.6` or greater
- `jupyter notebook`
- `riotwatcher`
- `Flask`
- `shap`
- `xgboost`
- `hyperopt`
- other modules: `pandas` `scikit-learn` `matplotlib` `seaborn` `numpy` `io` `base64`
- ~5 hours of time start to finish to run/set-up

The WebApp:

- The FlaskApp is running on Ubuntu on an AWS AmazonLightsail server, but you can easily reproduce on local host by running `Flask run app.py`

----

Project Map   

This project is split into data modeling from our dataset and live API calls to Riot Games servers each time you search a league name. This is reflected in our final product as the op.gg-like baseline data, and the SHAP force plots below: that's two separate functions.

Data modeling from dataset:

- Documented in `analysis.ipynb`,
- Defined in `liam_gg_ml.py`, called by `app.py`

Data collection from API call:

- `liam_gg.py`, called by `app.py`, search for username made in `templates/league.html` and data displayed in `templates/public/liam.gg.html`
