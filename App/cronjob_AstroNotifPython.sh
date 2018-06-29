#
# usage : ./cronjob_AstroNotifPython.sh <path_to_App>
#
#  Extract the deployment.xml file from component tarball in obedeliv
#
cd $1
python nightlyBatchBitmap.py
