#!/bin/sh

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

array=( 0 1 )

for var in "${array[@]}"
do
    if [ $var = 0 ]
    then
        room='ALL'
    else
        room='EXTRA'
    fi

    case "$WHEN" in
        quarter)
            echo "Compute Quarter on $WHERE"
            python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --day 1      --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_d_${var}.json
            ;;
        half)
            echo "Compute Half on $WHERE"
            python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --week 0     --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_w_${var}.json
            ;;
        hour)
            echo "Compute Hourly on $WHERE"
            python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --month 0    --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_m_${var}.json
            ;;
        daily)
            echo "Compute Daily on $WHERE"
            python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --day 60     --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_d60_${var}.json
            python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --day 120    --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_d120_${var}.json
            python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --day 180    --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_d180_${var}.json
            python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --day 240    --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_d240_${var}.json
            python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --day 300    --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_d300_${var}.json
            python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --day 360    --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_d360_${var}.json
            ;;
        monthly)
            echo "Compute Monthly on $WHERE"
            python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --month -1   --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_m1_${var}.json
            python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --month -2   --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_m2_${var}.json
            python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --month -3   --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_m3_${var}.json
            python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --month -4   --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_m4_${var}.json
            python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --month -5   --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_m5_${var}.json
            python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --month -6   --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_m6_${var}.json
            python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --month -7   --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_m7_${var}.json
            python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --month -8   --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_m8_${var}.json
            python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --month -9   --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_m9_${var}.json
            python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --month -10  --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_m10_${var}.json
            python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --month -11  --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_m11_${var}.json
            python3 $PATH_SCRIPT/RRFAnalyzer.py --room $room --month -12  --format JSON --path $PATH_DATA > $PATH_LOG/RRFAnalyzer_m12_${var}.json
            ;;
        esac
done
