# -*- coding: utf-8 -*-
import numpy as np
np.set_printoptions(threshold='nan')
from os import walk
import os
import math
import csv
import random
random.seed()
from PIL import Image, ImageDraw
dirPath = r"C:/_WORK/PYTHON/CELULAR_AUTOMAT-2D/zaloha/x/"
loadPath = r"C:/_WORK/PYTHON/CELULAR_AUTOMAT-2D/zaloha/y/"
CSV_logPath = r"C:/_WORK/PYTHON/CELULAR_AUTOMAT-2D/LOG/"
generateRandom = False
invertedRule = False
shiftDir = "N"
rndBaseRule = 0
writeLogFile = True
#         012345678910...15...20...25...30
#myRule = "01110110100010001000011010000011"
myIntRule = 1960164845
myHexRule = int("4110494c92db4006910d80592c12180114034ca4d94ca25145b6c900121a20040000000000000000000000000000000000000000000000000000000000000000", 16)
runNum = 10
myRange  = range(0,30)
zeroPositions = {0,511}

def getNewVersionRule(inOldRule): 	
    oldRule = inOldRule 	
    newRule = [] 	
    conversionTable = [16, 20, 24, 29, 17, 22, 26, 0, 25, 30, 19, 8, 27, 3, 13, 10, 21, 18, 28, 4, 23, 12, 1, 6, 31, 5, 9, 14, 2, 7, 11, 15] 	
    for i in conversionTable: 		
        newRule.append(oldRule[i]) 	
    returnString = "".join(newRule)
    print "new version rule :"
    print 	returnString
    return returnString

#myRule = getNewVersionRule("00000000000000100000110011000000")

def generateRandomRule(inInspArray):
    myRule = ""
    for i in inInspArray:
         myRule += str(random.randint(0,1))
    return myRule
    
def getSourceRule(inMyRule, inRandomRule, inGenerateRandom, inShiftDir, inRndBaseRule):
   myRule = inMyRule
#   print "MY RULE: \n" + myRule
   if inGenerateRandom == True:
      myRule = inRandomRule
      if inShiftDir == "R":
          myRule = shiftRule(myRule, inShiftDir)
          print "MY RANDOM RIGHT SHIFTED RULE: \n" + myRule
          return myRule
      elif inShiftDir == "L":
          myRule = shiftRule(myRule, inShiftDir)
          print "MY RANDOM LEFT SHIFTED RULE: \n" + myRule
          return myRule
      else:
          return myRule
   elif inShiftDir == "R":
      myRule = shiftRule(myRule, inShiftDir)
      print "MY RIGHT SHIFTED RULE: \n" + myRule
      return myRule
   elif inShiftDir == "L":
      myRule = shiftRule(myRule, inShiftDir)
      print "MY LEFT SHIFTED RULE: \n" + myRule
      return myRule      
   else:
       if inRndBaseRule > 0:
           myRule = randomizeRule(myRule, inRndBaseRule)
           print "MY RANDOMIZED " + str(inRndBaseRule) + " DIGITS IN RULE: \n" + myRule
           return myRule
       else:
           return myRule

def shiftRule(inRule, direction):
    shiftedRule = ""
    if direction == "R":
        shiftedRule += inRule[len(inRule)-1]
        for i, s in enumerate(inRule):
            if i< len(inRule) -1:
                shiftedRule += s
    elif direction == "L":
        shiftedRule += inRule[1]
        firstChar = inRule[0]
        for i, s in enumerate(inRule):
            if i< len(inRule) -2:
                shiftedRule += inRule[i+2]
        shiftedRule += firstChar
    elif direction == "N":
        return inRule
    return shiftedRule
        
def randomizeRule(inRule, inDigCount):
    fRule = inRule
    retRule = ""
    returnRule = []
    if inDigCount>0:
        for x in range(0,inDigCount):
            nRule = ""
            rulePos = random.randint(0,31)
            for i, y in enumerate(fRule):
                if i == rulePos:
                    if y == "0":
                         nRule += "1"
                    else:
                         nRule += "0"                
                else:
                    nRule += y
            fRule = nRule
    return fRule   

