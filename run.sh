scrapy crawl leaderboards --output "feed/%(name)s-%(time)s.json" --output-format json -L WARN
python3 preprocess/leaderboards.py
scrapy crawl profiles --output "feed/%(name)s-%(time)s.json" --output-format json -L WARN
python3 preprocessors/profiles.py
python3 ml/shap.py
