#
# usage : ./cronjob_AstroNotifPython.sh
#
#  Generate HTML file and bitmaps
#
currentDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $currentDir
python nightlyBatchBitmap.py