def getInvertedRule(inRule):
    returnString = ""
    for i in inRule:
        if i == "0":
            returnString += "1"
        elif i == "1":
            returnString += "0"
    return returnString
    
def getBinRuleFromInt(inInt):
    returnBins = []
    zeroes32 = []
    for x in range(0,32):
        zeroes = ""
        for y in range(0,x):
            zeroes += "0"
        zeroes32.append(zeroes)
#    for i in inRange:
    myBin = "{0:b}".format(inInt)
    myBinFull = zeroes32[31 - (len(myBin)-1)] + myBin
    returnBins.append(myBinFull)
    return returnBins
    
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
    print "type myBin:"
    print "myBin: " + myBin
#    myBin = bin(inHex)
    myBinFull = zeroes512[511 - (len(myBin)-1)] + myBin
    print "myBinFull :" + myBinFull
    print "len myBin: " + str(len(myBin))
    print "len myBinFull: " + str(len(myBinFull))
    returnBins.append(myBinFull)
    return myBinFull    

def getFirstHalfZeroRule(inRule):
    returnArray = []
    for i, v in enumerate(inRule):
        if i < len(inRule) / 2:
            returnArray.append("0")
        else:
            returnArray.append(inRule[i])
    return "".join(returnArray)

def getZeroPositionsRule(inRule, inPos):
    returnArray = []
    for i, v in enumerate(inRule):
        putZero = False
        if len(inPos) == 0:
            return inRule
            break
        else:
            for j, w in enumerate(inPos):
                if w == i:
                    putZero = True
        if putZero == True:
            returnArray.append("0")
        else:
            returnArray.append(v)
    return "".join(returnArray)
    
def getSecondHalfZeroRule(inRule):
    returnArray = []
    for i, v in enumerate(inRule):
        if i >= len(inRule) / 2 or i == 0:
            returnArray.append("0")
        else:
            returnArray.append(inRule[i])
    return "".join(returnArray)
    
def getFirstQuarterZeroRule(inRule):
    returnArray = []
    for i, v in enumerate(inRule):
        if i < len(inRule) / 4:
            returnArray.append("0")
        else:
            returnArray.append(inRule[i])
    return "".join(returnArray)

def getNTHZeroRule(inRule, inPos):
    returnArray = []
    for i, v in enumerate(inRule):
        if i % inPos == 0:
            returnArray.append("0")
        else:
            returnArray.append(inRule[i])
    return "".join(returnArray)

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
#        returnArray[i] = myChars .
    return arRange



def getLayNum(inDirPath):
    myDir = []
    layNum = int
    if os.path.isdir(inDirPath):
        myDir = os.listdir(inDirPath)
#        myDir.sort
        myLayNum = len(myDir)
        return myLayNum
    else:
        return 0
    
    
def createFirstLayerFromScratch(inResX, inResY):
    firstLayer = Image.new("1",(inResX,inResY))
    firstLayerDraw = ImageDraw.Draw(firstLayer)
    firstLayerDraw.point((inResX/2, inResY/2), 1)
    return firstLayer

def ensure_dir(file_path):
    directory = os.path.dirname(file_path) 
    if not os.path.exists(directory):
        os.makedirs(directory)
        
def getProperLayNum(inLayNum):
    returnString = ""
    inLayNumStr = str(inLayNum)
    if len(inLayNumStr) == 1:
        returnString = "00" + inLayNumStr
    elif len(inLayNumStr) == 2:
        returnString = "0" + inLayNumStr
    else:
        returnString = inLayNumStr
    return returnString



def getRule(inRules, inInspArray, XYuf, XYu, XYub, XYf, XY, XYb, XYdf, XYd, XYdb):
    myPixels = str(XYuf) + str(XYu) + str(XYub) + str(XYf) + str(XY) + str(XYb) + str(XYdf) + str(XYd) + str(XYdb)
    rulePosition = int(myPixels, 2)
    return inRules[rulePosition]

def createNextLayer(inFormerImg, inRules, inInspArray, inLaysCount):
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
    if writeLogFile == True:
        f = open(CSV_logPath + "CA2D9C_" + myHexCAstr[2:len(myHexCAstr)-1] + "_" + str(liWidth) + "x" + str(liHeight) + ".csv", 'w')
        writer = csv.writer(f)
    for l in range(0, inLaysCount):
        truePixs = []
