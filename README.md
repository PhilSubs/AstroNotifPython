# AstroNotifPython v1.8
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

 - Dans le répertoire `[CheminAPP]`:
 
   **Mettre a jour les fichiers JSON avec les nouvelles versions**

   - Verifier le contenu du fichier **`parameters_Places.json`** par rapport au fichier **`parameters_Places.default.json`** 
   - Verifier le contenu du fichier **`parameters_Runtime.json`** par rapport au fichier **`parameters_Runtime.default.json`** 
   - Verifier le contenu du fichier **`parameters_Rendering.json`** par rapport au fichier **`parameters_Rendering.default.json`** 
   - Verifier le contenu du fichier **`parameters_SkyObjects.json`** par rapport au fichier **`parameters_SkyObjects.default.json`** 
   - Verifier le contenu du fichier **`parameters_LunarFeatures.json`** par rapport au fichier **`parameters_LunarFeatures.default.json`** 

 - Copier le contenu du répertoire **`www`** dans **`[CheminWWW]`**


## Nouvelle installation

 - Copier le contenu du répertoire **`App`** dans **`[CheminAPP]`**

 - Copier le contenu du répertoire **`www`** dans **`[CheminWWW]`**

 - Dans le répertoire `[CheminAPP]`:

   - copier le fichier **`parameters_Places.default.json`** vers **`parameters_Places.json`**
   - copier le fichier **`parameters_Runtime.default.json`** vers **`parameters_Runtime.json`**
   - copier le fichier **`parameters_Rendering.default.json`** vers **`parameters_Rendering.json`**
   - copier le fichier **`parameters_SkyObjects.default.json`** vers **`parameters_SkyObjects.json`**
   - copier le fichier **`parameters_LunarFeatures.default.json`** vers **`parameters_LunarFeatures.json`**
   
   - modifier le fichier **`parameters_Places.json`**
     - renseigner les longitude et latitude pour les lieux déclarés:
       - "Longitude":0.000000000
       - "Latitude":0.000000000 
     - renommer les lieux comme il convient, notamment celui qui sera utilisé pour le calcul **`[nomDuLieu]`**.
    
   - modifier le fichier **`parameters_Runtime.json`**
     - "GlobalPathToWWWFolder":"**`[CheminWWW]`**"
     - "GlobalPathToAPPFolder":"**`[CheminAPP]`**"
     - "ObservationPlaceName":"**`[nomDuLieu]`**"
     - "NightlyBatchEmailAddress":"email@domain.com"   (email destinataire de la notification par mail)
     - "NightlyBatchEmailSMTPServer":"server.domain.com"  (nom du serveur SMTP, ex: smtp.gmail.com)
     - "NightlyBatchEmailSMTPUser":"username"  (username du compte envoyant le mail)
     - "NightlyBatchEmailSMTPPassword":"password"  (password du compte envoyant le mail)
     - "NightlyBatchEmailFromAddress":"AstroNotif<email@domain.com>"   (email d'origine de la notification par mail)
     - "NightlyBatchDomain":"IP or URL"   (Addresse IP ou url du domaine hebergeant l'application)

 - Ajouter une tâche récurrente pour calculer les éphémérides tous les jours:
 
   - dans une fenêtre schell:
     - Ajouter l'attribut X sur le script shell par la commande:
         `chmod +x [CheminAPP]/cronjob_NightlyBatch.sh`
     - taper la commande `crontab -e`
     - entrer la ligne suivante :
        `0 4 * * [CheminAPP]/cronjob_NightlyBatch.sh`
     - sauvegarder par `CTRL-O`
     - quitter par `CTRL-X`
