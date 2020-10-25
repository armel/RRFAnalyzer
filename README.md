# RRFAnalyzer
Analyseur des statistiques d'utilisation du RRF.


# Crontab
À ajouter dans la crontab

```
export VISUAL=vi
```

```
*/15 * * * * /opt/RRFAnalyzer/back/RRFAnalyzer.sh prod quarter
*/30 * * * * /opt/RRFAnalyzer/back/RRFAnalyzer.sh prod half
00 */2 * * * /opt/RRFAnalyzer/back/RRFAnalyzer.sh prod hour
05 02 * * *  /opt/RRFAnalyzer/back/RRFAnalyzer.sh prod day
00 01 1 * *  /opt/RRFAnalyzer/back/RRFAnalyzer.sh prod month
```