#!/usr/bin/python2.7
# -*-coding:Latin-1 -*

import string
import os
import os.path
import sys

# Import PIL or PILLOW libraries for bitmaps
from PIL import Image, ImageDraw

# Import smtplib for the actual sending function
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Tools:
    @staticmethod
    def get_script_path():
        """ Return the script path"""
        return os.path.dirname(os.path.realpath(sys.argv[0]))

    @staticmethod
    def get_ResourceSubfolder_path(sSubfolder):
        """ Return the script path"""
        sScriptPath = Tools.get_script_path()
        if sScriptPath[0:1] == "/":
            sFontPath = sScriptPath + "/Resources/" + sSubfolder + "/"
        else:
            sFontPath = sScriptPath + "\\Resources\\" + sSubfolder + "\\"
        return sFontPath

    @staticmethod
    def get_ResourceBitmaps_path():
        """ Return the script path"""
        sScriptPath = Tools.get_script_path()
        if sScriptPath[0:1] == "/":
            sFontPath = sScriptPath + "/Resources/Bitmaps/"
        else:
            sFontPath = sScriptPath + "\\Resources\\Bitmaps\\"
        return sFontPath

    
    @staticmethod
    def getScriptname(  ):
        """ Return the scriptname part of the URL ("/path/to/my.cgi"). """
        return os.environ.get('SCRIPT_NAME', '')

    @staticmethod
    def getPathinfo(  ):
        """ Return the remaining part of the URL. """
        pathinfo = os.environ.get('PATH_INFO', '')

        # Fix for a well-known bug in IIS/4.0
        if os.name == 'nt':
            scriptname = Tools.getScriptname(  )
            if string.find(pathinfo, scriptname) == 0:
                pathinfo = pathinfo[len(scriptname):]

        return pathinfo

    @staticmethod
    def getQualifiedURL(uri = None):
        """ Return a full URL starting with schema, servername, and port.
            Specifying uri causes it to be appended to the server root URL (uri must
            start with a slash).
        """
        schema, stdport = (('http', '80'), ('https', '443'))[Tools.isSSL(  )]
        host = os.environ.get('HTTP_HOST', '')
        if not host:
            host = os.environ.get('SERVER_NAME', 'localhost')
            port = os.environ.get('SERVER_PORT', '80')
            if port != stdport: host = host + ":" + port

        result = "%s://%s" % (schema, host)
        if uri: result = result + uri

        return result

    @staticmethod
    def getGenerateMoonFeatureBitmap(sSubfolderForBitmaps, sFeatureID, fFeatureLongitude, fFeatureLatitude, iBitmapSizeX, iBitmapSizeY, iIndicatorSizeInPx):
        #Creating new image with PIL: size  iBitmapSizeX x iBitmapSizeY, background white
        img = Image.new( 'RGB', (iBitmapSizeX, iBitmapSizeY), "white") # create a new black image
        # Draw Moon shape as black circle
        draw = ImageDraw.Draw(img)
        draw.ellipse((0, 0, iBitmapSizeX - 1, iBitmapSizeY - 1), fill=(255,255,255), outline=(0,0,0))
        # Compute position of the feature in the image
        x = int(iBitmapSizeX / 2) + 1 + int(fFeatureLongitude / 90.0 * float(iBitmapSizeX / 2))
        y = int(iBitmapSizeY / 2) + 1 + int( - fFeatureLatitude / 90.0 * float(iBitmapSizeY / 2))
        # Draw a red dot at the position of the feature
        draw.ellipse((x - int(iIndicatorSizeInPx / 2) , y - int(iIndicatorSizeInPx / 2), x + int(iIndicatorSizeInPx / 2), y + int(iIndicatorSizeInPx / 2)), fill=(255,0,0), outline=(255,0,0))
        del draw 
        # compute image name, based on image id and size
        sImageName = "Eph_" + sFeatureID + "_" + str(iBitmapSizeX) + "x" + str(iBitmapSizeY) + ".jpg"  
        # save image and return image name
        img.save(sSubfolderForBitmaps + sImageName, "JPEG")
        return sImageName

    @staticmethod
    def getBaseURL(  ):
        """ Return a fully qualified URL to this script. """
        return Tools.getQualifiedURL(getScriptname(  ))


    @staticmethod
    def sendEmailHTML(sFrom, sTo, sSubject, sHTMLContent, sSMTPServer ):
        # Create message container - the correct MIME type is multipart/alternative.
        theMsg = MIMEMultipart('alternative')
        theMsg['Subject'] = sSubject
        theMsg['From'] = sFrom
        theMsg['To'] = sTo

        # Record the MIME types of both parts - text/plain and text/html.
        theMIMEpart = MIMEText(sHTMLContent, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        theMsg.attach(theMIMEpart)

        # Send the message via local SMTP server.
        theSender = smtplib.SMTP(sSMTPServer)
        theSender.set_debuglevel(False)
        theSender.login("notifier@astronot.heliohost.org", "bH!l!bb6@8K8dtF3Unbi$sep##eKM7jk")
        try:
            # sendmail function takes 3 arguments: sender's address, recipient's address
            # and message to send - here it is sent as one string.
            theSender.sendmail(sFrom, sTo, theMsg.as_string())
        finally:
            theSender.quit()

    @staticmethod
    def saveAsFile(sFileName, sContent ):
        theFile = open(sFileName,'w')
        theFile.write(sContent)
        theFile.close()

    @staticmethod
    def getCurrentFilesHTMLHeaderComment(sFileName):
        # default returned value is empty string (in case file doesn't exist, or file doesn't contain header as first row
        sReturn = ""
        # if file esists...
        if os.path.isfile(sFileName):
            # read first line from file
            theFile = open(sFileName,'r')
            sFirstLine = theFile.readline()
            theFile.close()
            # if first line is a header...
            if sFirstLine[0:24] == '<!-- Parameters... Date:':
                # header will be returned
                sReturn = sFirstLine
        # return value
        return sReturn

    @staticmethod
    def removeHTMLTags(sText):
        # Remove HTML tags:
        #    <B> and </B>
        #    &nbsp;
        sReturn = sText
        sText = sText.replace('<B>','')
        sText = sText.replace('</B>','')
        sText = sText.replace('&nbsp;',' ')
        
        return sText
        
