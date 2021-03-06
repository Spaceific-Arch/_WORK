import math
from PIL import Image, ImageDraw, ImageFont, ImageColor
import time
import numpy as np
import csv

def getBinRuleFromHex(inHex):
    returnBins = []
    zeroes512 = []
    for x in range(0,512):
        zeroes = ""
        for y in range(0,x):
            zeroes += "0"
        zeroes512.append(zeroes)
#    for i in inRange:
    myBin = "{0:b}".format(int(inHex,16))
#    print "myBin: " + myBin
#    myBin = bin(inHex)
    myBinFull = zeroes512[511 - (len(myBin)-1)] + myBin
    print "type myBinFull:"
    print type(myBinFull)
#   print "myBinFull :" + myBinFull
#   print "len myBin: " + str(len(myBin))
#   print "len myBinFull: " + str(len(myBinFull))
    returnBins.append(myBinFull)
    return myBinFull   

def getInspArray(inArLenght):
    rulesCount = pow(2, inArLenght)
    arRange = range(0, rulesCount)
#    binSeqDiv = [pow(2, x) for x in range(0,inArLenght)]
#    binSeqDiv.reverse()
#    myArray = [[math.trunc(x / y) % 2 for x in arRange] for y in binSeqDiv]
#    myArray = map(list, zip(*myArray))
#    returnArray = [[]]
#    for i in arRange:
#        myChars = ""
#        for j in myArray[i]:
#            myChars += str(myArray[i][j])
#        returnArray[i] = myChars 
    return arRange

def returnOne(inNum):
    if inNum > 1:
        return 1
    else:
        return inNum

def getInspArrayRangeZero(inArLenght):
    rulesCount = pow(2, inArLenght)
    returnArray = []
    arRange = range(0, rulesCount) 
    for i in arRange:
        returnArray.append(0)
    return returnArray

def getInspArraySeqence(inArLenght):
    rulesCount = pow(2, inArLenght)
    arRange = range(0, rulesCount)
    binSeqDiv = [pow(2, x) for x in range(0,inArLenght)]
    binSeqDiv.reverse()
    myArray = [[math.trunc(x / y) % 2 for x in arRange] for y in binSeqDiv]
    myArray = map(list, zip(*myArray)) 
    return myArray

def getRule(inRules, inInspArray, XYuf, XYu, XYub, XYf, XY, XYb, XYdf, XYd, XYdb):
    myPixels = str(XYuf) + str(XYu) + str(XYub) + str(XYf) + str(XY) + str(XYb) + str(XYdf) + str(XYd) + str(XYdb)
    rulePosition = int(myPixels, 2)
    return inRules[rulePosition]

def createFirstLayerFromScratch(inResX, inResY):
    firstLayer = Image.new("RGBA",(inResX,inResY), (0,0,0,255))
    firstLayerDraw = ImageDraw.Draw(firstLayer)
    firstLayerDraw.point((inResX/2, inResY/2), (255,255,255,255))
    return firstLayer

def createNextLayer(inFormerImg, inRules, inInspArray, inLaysCount, inCSV_logPath, inWriteLogFile):
    sTime = time.time()
    myFImgData = np.array(inFormerImg.getdata())
    liWidth = inFormerImg.size[0]
    liHeight = inFormerImg.size[1]
    liLength = len(myFImgData)
    returnImgs = []
    myPixDatasLog = []
    myStrRule = ""
    for x in inRules:
        myStrRule += str(x)
    myHexCAstr = str(hex(int(myStrRule, 2)))
    if inWriteLogFile == True:
        f = open(inCSV_logPath, 'w')
        writer = csv.writer(f)
    for l in range(0, inLaysCount):
        truePixs = []
        nextImg = Image.new("RGBA",(liWidth, liHeight), (0, 0, 0,255))
        nextImgDraw = ImageDraw.Draw(nextImg)
        myPixData = []
        for b in myFImgData:
            myPixData.append((0,0,0,255))
        if inWriteLogFile == True:
            writer.writerow([l])
        for a, x in enumerate(myFImgData):   
            if (a % liWidth > 0) and (a % liWidth < liWidth -1) and a > liWidth and a < liLength - liWidth:
 #               print "myFImgData[(a - liWidth - 1)]"
 #               print myFImgData[(a - liWidth - 1)]
                XYuf = returnOne(myFImgData[(a - liWidth - 1)][0])
                XYu = returnOne(myFImgData[a - liWidth][0])
                XYub = returnOne(myFImgData[a - liWidth + 1][0])
                XYf = returnOne(myFImgData[a - 1][0])
                XY = returnOne(myFImgData[a][0])
                XYb = returnOne(myFImgData[a + 1][0])
                XYdf = returnOne(myFImgData[a + liWidth - 1][0])
                XYd = returnOne(myFImgData[a + liWidth][0])
                XYdb = returnOne(myFImgData[a + liWidth + 1][0])
                rule = getRule(inRules, inInspArray, XYuf, XYu, XYub, XYf, XY, XYb, XYdf, XYd, XYdb)
                if rule == 1:
