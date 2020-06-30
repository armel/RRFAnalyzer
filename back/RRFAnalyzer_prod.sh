#!/bin/sh
PATH_SCRIPT='/opt/RRFAnalyzer/back'
PATH_LOG='/var/www/RRFAnalyzer'

python3 $PATH_SCRIPT/RRFAnalyzer.py --room ALL --day 1 --format JSON > $PATH_LOG/RRFAnalyzer_d.json
python3 $PATH_SCRIPT/RRFAnalyzer.py --room ALL --week 0 --format JSON > $PATH_LOG/RRFAnalyzer_w.json
python3 $PATH_SCRIPT/RRFAnalyzer.py --room ALL --format JSON > $PATH_LOG/RRFAnalyzer_m.json
python3 $PATH_SCRIPT/RRFAnalyzer.py --room ALL --month -1 --format JSON > $PATH_LOG/RRFAnalyzer_m1.json
python3 $PATH_SCRIPT/RRFAnalyzer.py --room ALL --month -2 --format JSON > $PATH_LOG/RRFAnalyzer_m2.json
python3 $PATH_SCRIPT/RRFAnalyzer.py --room ALL --month -3 --format JSON > $PATH_LOG/RRFAnalyzer_m3.json
python3 $PATH_SCRIPT/RRFAnalyzer.py --room ALL --month -4 --format JSON > $PATH_LOG/RRFAnalyzer_m4.json
python3 $PATH_SCRIPT/RRFAnalyzer.py --room ALL --month -5 --format JSON > $PATH_LOG/RRFAnalyzer_m5.json
python3 $PATH_SCRIPT/RRFAnalyzer.py --room ALL --month -6 --format JSON > $PATH_LOG/RRFAnalyzer_m6.json
python3 $PATH_SCRIPT/RRFAnalyzer.py --room ALL --month -7 --format JSON > $PATH_LOG/RRFAnalyzer_m7.json
python3 $PATH_SCRIPT/RRFAnalyzer.py --room ALL --month -8 --format JSON > $PATH_LOG/RRFAnalyzer_m8.json
python3 $PATH_SCRIPT/RRFAnalyzer.py --room ALL --month -9 --format JSON > $PATH_LOG/RRFAnalyzer_m9.json
python3 $PATH_SCRIPT/RRFAnalyzer.py --room ALL --month -10 --format JSON > $PATH_LOG/RRFAnalyzer_m10.json
python3 $PATH_SCRIPT/RRFAnalyzer.py --room ALL --day 60 --format JSON > /$PATH_LOG/RRFAnalyzer_d60.json
python3 $PATH_SCRIPT/RRFAnalyzer.py --room ALL --day 120 --format JSON > /$PATH_LOG/RRFAnalyzer_d120.json
python3 $PATH_SCRIPT/RRFAnalyzer.py --room ALL --day 180 --format JSON > $PATH_LOG/RRFAnalyzer_d180.json
python3 $PATH_SCRIPT/RRFAnalyzer.py --room ALL --day 240 --format JSON > $PATH_LOG/RRFAnalyzer_d240.json
python3 $PATH_SCRIPT/RRFAnalyzer.py --room ALL --day 300 --format JSON > $PATH_LOG/RRFAnalyzer_d300.json
