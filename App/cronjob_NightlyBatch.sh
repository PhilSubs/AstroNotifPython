#!/bin/bash
#
# usage : ./cronjob_NightlyBatch.sh
#
#  Generate HTML file and bitmaps
#

main_function() {
    current_date_time="`date "+%Y-%m-%d %H:%M:%S"`"
    python nightlyBatchLog.py "resetTrace"
    python nightlyBatchLog.py "logToTrace" "Start nightly batch script ($current_date_time)"
    python nightlyBatchLog.py "logToTrace" "Get path to script folder..."
    currentDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    python nightlyBatchLog.py "logToTrace" "&nbsp;&nbsp;&nbsp;&nbsp;--> script folder is : $currentDir"
    python nightlyBatchLog.py "logToTrace" "Set current dir to $currentDir ..."
    cd $currentDir
    python nightlyBatchLog.py "logToTrace" "Run script nightlyBatchBitmap.py ...\n\n"
    
    python nightlyBatchBitmap.py
    
    python nightlyBatchLog.py "logToTrace" "Generate html trace file ...\n"
    python nightlyBatchLog.py "generateHTMLPageForTrace"
}

# log everything, but also output to stdout
#main_function 2>&1 | tee -a $fichierLog
main_function