#                  truePixs.append([a / liWidth, a % liWidth])
                   truePixs.append((a % liWidth, a / liWidth))
                   myStrInspArray = str(XYuf) + str(XYu) + str(XYub) + str(XYf) + str(XY) + str(XYb) + str(XYdf) + str(XYd)  + str(XYdb)
                   if inWriteLogFile == True:
                       writer.writerow([str(a % liWidth), str(a / liWidth), myStrInspArray, int(myStrInspArray, 2)])
        nextImgDraw.point(truePixs, (255, 255, 255,255))
        myFImgData = np.array(nextImg.getdata())
#        testImg.save(r"/storage/emulated/0/CA/_moje pokusy/testPix.png")
        returnImgs.append(nextImg)
        myPixDatasLog.append(myPixData.append)
        
#    nextImgData = np.array(nextImg.getdata())
    eTime = time.time()
    myTime = eTime -sTime
    print "Time of creating "+str(inLaysCount)+" CA layers is " + str(int(myTime/60))+" m " +str(int(myTime%60)) + " s"
    return returnImgs

def remap(value, minInput, maxInput, minOutput, maxOutput):
    if minInput < maxInput:
        value = maxInput if value > maxInput else value
        value = minInput if value < minInput else value
        inputSpan = maxInput - minInput
        outputSpan = maxOutput - minOutput
        scaledThrust = float(value - minInput) / float(inputSpan)
        return minOutput + (scaledThrust * outputSpan)
    else:
        return minOutput

def run(inResX, inResY, inLayCount, inMyRule, inCSV_logPath, inWriteLogFile):
    resXstr = str(inResX)
    resYstr = str(inResY)
    myInspArray = getInspArray(9)
    sourceRule = inMyRule
    sourceRuleArray = [int(x) for x in sourceRule]
#    print "CURRENT RULE: \n" + sourceRule
    slashChar = r"/"
#    layNum = 0
#    print "CURRENT GENERATION: " + str(layNum)
#    properLayNum = getProperLayNum(layNum)
    imageFormat = "bmp"
    myLayers = []
    
#    if layNum == 0:
    firstLayer = createFirstLayerFromScratch(inResX, inResY)
#    myLayers.append(firstLayer)
#    ensure_dir(finalDirPath)
#    firstLayer.save(finalDirPath + properLayNum + "_" + resXstr + "x" + resYstr + "." + imageFormat)
#    layNum += 1
    myLastImg = firstLayer
    myLayers = createNextLayer(myLastImg, sourceRuleArray, myInspArray, inLayCount-1, inCSV_logPath, inWriteLogFile)
    myLayers.insert(0,firstLayer)
#        for c in myNextLayers:
#            layNum += 1
#            properLayNum = getProperLayNum(layNum)
#            c.save(finalDirPath + properLayNum + "_" + resXstr + "x" + resYstr + "." + imageFormat)
#    else:
#        myLastImg = loadLastLayer(finalDirPath)
#        myNextLayers = createNextLayer(myLastImg, sourceRuleArray, myInspArray, layersCount)
#        for c in myNextLayers:
#            layNum += 1
#            properLayNum = getProperLayNum(layNum)
#            c.save(finalDirPath + properLayNum + "_" + resXstr + "x" + resYstr + "." + imageFormat)
    return myLayers

def getCross(inRule, inInspArraySequence, inRows, inLogData):
#    dirPath = r"/storage/emulated/0/CA/_moje pokusy/cross_test.png"  
    rows = inRows
    columns = len(inInspArraySequence) / rows
    recColumns = 3
    recRows = 3
    print "columns:"
    print columns
#    recSize = inWidth / (len(inInspArraySequence)/float(rows)) / 7
    recSize = 4
    fadeValue = 0.35
    crossSize = recSize * 7
    outlineWidth = 3
    gap = recSize
    crossMXCoords3x3 = [[0,0],[1,0],[2,0],[0,1],[1,1],[2,1],[0,2],[1,2],[2,2]]
