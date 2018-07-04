#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
from PIL import Image

oImg = Image.open('C:\_DATA\_PERSO\Catalog_Messier_Miniatures.jpg')

iTopMargin = 18
iBorderHeight = 2
iImageHeight = 149#169
iBorderBottom = 2
iInterline = 5

iLeftMargin = 22
iBorderWidth = 2
iImageWidth = 149#173
iBorderRight = 2
iSpace = 5

sizeThumbnail = 250, 250

for iRow in range(1, 12):
    for iCol in range(1, 11):
        sCropName = "miniature_M" + ("000" + str((iRow - 1) * 11 + iCol))[-3:]
        iStartX = iLeftMargin + (iBorderWidth  + iImageWidth  + iBorderRight  + iSpace)     * (iCol - 1) + iBorderWidth
        iStartY = iTopMargin  + (iBorderHeight + iImageHeight + iBorderBottom + iInterline) * (iRow - 1) + iBorderHeight
        iSizeX = iStartX + iImageWidth
        iSizeY = iStartY + iImageHeight
        iAdjustX = 0
        iAdjustY = 0
        if iRow > 5: iAdjustY = -2
        if iRow > 7: iAdjustY = -4
        if iRow > 10: iAdjustY = -7
        newImg = oImg.crop((iStartX + iAdjustX, iStartY + iAdjustY, iSizeX - 2 + iAdjustX, iSizeY - 2 + iAdjustY))
        print "...Row:" + str(iRow) + "  Col:" + str(iCol) + "    " + sCropName + "    from " + str(iStartX) + ", " +str(iStartY) + "  to  " + str(iSizeX) + ", " +str(iSizeY)
        try:
            newImg.thumbnail(sizeThumbnail, Image.ANTIALIAS)
            newImg.save(sCropName + ".png", "PNG")
        except IOError:
            print "cannot create thumbnail for '%s'" % infile
        #newImg.save(sCropName + ".png", "PNG")
        print "      -->" + sCropName + ".png"
        
