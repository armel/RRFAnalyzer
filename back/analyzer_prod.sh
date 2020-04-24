#!/bin/sh

PATH_LOG='/var/www/RRFAnalyzer'

python /opt/RRFAnalyzer/back/analyzer.py --room ALL --day 1 --format JSON > $PATH_LOG/analyzer_d1.json
python /opt/RRFAnalyzer/back/analyzer.py --room ALL --week 0 --format JSON > $PATH_LOG/analyzer_w.json
python /opt/RRFAnalyzer/back/analyzer.py --room ALL --format JSON > $PATH_LOG/analyzer_m.json
python /opt/RRFAnalyzer/back/analyzer.py --room ALL --month -1 --format JSON > $PATH_LOG/analyzer_m1.json
python /opt/RRFAnalyzer/back/analyzer.py --room ALL --month -2 --format JSON > $PATH_LOG/analyzer_m2.json
python /opt/RRFAnalyzer/back/analyzer.py --room ALL --month -3 --format JSON > $PATH_LOG/analyzer_m3.json
python /opt/RRFAnalyzer/back/analyzer.py --room ALL --month -4 --format JSON > $PATH_LOG/analyzer_m4.json
python /opt/RRFAnalyzer/back/analyzer.py --room ALL --month -5 --format JSON > $PATH_LOG/analyzer_m5.json
python /opt/RRFAnalyzer/back/analyzer.py --room ALL --month -6 --format JSON > $PATH_LOG/analyzer_m6.json
python /opt/RRFAnalyzer/back/analyzer.py --room ALL --day 90 --format JSON > /$PATH_LOG/analyzer_d90.json
python /opt/RRFAnalyzer/back/analyzer.py --room ALL --day 180 --format JSON > $PATH_LOG/analyzer_d180.json