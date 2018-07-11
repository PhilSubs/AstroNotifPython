#!/usr/bin/python2.7
# -*-coding:Latin-1 -*

# Import libs for ephemerides
import json
from datetime import datetime, timedelta
import ANLib
import os.path

    
def updateDictValues(sJsonFilename, sLevel, dictData, dictDataDefault):
    bChangeDone = False
    sFormattedFilename = ("                          " + sJsonFilename)[-30:]
    for iId in range (0, len(dictDataDefault)):
        sKeyLabel = list(dictDataDefault.keys())[iId]
        sFormattedKeyLabel = ("'" + sLevel + sKeyLabel + "'                                ")[-0:40]
        if sKeyLabel == "currentVersion" and sJsonFilename == "parameters_Runtime.json":
            dictData[sKeyLabel] = dictDataDefault[sKeyLabel]
            bChangeDone = True
            sFormattedNewValue = dictData[sKeyLabel]
            if type(sFormattedNewValue) is unicode:
                sFormattedNewValue.encode("iso-8859-1" )
            elif not(type(sFormattedNewValue) is str): 
                sFormattedNewValue = str(sFormattedNewValue)
            print "      " + sFormattedFilename + ":     " + sFormattedKeyLabel + "    -->   " + sFormattedNewValue
        elif sKeyLabel == "GlobalPathToAPPFolder" and sJsonFilename == "parameters_Runtime.json":
            dictData[sKeyLabel] = ANLib.Tools.get_script_path()
            bChangeDone = True
            sFormattedNewValue = dictData[sKeyLabel]
            if type(sFormattedNewValue) is unicode:
                sFormattedNewValue.encode("iso-8859-1" )
            elif not(type(sFormattedNewValue) is str): 
                sFormattedNewValue = str(sFormattedNewValue)
            print "      " + sFormattedFilename + ":     " + sFormattedKeyLabel + "    -->   " + sFormattedNewValue
        else:
            if sKeyLabel in dictData:
                if type(dictDataDefault[sKeyLabel]) is dict:
                    bSubChangeDone, dictData[sKeyLabel] = updateDictValues(sJsonFilename, sLevel + sKeyLabel + ".", dictData[sKeyLabel], dictDataDefault[sKeyLabel])
                    if bSubChangeDone: bChangeDone = True
                else:
                    sCurrentValue = dictData[sKeyLabel]
                    if type(sCurrentValue) is unicode:
                        sCurrentValue.encode("iso-8859-1" )
                    elif not(type(sCurrentValue) is str): 
                        sCurrentValue = str(sCurrentValue)
                    sDefaultValue = dictDataDefault[sKeyLabel]
                    if type(sDefaultValue) is unicode:
                        sCurrentValue.encode("iso-8859-1" )
                    elif not(type(sDefaultValue) is str): 
                        sDefaultValue = str(sDefaultValue)
                    if dictData[sKeyLabel] != dictDataDefault[sKeyLabel]:
                        print "      " + sFormattedFilename + ":  #  " + sFormattedKeyLabel + "          " + sCurrentValue + "    <-->    " +  sDefaultValue
            else:
                dictData[sKeyLabel] = dictDataDefault[sKeyLabel]
                bChangeDone = True
                sFormattedNewValue = dictDataDefault[sKeyLabel]
                if type(sFormattedNewValue) is unicode:
                    sFormattedNewValue.encode("iso-8859-1" )
                elif not(type(sFormattedNewValue) is str): 
                    sFormattedNewValue = str(sFormattedNewValue)
                print "      " + sFormattedFilename + ":     " + sFormattedKeyLabel + "    -->   " + sFormattedNewValue
    return bChangeDone, dictData

def updateParameterFile(sJsonDefaultFilename):
    sJsonFilename = sJsonDefaultFilename.replace(".default.json",".json")
    print "      Fichier  " + sJsonFilename
    if os.path.isfile(ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + sJsonFilename):
        with open(ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + sJsonFilename, 'r') as fParametersFile:
            dataParametersRuntime = json.load(fParametersFile)
        with open(ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + sJsonDefaultFilename, 'r') as fParametersDefaultFile:
            dataParametersRuntimeDefault = json.load(fParametersDefaultFile)
        # update parameters
        bChangeDone, dataParametersRuntime = updateDictValues(sJsonFilename, "", dataParametersRuntime, dataParametersRuntimeDefault)
        # write JSON file
        print ""
        if bChangeDone:
            try:
                with open(ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + sJsonFilename, "w") as fParametersFile:
                    json.dump(dataParametersRuntime, fParametersFile)
                bResult = True
                print "             --> fichier  " + sJsonFilename + "   modifie."
            except:
                print "             >>> erreur lors de la modification du fichier  " + sJsonFilename
                bResult = False
        else:
            print "             --> pas de modifications."
            bResult = True
    print ""
    print ""
    return bResult
    
