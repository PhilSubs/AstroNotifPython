#
# usage : ./cronjob_AstroNotifPython.sh <path_to_App>
#
#  Generate HTML file and bitmaps
#
cd $1
python nightlyBatchBitmap.py
