# RRFAnalyzer
Analyseur des statistiques d'utilisation du RRF.


# Crontab
À ajouter dans la crontab

```
*/15 * * * * python3 /opt/RRFAnalyzer/back/RRFAnalyzer.py --room ALL --day 1 --format JSON > /var/www/RRFAnalyzer/RRFAnalyzer_d.json
*/30 * * * * python3 /opt/RRFAnalyzer/back/RRFAnalyzer.py --room ALL --week 0 --format JSON > /var/www/RRFAnalyzer/RRFAnalyzer_w.json
00 */2 * * * python3 /opt/RRFAnalyzer/back/RRFAnalyzer.py --room ALL --format JSON > /var/www/RRFAnalyzer/RRFAnalyzer_m.json
05 02 * * * /opt/RRFAnalyzer/back/RRFAnalyzer_daily.sh
00 01 1 * * /opt/RRFAnalyzer/back/RRFAnalyzer_monthly.sh```