#!/bin/sh
PATH_SCRIPT='/opt/RRFAnalyzer/back'
PATH_LOG='/var/www/RRFAnalyzer'

python3 $PATH_SCRIPT/RRFAnalyzer.py --room ALL --day 1 --format JSON > $PATH_LOG/RRFAnalyzer_d.json
python3 $PATH_SCRIPT/RRFAnalyzer.py --room ALL --week 0 --format JSON > $PATH_LOG/RRFAnalyzer_w.json
python3 $PATH_SCRIPT/RRFAnalyzer.py --room ALL --format JSON > $PATH_LOG/RRFAnalyzer_m.json
python3 $PATH_SCRIPT/RRFAnalyzer.py --room ALL --day 90 --format JSON > /$PATH_LOG/RRFAnalyzer_d90.json
python3 $PATH_SCRIPT/RRFAnalyzer.py --room ALL --day 180 --format JSON > $PATH_LOG/RRFAnalyzer_d180.json
python3 $PATH_SCRIPT/RRFAnalyzer.py --room ALL --day 240 --format JSON > $PATH_LOG/RRFAnalyzer_d240.json