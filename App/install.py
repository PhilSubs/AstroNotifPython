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
            dictData["currentVersion"] = dictDataDefault["currentVersion"]
            bChangeDone = True
            print "      " + sFormattedFilename + ":     " + sFormattedKeyLabel + "    -->   " + dictData["currentVersion"]
        else:
            if sKeyLabel in dictData:
                if type(dictData[sKeyLabel]) is dict:
                    bSubChangeDone, dictData[sKeyLabel] = updateDictValues(sJsonFilename, sLevel + sKeyLabel + ".", dictData[sKeyLabel], dictDataDefault[sKeyLabel])
                    if bSubChangeDone: bChangeDone = True
                else:
                    sCuurentValue = dictData[sKeyLabel]
                    sDefaultValue = dictDataDefault[sKeyLabel]
                    if sCuurentValue != sDefaultValue:
                        print "      " + sFormattedFilename + ":  #  " + sFormattedKeyLabel + "          " + sCuurentValue + "    <-->    " +  sDefaultValue
#                    else:
#                        print "      " + sFormattedFilename + ":  .  " + sFormattedKeyLabel
            else:
                dictData[sKeyLabel] = dictDataDefault[sKeyLabel]
                bChangeDone = True
                print "      " + sFormattedFilename + ":     " + sFormattedKeyLabel + "    -->   " + dictDataDefault[sKeyLabel]
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
    #        with open(ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + sJsonFilename, "w") as fParametersFile:
    #            json.dump(dataParametersRuntime, fParametersFile)
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
print "Installation ASTRONOTIF python"
print "=============================="
print ""

# Check parameters_runtime files
# load parameters file
with open('parameters_Runtime.json', 'r') as fParametersRuntime:
    dataParametersRuntime = json.load(fParametersRuntime)
# load parameters file default
with open('parameters_Runtime.default.json', 'r') as fParametersRuntimeDefault:
    dataParametersRuntimeDefault = json.load(fParametersRuntimeDefault)

# Récupération des versions
sNewVersion = dataParametersRuntimeDefault['currentVersion']
sUpgradeFromVersion = dataParametersRuntime['currentVersion']

# Afficher du message de changement de version
if sUpgradeFromVersion == "":
    print "Nouvelle installation en version " + sNewVersion
else:
    print "Mise a jour de la version " + sUpgradeFromVersion + " vers la version " + sNewVersion
print ""

# copy de backup des fichiers existants (suffixe: version précédente)
print ""
print "   BACKUP PARAMETERS FILES"
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
    print "    --> Backup is successful"
    print ""
    
    # si les fichiers de paramètres n'existent pas, il sont créés
    if not os.path.isfile(ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_Runtime.json'):
        if ANLib.Tools.copyFile(ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_Runtime.default.json', ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_Runtime.json'):
            print "Creation du fichier  " + ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_Runtime.json' 
    if not os.path.isfile(ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_Rendering.json'):
        if ANLib.Tools.copyFile(ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_Rendering.default.json', ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_Rendering.json'):
            print "Creation du fichier  " + ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_Rendering.json' 
    if not os.path.isfile(ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_Places.json'):
        if ANLib.Tools.copyFile(ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_Places.default.json', ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_Places.json'):
            print "Creation du fichier  " + ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_Places.json' 
    if not os.path.isfile(ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_LunarFeatures.json'):
        if ANLib.Tools.copyFile(ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_LunarFeatures.default.json', ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_LunarFeatures.json'):
            print "Creation du fichier  " + ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_LunarFeatures.json' 
    if not os.path.isfile(ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_Localization.json'):
        if ANLib.Tools.copyFile(ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_Localization.default.json', ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_Localization.json'):
            print "Creation du fichier  " + ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_Localization.json' 
    if not os.path.isfile(ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_SkyObjects.json'):
        if ANLib.Tools.copyFile(ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_SkyObjects.default.json', ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_SkyObjects.json'):
            print "Creation du fichier  " + ANLib.Tools.get_script_path() + ANLib.Tools.get_path_separator() + 'parameters_SkyObjects.json' 
    print ""
    
    # Update des fichiers JSON si existants et Affichage des changement
    print ""
    print "   UPDATE PARAMETERS FILES"
    print ""
    bIsReplaceOk = updateParameterFile( 'parameters_Runtime.default.json')
    if bIsReplaceOk: bIsReplaceOk = updateParameterFile( 'parameters_Rendering.default.json')
    if bIsReplaceOk: bIsReplaceOk = updateParameterFile( 'parameters_LunarFeatures.default.json')
    if bIsReplaceOk: bIsReplaceOk = updateParameterFile( 'parameters_SkyObjects.default.json')
    if bIsReplaceOk: bIsReplaceOk = updateParameterFile( 'parameters_Localization.default.json')
    
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
        

else:
    print ""
    print "   >>> ERROR during backup. Process aborted"
    print ""
