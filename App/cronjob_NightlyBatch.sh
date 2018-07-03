#!/bin/bash
#
# usage : ./cronjob_NightlyBatch.sh
#
#  Generate HTML file and bitmaps
#
fichierLog="/var/www/html/nightlyBatch_log.html"
if [ -f $fichierLog ] ; then
    logDelete="&nbsp;&nbsp;&nbsp;&nbsp;--> le fichier '$fichierLog' existe:  on le supprime....<BR>"
    rm $fichierLog
else
    logDelete="&nbsp;&nbsp;&nbsp;&nbsp;--> le fichier '$fichierLog' n'existe pas....<BR>"
fi

main_function() {
    current_date_time="`date "+%Y-%m-%d %H:%M:%S"`"
    echo "Démarrage du script ($current_date_time) <BR><BR>"
    echo "<BR>"
    echo "----------------------------------------------------------------<BR>"
    echo "<BR>"
    echo "Suppression du fichier de log '$fichierLog' ...<BR>"
    echo "$logDelete <BR>"
    echo "Récupère le chemin du répertoire du script...<BR>"
    currentDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    echo "&nbsp;&nbsp;&nbsp;&nbsp;--> le répertoire du script est : $currentDir <BR>"
    echo "<BR>"
    echo "Se positionne dans le répertoire $currentDir ...<BR>"
    cd $currentDir
    echo "<BR>"
    echo "Répertoire courant :<BR>"
    echo "&nbsp;&nbsp;&nbsp;&nbsp;--> "
    pwd
    echo "<BR>"
    echo "<BR>"
    echo "Exécute le script nightlyBatchBitmap.py ...<BR>"
    echo "<BR>"
    echo "<BR>"
    echo "----------------------------------------------------------------<BR>"
    echo "<BR>"
    echo "<BR>"
    python nightlyBatchBitmap.py
}

# log everything, but also output to stdout
main_function 2>&1 | tee -a $fichierLog
