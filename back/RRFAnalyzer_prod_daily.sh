#!/bin/sh
PATH_SCRIPT='/opt/RRFAnalyzer/back'
PATH_LOG='/var/www/RRFAnalyzer'

python3 $PATH_SCRIPT/RRFAnalyzer.py --room ALL --day 1 --format JSON > $PATH_LOG/RRFAnalyzer_d.json
python3 $PATH_SCRIPT/RRFAnalyzer.py --room ALL --week 0 --format JSON > $PATH_LOG/RRFAnalyzer_w.json
python3 $PATH_SCRIPT/RRFAnalyzer.py --room ALL --format JSON > $PATH_LOG/RRFAnalyzer_m.json
python3 $PATH_SCRIPT/RRFAnalyzer.py --room ALL --day 60 --format JSON > $PATH_LOG/RRFAnalyzer_d60.json
python3 $PATH_SCRIPT/RRFAnalyzer.py --room ALL --day 120 --format JSON > $PATH_LOG/RRFAnalyzer_d120.json
python3 $PATH_SCRIPT/RRFAnalyzer.py --room ALL --day 180 --format JSON > $PATH_LOG/RRFAnalyzer_d180.json
python3 $PATH_SCRIPT/RRFAnalyzer.py --room ALL --day 240 --format JSON > $PATH_LOG/RRFAnalyzer_d240.json
python3 $PATH_SCRIPT/RRFAnalyzer.py --room ALL --day 300 --format JSON > $PATH_LOG/RRFAnalyzer_d300.json
python3 $PATH_SCRIPT/RRFAnalyzer.py --room ALL --day 360 --format JSON > $PATH_LOG/RRFAnalyzer_d360.json