#        testImg = Image.new("RGBA",(liWidth, liHeight))
#        testData = testImg.getdata()
#        for i in testData:
#            print i
        nextImg = Image.new("1",(liWidth, liHeight))
        nextImgDraw = ImageDraw.Draw(nextImg)
        myPixData = []
        for b in myFImgData:
            myPixData.append((0,0,0,255))
        if writeLogFile == True:
            writer.writerow([l])
        for a, x in enumerate(myFImgData):   
            if (a % liWidth > 0) and (a % liWidth < liWidth -1) and a > liWidth and a < liLength - liWidth:
                XYuf = returnOne(myFImgData[(a - liWidth - 1)])
                XYu = returnOne(myFImgData[a - liWidth])
                XYub = returnOne(myFImgData[a - liWidth + 1])
                XYf = returnOne(myFImgData[a - 1])
                XY = returnOne(myFImgData[a])
                XYb = returnOne(myFImgData[a + 1])
                XYdf = returnOne(myFImgData[a + liWidth - 1])
                XYd = returnOne(myFImgData[a + liWidth])
                XYdb = returnOne(myFImgData[a + liWidth + 1])
                rule = getRule(inRules, inInspArray, XYuf, XYu, XYub, XYf, XY, XYb, XYdf, XYd, XYdb)
                if rule == 1:
#                  truePixs.append([a / liWidth, a % liWidth])
                   truePixs.append((a % liWidth, a / liWidth))
                   myStrInspArray = str(XYuf) + str(XYu) + str(XYub) + str(XYf) + str(XY) + str(XYb) + str(XYdf) + str(XYd)  + str(XYdb)
                   if writeLogFile == True:
                       writer.writerow([str(a % liWidth), str(a / liWidth), myStrInspArray, int(myStrInspArray, 2)])
        nextImgDraw.point(truePixs, 1)
        myFImgData = np.array(nextImg.getdata())
#        testImg.save(r"/storage/emulated/0/CA/_moje pokusy/testPix.png")
        returnImgs.append(nextImg)
        myPixDatasLog.append(myPixData.append)
#    nextImgData = np.array(nextImg.getdata())
    return returnImgs
    
def loadLastLayer(inDirPath):
    myDir = []
    truePixs = [[]]
    lastImg = Image
    liWidth = 0
    liHeight = 0
    if os.path.isdir(inDirPath):
        myDir = os.listdir(inDirPath)
        myDir.sort()
    if len(myDir) != 0:
        lastImg = Image.open(inDirPath + myDir[len(myDir)-1])
        lastImg.convert("1")
        lastImg.tobitmap(lastImg)
        print "LAST IMAGE: " +myDir[len(myDir)-1]
        print "colors = " + str(lastImg.getcolors())
    else:
        return null
 #   myImgData = np.array(lastImg.getdata())
#    liWidth = lastImg.size[0]
#    liHeight = lastImg.size[1]
#    ind = 0
#    for a, x in enumerate(myImgData):
#        if x == 1:
#            truePixs.append([a / liWidth, a % liWidth])
#            ind += 1
    return lastImg
    
def returnOne(inNum):
    if inNum > 1:
        return 1
    else:
        return inNum