#    print crossMXCoords3x3[0]
    orderTextFontSize = int(crossSize*0.5)
    ocurenceTextFontSize = int(crossSize*0.7)
    headFontSize = int(crossSize*0.6)
    headLines = 6
    headLineGap = int(headFontSize * 0.5)
    headLineHeight = headFontSize + headLineGap
    headTextHeight = (headLineHeight) * headLines + headLineGap
    headTextX = gap
    headText1Y = 0 * headLineHeight
    headText2Y = 1 * headLineHeight
    headText3Y = 2 * headLineHeight
    headText4Y = 3 * headLineHeight
    headText5Y = 4 * headLineHeight
    headText6Y = 5 * headLineHeight
    orderTextYOffset = orderTextFontSize
    orderTextFont = ImageFont.truetype("raavi.ttf", orderTextFontSize)
    ocurenceTextFont = ImageFont.truetype("arial.ttf", ocurenceTextFontSize)
    headFont = ImageFont.truetype("arial.ttf", headFontSize)
    rowHeight = orderTextYOffset + crossSize + ocurenceTextFontSize
    imHeight = int(headTextHeight + (rowHeight * rows))
    imWidth = columns * crossSize
    print "imWidth: " + str(imWidth)
    myHSLcol = "hsl(0,100%,50%)"
    myFirstOcurences = inLogData[0]
    myOcurencesCount = inLogData[1]
    maxOcurenceValue = max(myOcurencesCount)
    scaleCount = 10
    scaleStep = maxOcurenceValue / scaleCount
    if scaleStep > 0:
        scaleRange = range(0,maxOcurenceValue,scaleStep)
    else:
        scaleRange = range(0,10,1)
    im = Image.new('RGBA', (imWidth + outlineWidth,imHeight + outlineWidth), (0, 0, 0,255))
    imD = ImageDraw.Draw(im)
    canvasBColor = ImageColor.getrgb("Coral")
    crossBColor = "hsl(130,100%,70%)"
    recBColor = "hsl(240,100%,70%)"
    orderTextCollor = (255,255,255,255)
#    imD.rectangle([0,0, imWidth, imHeight],(0,0,255,0), "Coral")
    imD.text((headTextX, headText1Y), "BIN: " + inRule, font=headFont, fill=(255,255,255,255))
    imD.text((headTextX, headText2Y), "INT: " + str(int(inRule, 2)), font=headFont, fill=(255,255,255,255))
    myHex = str(hex(int(inRule, 2)))
    imD.text((headTextX, headText3Y),"HEX: " + myHex[2:len(myHex)-1], font=headFont, fill=(255,255,255,255))
    for i, v in enumerate(inInspArraySequence):
        orderTextSize = imD.textsize(str(i),font=orderTextFont)
        crossXOffset = (i%columns)*crossSize
        crossYOffset = headTextHeight + (i/columns)*rowHeight
#        imD.rectangle([crossXOffset, crossYOffset, crossXOffset+crossSize, crossYOffset+crossSize],(0,0,0,0), crossBColor)
        orderTextX = (crossXOffset + crossSize/2) - orderTextSize[0]/2
        orderTextY = crossYOffset - orderTextYOffset
        imD.text((orderTextX, orderTextY), str(i), font=orderTextFont, fill=(80,80,80,255))
        ocurenceTextSize = imD.textsize(str(myFirstOcurences[i]),font=ocurenceTextFont)
        ocurenceTextX = (crossXOffset + crossSize/2) - ocurenceTextSize[0]/2
        ocurenceTextY = crossYOffset + crossSize
        myHSLcol = "hsl(" + str(int(remap(myOcurencesCount[i], 0, maxOcurenceValue, 0, 185))) + ",100%, " + str(int(remap(myOcurencesCount[i], 0, maxOcurenceValue, 30, 70))) + "%)"
        imD.text((ocurenceTextX, ocurenceTextY), str(myFirstOcurences[i]),font=ocurenceTextFont, fill=myHSLcol)
        for j, h in enumerate(v):
#            print j
            fCComponent = int(255*fadeValue)
            frameColor = (fCComponent, fCComponent, fCComponent, fCComponent)
            fillCComponent = int(int(h)*(255*fadeValue+((1-fadeValue)*int(inRule[i])*255)))
            fillColor = (fillCComponent, fillCComponent, fillCComponent, 255)
            mx3x3Coords = crossMXCoords3x3[j]
            recXCoord = mx3x3Coords[0]
            recYCoord = mx3x3Coords[1]
            recXOffset = crossXOffset + recSize + recXCoord*recSize
            recYOffset = crossYOffset + recSize + recYCoord*recSize
            imD.rectangle([recXOffset, recYOffset, recXOffset+recSize, recYOffset+recSize], fillColor, frameColor)
    textXpos = headTextX
    symGroupCoordStr = "SYMETRY_GROUPS_COORDS:   "
    # symGroupStr =      "SYMETRY_GROUPS_POSITIONS:"
    # for d in rndSymGroupeCoords:
    #     symGroupCoordStr += "("+str(d[0])+","+str(d[1])+")"
    # imD.text((headTextX, headText4Y), symGroupCoordStr,font=headFont, fill="white")
    # for c in myRndSymGroups:
    #     symGroupStr += str(c)+","
    # imD.text((headTextX, headText5Y), symGroupStr,font=headFont, fill="white")
    for s in scaleRange:
        myHSLcol = "hsl(" + str(int(remap(s, 0, maxOcurenceValue, 0, 185))) + ",100%, " + str(int(remap(s, 0, maxOcurenceValue, 30, 70))) + "%)"
        imD.text((textXpos, headText6Y), str(s),font=headFont, fill=myHSLcol)
        myTextSize = imD.textsize(str(s),font=headFont)
        textXpos += (myTextSize[0] + 15)
        
    return im