print ""
print ""
print ""
print "Installation ASTRONOTIF python"
print "=============================="
print ""
print ""

# Récupération des versions
sUpgradeFromVersion = ""
if os.path.isfile(ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_Runtime.json'):
    with open('parameters_Runtime.json', 'r') as fParametersRuntime:
        dataParametersRuntime = json.load(fParametersRuntime)
    sUpgradeFromVersion = dataParametersRuntime['currentVersion']
# load parameters file default
with open('parameters_Runtime.default.json', 'r') as fParametersRuntimeDefault:
    dataParametersRuntimeDefault = json.load(fParametersRuntimeDefault)
sNewVersion = dataParametersRuntimeDefault['currentVersion']

# Afficher du message de changement de version
if sUpgradeFromVersion == "":
    print "Nouvelle installation en version " + sNewVersion
else:
    print "Mise a jour de la version " + sUpgradeFromVersion + " vers la version " + sNewVersion
print ""

# copy de backup des fichiers existants (suffixe: version précédente)
if sUpgradeFromVersion != "":
    print ""
    print "   BACKUP DES FICHIERS DE PARAMETRES"
    print ""
    bIsBackupOk = True
    sBackupSuffix = '.back-' + sUpgradeFromVersion
    if os.path.isfile(ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_Runtime.json'):
        bIsBackupOk = bIsBackupOk and ANLib.Tools.backupFile(ANLib.Tools.get_script_path(), 'parameters_Runtime.json', sBackupSuffix)
    if os.path.isfile(ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_Rendering.json'):
        bIsBackupOk = bIsBackupOk and ANLib.Tools.backupFile(ANLib.Tools.get_script_path(), 'parameters_Rendering.json', sBackupSuffix)
    if os.path.isfile(ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_Places.json'):
        bIsBackupOk = bIsBackupOk and ANLib.Tools.backupFile(ANLib.Tools.get_script_path(), 'parameters_Places.json', sBackupSuffix)
    if os.path.isfile(ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_LunarFeatures.json'):
        bIsBackupOk = bIsBackupOk and ANLib.Tools.backupFile(ANLib.Tools.get_script_path(), 'parameters_LunarFeatures.json', sBackupSuffix)
    if os.path.isfile(ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_Localization.json'):
        bIsBackupOk = bIsBackupOk and ANLib.Tools.backupFile(ANLib.Tools.get_script_path(), 'parameters_Localization.json', sBackupSuffix)
    if os.path.isfile(ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_SkyObjects.json'):
        bIsBackupOk = bIsBackupOk and ANLib.Tools.backupFile(ANLib.Tools.get_script_path(), 'parameters_SkyObjects.json', sBackupSuffix)

    if bIsBackupOk:
        print ""
        print "    --> Backup termine."
        print ""
        bContinue = True
    else:
        print ""
        print "   >>> ERREUR pendant lle backup. Installation interrompue."
        print ""    
        bContinue = False

if bContinue:
        
    # si les fichiers de paramètres n'existent pas, il sont créés
    if bContinue and not os.path.isfile(ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_Runtime.json'):
        bContinue = ANLib.Tools.copyFile(ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_Runtime.default.json', ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_Runtime.json')
        if bContinue:
            print "Creation du fichier  " + ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_Runtime.json' 
            print ""
            print "   Modifier le fichier parameters_Runtime.json:"
            print ""
            print '      "GlobalPathToWWWFolder":"[CheminWWW]"'
            print '      "GlobalPathToAPPFolder":"[CheminAPP]"'
            print '      "ObservationPlaceName":"[nomDuLieu]"'
            print '      "NightlyBatchEmailAddress":"email@domain.com" (email destinataire de la notification par mail)'
            print '      "NightlyBatchEmailSMTPServer":"server.domain.com" (nom du serveur SMTP, ex: smtp.gmail.com)'
            print '      "NightlyBatchEmailSMTPUser":"username" (username du compte envoyant le mail)'
            print '      "NightlyBatchEmailSMTPPassword":"password" (password du compte envoyant le mail)'
            print '      "NightlyBatchEmailFromAddress":"AstroNotifemail@domain.com" (email d''origine de la notification par mail)'
            print '      "NightlyBatchDomain":"IP or URL" (Addresse IP ou url du domaine hebergeant l''application)'
            print ""
        else:
            print ""
            print "   >>> ERREUR pendant la creation du fichier. Installation interrompue."
            print ""    
            bContinue = False
    if bContinue and not os.path.isfile(ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_Rendering.json'):
        bContinue = ANLib.Tools.copyFile(ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_Rendering.default.json', ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_Rendering.json')
        if bContinue:
            print "Creation du fichier  " + ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_Rendering.json' 
            print ""
        else:
            print ""
            print "   >>> ERREUR pendant la creation du fichier. Installation interrompue."
            print ""    
            bContinue = False
    if bContinue and not os.path.isfile(ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_Places.json'):
        bContinue = ANLib.Tools.copyFile(ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_Places.default.json', ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_Places.json')
        if bContinue:
            print "Creation du fichier  " + ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_Places.json' 
            print ""
            print "   Modifier le fichier parameters_Places.json:"
            print ""
            print '      renseigner les longitude et latitude pour les lieux déclarés:'
            print '         "Longitude":0.000000000'
            print '         "Latitude":0.000000000'
            print '      renommer les lieux comme il convient, notamment celui qui sera utilisé pour le calcul [nomDuLieu].'
            print ""
        else:
            print ""
            print "   >>> ERREUR pendant la creation du fichier. Installation interrompue."
            print ""    
            bContinue = False
    if bContinue and not os.path.isfile(ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_LunarFeatures.json'):
        bContinue = ANLib.Tools.copyFile(ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_LunarFeatures.default.json', ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_LunarFeatures.json')
        if bContinue:
            print "Creation du fichier  " + ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_LunarFeatures.json' 
            print ""
        else:
            print ""
            print "   >>> ERREUR pendant la creation du fichier. Installation interrompue."
            print ""    
            bContinue = False
    if bContinue and not os.path.isfile(ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_Localization.json'):
        bContinue = ANLib.Tools.copyFile(ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_Localization.default.json', ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_Localization.json')
        if bContinue:
            print "Creation du fichier  " + ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_Localization.json' 
            print ""
        else:
            print ""
            print "   >>> ERREUR pendant la creation du fichier. Installation interrompue."
            print ""    
            bContinue = False
    if bContinue and not os.path.isfile(ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_SkyObjects.json'):
        bContinue = ANLib.Tools.copyFile(ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_SkyObjects.default.json', ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_SkyObjects.json')
        if bContinue:
            print "Creation du fichier  " + ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_SkyObjects.json' 
            print ""
        else:
            print ""
            print "   >>> ERREUR pendant la creation du fichier. Installation interrompue."
            print ""    
            bContinue = False
    print ""

if bContinue:
     # Update des fichiers JSON si existants et Affichage des changement
    print ""
    print "   MISE A JOUR DES FICHIERS DE PARAMETRES"
    print ""
    if not updateParameterFile( 'parameters_Runtime.default.json'):
        print ""
        print "   >>> ERREUR pendant la mise a jour du fichier parameters_Runtime.default.json. Installation interrompue."
        print ""    
        bContinue = False
    elif not updateParameterFile( 'parameters_Rendering.default.json'):
        print ""
        print "   >>> ERREUR pendant la mise a jour du fichier parameters_Rendering.default.json. Installation interrompue."
        print ""    
        bContinue = False
    elif not updateParameterFile( 'parameters_LunarFeatures.default.json'):
        print ""
        print "   >>> ERREUR pendant la mise a jour du fichier parameters_LunarFeatures.default.json. Installation interrompue."
        print ""    
        bContinue = False
    elif not updateParameterFile( 'parameters_SkyObjects.default.json'):
        print ""
        print "   >>> ERREUR pendant la mise a jour du fichier parameters_SkyObjects.default.json. Installation interrompue."
        print ""    
        bContinue = False
    elif not updateParameterFile( 'parameters_Localization.default.json'):
        print ""
        print "   >>> ERREUR pendant la mise a jour du fichier parameters_Localization.default.json. Installation interrompue."
        print ""    
        bContinue = False
    elif not updateParameterFile( 'parameters_Places.default.json'):
        print ""
        print "   >>> ERREUR pendant la mise a jour du fichier parameters_Places.default.json. Installation interrompue."
        print ""    
        bContinue = False
    

if bContinue:
    # Affichage des instruction pour le crontab
    if ANLib.Tools.get_path_separator() == "/":
        print ""
        print "   INSTRUCTIONS POUR LE NIGHTLY BATCH"
        print ""
        print "       Pour pouvoir executer le script batch, taper la commande:"
        print ""
        print "          chmod +x " + ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + "cronjob_NightlyBatch.sh"
        print ""
        print "       Pour déclarer le nightly batch dans la crontab, taper:"
        print ""
        print "          crontab -e"
        print ""
        print "       Inserer (ou modifier la ligne si deja existant) la ligne suivante:"
        print ""
        print "          0 4  * * * " + ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + "cronjob_NightlyBatch.sh"
        print ""
        print "       Sauvegarder par CTRL-O"
        print ""
        print "       Quitter par CTRL-O"
        print ""
        


