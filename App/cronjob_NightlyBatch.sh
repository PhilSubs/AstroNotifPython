#!/bin/bash
#
# usage : ./cronjob_NightlyBatch.sh
#
#  Generate HTML file and bitmaps
#

main_function() {
    current_date_time="`date "+%Y-%m-%d %H:%M:%S"`"
    python nightlyBatchLog.py "resetTrace"
    python nightlyBatchLog.py "logToTrace" "Démarrage du script ($current_date_time)"
    python nightlyBatchLog.py "logToTrace" "Récupère le chemin du répertoire du script..."
    currentDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    python nightlyBatchLog.py "logToTrace" "&nbsp;&nbsp;&nbsp;&nbsp;--> le répertoire du script est : $currentDir"
    python nightlyBatchLog.py "logToTrace" "Se positionne dans le répertoire $currentDir ..."
    cd $currentDir
    python nightlyBatchLog.py "logToTrace" "Exécute le script nightlyBatchBitmap.py ...\n\n"
    
    python nightlyBatchBitmap.py
    
    python nightlyBatchLog.py "generateHTMLPageForTrace"
}

# log everything, but also output to stdout
#main_function 2>&1 | tee -a $fichierLog
main_function