def run(inRule):  
#    for i in range(0, inTimes):
#        print "loop index: " + str(i )
#    myRule = "".join(getBinRuleFromInt(myIntRule))
#        myRule = "".join(getBinRuleFromHex(myHexRule))
        myRule = inRule
        print "run myRule: "
        print myRule
        print "run myRule type:"
        print type(myRule)
        myInspArray = getInspArray(9)
        myRandomRule = generateRandomRule(myInspArray)
        sourceRule = getSourceRule(myRule, myRandomRule, generateRandom, shiftDir, rndBaseRule)
    #    sourceRule = getZeroPositionsRule(sourceRule, zeroPositions)
    #    sourceRule = getFirstHalfZeroRule(sourceRule)
    #    sourceRule = getFirstQuarterZeroRule(sourceRule)
    #    
    #    sourceRule = getNTHZeroRule(sourceRule, 3)
    #    sourceRule = getSecondHalfZeroRule(sourceRule)
        sourceRuleArray = [int(x) for x in sourceRule]
    #    print sourceRuleArray
    #    print "CURRENT RULE: \n" + sourceRule
        resolutionX = 51
        resXstr = str(resolutionX)
        resolutionY = 51
        resYstr = str(resolutionY)
        layersCount = 300
        slashChar = r"/"
        print type(myRule)
        myStrRule = ""
        for x in inRule:
            myStrRule += str(x)
        myHexCAstr = str(hex(int(myStrRule, 2)))
    #    print mystr[2:len(mystr)]
        finalDirPath = dirPath + "CA2D9C_" + myHexCAstr[2:len(myHexCAstr)-1] + "_" + resXstr + "x" + resYstr + slashChar
    #    binNum = [1,1,1,1,1]
    #    binStr = ""
    #    for i in binNum:
    #        binStr += str(binNum[i])
    #    print binStr  Str  
        layNum = getLayNum(finalDirPath)
        print "CURRENT GENERATION: " + str(layNum)
    
    #    print myInspArray
    #    print getRule(sourceRuleArray, myInspArray, 1, 1, 1, 1, 0) 
    #    print loadLastLayer(sourceRule, finalDirPath)
        properLayNum = getProperLayNum(layNum)
        imageFormat = "bmp"
        if layNum == 0:
            firstLayer = createFirstLayerFromScratch(resolutionX, resolutionY)
            ensure_dir(finalDirPath)
            firstLayer.save(finalDirPath + properLayNum + "_" + resXstr + "x" + resYstr + "." + imageFormat)
            layNum += 1
            myLastImg = firstLayer
            myNextLayers = createNextLayer(myLastImg, myRule, myInspArray, layersCount-1)
            for c in myNextLayers:
                layNum += 1
                properLayNum = getProperLayNum(layNum)
                c.save(finalDirPath + properLayNum + "_" + resXstr + "x" + resYstr + "." + imageFormat)
        else:
            myLastImg = loadLastLayer(finalDirPath)
            myNextLayers = createNextLayer(myLastImg, myRule, myInspArray, layersCount)
            for c in myNextLayers:
                layNum += 1
                
                properLayNum = getProperLayNum(layNum)
                c.save(finalDirPath + properLayNum + "_" + resXstr + "x" + resYstr + "." + imageFormat)
    #       print "myImgData " + ": " + str(myNextLayers) ers) ers) 

def runDirSequence(inLoadPath, inDirPath, inRange):
    rules = []
    f = []
    for (path, dirnames, filenames) in walk(inLoadPath): 

        f.extend(dirnames) 
        break
    f.sort()
    print "dir names:"
    print f
    for i in f:
        myBinRule = getBinRuleFromHex(i)
        print "myBinRule: "
        print type(myBinRule)
        rules.append(myBinRule)
    print "bin rules:"
    print "type(rules[0])"
    print type(rules[0])
    print "rules[0][0]"
    print rules[0][0]
    print "rules"
    print rules
#    CA = []
    for i, r in enumerate(rules[inRange[0] : inRange[0] + len(inRange)]):
        print str(i) + " from " + str(len(rules[inRange[0] : inRange[0] + len(inRange)]))
        print str(i + inRange[0]) + " from " + str(inRange[0] + len(inRange))
        print "all: " + str(len(rules))
#        position = int(r,16)
#        print "position " + str(position)
        ruleArray = [int(x) for x in r]
        run(ruleArray)
#        print rules
#        CA.append([myCA, position, r])
#        print CA[i]
#    createImgCollection(CA, dirPath)

#    for i in f[inRange[0]:inRange[len(inRange)-1]]:
#        splitedPath = i.split("_")
#        rules.append(splitedPath[1])
#    for j, s in enumerate(f):
#        f[j] = inDirPath + s
#    for i in rules:
#        run(resolutionX, resolutionY, layersCount, i, dirPath, generateRandom, shiftDir, rndBaseRule)
    for r in rules:
        print int(r,2)
    print "------------"
    for r in rules[inRange[0] : inRange[0] + len(inRange)]:
        print int(r,2)
    print "------------"
    print inRange[0]
    print inRange[0] + len(inRange)
    
runDirSequence(loadPath, dirPath, myRange)
        


