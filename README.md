# AstroNotifPython
Notify Astronomy objects observability

# Pré-requis:
 - Python 2.7
 - Librairie PIL

# Structure des répertoires:
 La delivery contient trois répertoires:
 - **`App`**: contient les scripts Python, les fichiers de paramètres JSON, les fontes nécessaires.
 - **`www`**: contient un fichier favicon
 - **`Documentation`**: contient la documentation

# Installation
L'application a besoin de connaitre le répertoire où elle est installée, ainsi que le répertoire qui contiendra les fichiers HTML et bitmap générés:
 - **`[CheminAPP]`** : répertoire d'installation de l'application (chemin vers le répertoir App)
 - **`[CheminWWW]`** : répertoire contenant les fichiers HTML et bitmap

**ATTENTION: En cas d'installation d'une mise à jour:** _attention à ne pas écraser le fichier **parameters_Places.json**._

## Dans le répertoire App:
 - modifier le fichier **`parameters_Places.json`**
   - renseigner les longitude et latitude pour les lieux déclarés:
      "Longitude":0.000000000
      "Latitude":0.000000000 
   - renommer les lieux comme il convient, notamment celui qui sera utilisé pour le calcul **`[nomDuLieu]`**.
 - modifier le fichier **`parameters_Runtime.json`**
   - "GlobalPathToWWWFolder":"**`[CheminWWW]`**"
   - "GlobalPathToAPPFolder":"**`[CheminAPP]`**"
   - "ObservationPlaceName":"**`[nomDuLieu]`**"

## Ajouter une tâche récurrente pour calculer les éphémérides tous les jours:
 - dans une fenêtre schell:
   - `chmod +x **[CheminAPP]**/cronjob_AstroNotifPython.sh`
   - taper la commande `crontab -e`
   - entrer la ligne suivante :
        `0 4 * * [CheminAPP]/cronjob_AstroNotifPython.sh > [CheminWWW]/lastRun.log`
   - sauvegarder par `CTRL-O`
   - quitter par `CTRL-X`
  
## Copier le contenu du répertoire www dans [CheminWWW]
