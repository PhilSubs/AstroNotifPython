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


## Installation d'une mise à jour

 - Copier le contenu du répertoire **`App`** dans **`[CheminAPP]`**
     **ATTENTION: _ne pas écraser le fichier parameters_Places.json._**

 - Copier le contenu du répertoire **`www`** dans **`[CheminWWW]`**


## Nouvelle installation

 - Copier le contenu du répertoire **`App`** dans **`[CheminAPP]`**

 - Copier le contenu du répertoire **`www`** dans **`[CheminWWW]`**

 - Dans le répertoire `[CheminAPP]`:

   - modifier le fichier **`parameters_Places.json`**
     - renseigner les longitude et latitude pour les lieux déclarés:
        "Longitude":0.000000000
        "Latitude":0.000000000 
     - renommer les lieux comme il convient, notamment celui qui sera utilisé pour le calcul **`[nomDuLieu]`**.
    
   - modifier le fichier **`parameters_Runtime.json`**
     - "GlobalPathToWWWFolder":"**`[CheminWWW]`**"
     - "GlobalPathToAPPFolder":"**`[CheminAPP]`**"
     - "ObservationPlaceName":"**`[nomDuLieu]`**"

 - Ajouter une tâche récurrente pour calculer les éphémérides tous les jours:
 
   - dans une fenêtre schell:
     - Ajouter l'attribut X sur le script shell par la commande:
         `chmod +x **[CheminAPP]**/cronjob_NightlyBatch.sh`
     - taper la commande `crontab -e`
     - entrer la ligne suivante :
        `0 4 * * [CheminAPP]/cronjob_NightlyBatch.sh`
     - sauvegarder par `CTRL-O`
     - quitter par `CTRL-X`
