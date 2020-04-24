#!/bin/sh

python /opt/RRFAnalyzer/back/analyzer.py --room ALL --day 1 --format JSON > /var/www/RRFAnalyser/analyzer_1.json
python /opt/RRFAnalyzer/back/analyzer.py --room ALL --week 0 --format JSON > /var/www/RRFAnalyser/analyzer_7.json
python /opt/RRFAnalyzer/back/analyzer.py --room ALL --format JSON > /var/www/RRFAnalyser/analyzer_30.json
python /opt/RRFAnalyzer/back/analyzer.py --room ALL --day 90 --format JSON > /var/www/RRFAnalyser/analyzer_90.json
python /opt/RRFAnalyzer/back/analyzer.py --room ALL --day 180 --format JSON > /var/www/RRFAnalyser/analyzer_180.json