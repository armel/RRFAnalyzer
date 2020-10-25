#!/bin/sh

# 
# */15 * * * * /opt/RRFAnalyzer/back/RRFAnalyzer.sh prod quarter
# */30 * * * * /opt/RRFAnalyzer/back/RRFAnalyzer.sh prod half
# 00 */2 * * * /opt/RRFAnalyzer/back/RRFAnalyzer.sh prod hour
# 05 02 * * *  /opt/RRFAnalyzer/back/RRFAnalyzer.sh prod day
# 00 01 1 * *  /opt/RRFAnalyzer/back/RRFAnalyzer.sh prod month
#

# Set default values

if [ -z "$1" ]
then
    WHERE='local'
    WHEN='quarter'
else
    WHERE=$1
    WHEN='quarter'
fi

if [ -z "$2" ]
then
    WHEN='quarter'
else
    WHEN=$2
fi

room='EXTRA'

case "$WHERE" in
    local)
        PATH_SCRIPT='/Users/armel/Dropbox/RRFAnalyzer/back'
        PATH_DATA='/Users/armel/Sites/RRFTracker/'
        PATH_LOG='/Users/armel/Sites/RRFAnalyzer'
        ;;
    prod)
        PATH_SCRIPT='/opt/RRFAnalyzer/back'
        PATH_DATA='/var/www/RRFTracker/'
        PATH_LOG='/var/www/RRFAnalyzer'
        ;;
    esac

case "$WHEN" in
    quarter)
        echo "Compute Quarter on $WHERE"
        python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --day 1      --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_d.json
        ;;
    half)
        echo "Compute Half on $WHERE"
        python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --week 0     --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_w.json
        ;;
    hour)
        echo "Compute Hourly on $WHERE"
        python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --month 0    --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_m.json
        ;;
    day)
        echo "Compute Daily on $WHERE"
        python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --day 60     --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_d60.json
        python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --day 120    --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_d120.json
        python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --day 180    --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_d180.json
        python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --day 240    --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_d240.json
        python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --day 300    --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_d300.json
        python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --day 360    --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_d360.json
        ;;
    month)
        echo "Compute Monthly on $WHERE"
        python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --month -1   --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_m1.json
        python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --month -2   --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_m2.json
        python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --month -3   --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_m3.json
        python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --month -4   --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_m4.json
        python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --month -5   --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_m5.json
        python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --month -6   --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_m6.json
        python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --month -7   --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_m7.json
        python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --month -8   --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_m8.json
        python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --month -9   --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_m9.json
        python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --month -10  --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_m10.json
        python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --month -11  --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_m11.json
        python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --month -12  --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_m12.json
        ;;
    esac
