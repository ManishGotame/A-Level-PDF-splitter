# saves a json file for offline visualization
# saves a text file for uploading to the server

# main
import re
import os
#from fonts import get_font 
import json
import cv2
import datetime
import imutils
import fitz
import shutil

# OpenPastPaper mainLib
#from AI.predict import predict 

from pdfsplitter.qpaper import qparser
from pdfsplitter.mscheme import mparser
from pdfsplitter.utils.mcq import mcq 
from pdfsplitter.utils.extractor import extract
from pdfsplitter.utils.funct import *

msFilename = ""
subjectCode = ""
qFilename = "9231_s12_qp_22"
#qFilename = "9700_s14_qp_21"
qFilename = "9709_s14_qp_21"
#qFilename = "9706_s14_qp_21"
# qFilename = "9701_s11_qp_21" # -> failed -> didn't read the first page -> 
#qFilename = "9701_s1qpqp_22"
#qFilename = "9701_s16_qp_41"
#qFilename = "9701_s15_qp_32" # -> couldn't locate question number 3
#qFilename = "9701_s07_qp_2"
#qFilename = "9702_s10_qp_43"
# qFilename = "9990_s18_qp_22"
#qFilename = "9608_s16_qp_11"
#qFilename = "9231_s10_qp_11"
#qFilename = "9709_w10_qp_73"
#qFilename = "9709_s14_qp_21"
# qFilename = "9709_s12_qp_42"
# qFilename = "9702_s09_qp_4"
#qFilename = "9709_w10_qp_73"
# qFilename = "9709_s15_qp_62"
qFilename = "9702_s12_qp_21"
# qFilename = "9702_s16_qp_32"
qFilename = "9709_s10_qp_11"
qFilename = "9709_s17_qp_12"
qFilename = "9702_s18_qp_22"
qFilename = "9702_s12_qp_21"
qFilename = "9709_s19_qp_22"
qFilename = "9608_s19_qp_12"
qFilename = "9701_s13_qp_22"
qFilename = "9701_s19_qp_22"
#qFilename = "9702_s05_qp_4"
#qFilename = "9702_s10_qp_43"
#qFilename = "9709_s19_qp_22"
qFilename = "9702_s16_qp_12"
qFilename = "9702_s13_qp_13"
qFilename = "9702_w19_qp_11"
# qFilename = "9702_s13_qp_42"
qFilename = "9702_s17_qp_42"
qFilename = "9608_s16_qp_11"
qFilename = "9709_s13_qp_22"
qFilename = "9701_s17_qp_13"
qFilename = "9702_s05_qp_4"
qFilename = "9701_s14_qp_22" # the marking scheme page is too wide for the parser to detect

filePath = "9701_s18_qp_22.pdf"
filePath = "9709_s10_qp_11.pdf"
try:
    qFilename = re.split("[/]", filePath)[1]
except: qFilename = filePath 

qFilename = re.split("[.]", qFilename)[0]

word = "[_]"
qName = re.split(word, filePath)
qName[2] = "ms"
msFilename = "_".join(qName)
subjectCode = qName[0] + "-" + qName[3][0]   # for AI.predict 
# subjectCode = "9702-2"

def main():
    # check if the folder exists
    allQuestions = os.listdir("questionsPDF/")
    if qFilename not in allQuestions: os.mkdir("questionsPDF/" + qFilename)

    paperData, questionText = qparser(filePath).parse()
    
    for each in paperData:
        print(each)
        print()
    '''  
    for each in questionText:
        print(each ,questionText[each])
        print()
    '''  
    
    jsonFile = extract(filePath, paperData, {}, qFilename)

    paperData = mparser(msFilename, {}).parse() # also returns the text -- Paper 1 only for now
    jsonFile = extract(msFilename, paperData, jsonFile, qFilename)

    
    textFile = open("questionsPDF/" + qFilename + "/" + qFilename + ".txt", "w")
    
    with open("json/test.json", "w") as f:
        json.dump(jsonFile, f, sort_keys=True, indent=4)
        f.close()
    
    '''
            To avoid calling the PDFsplitters
    textFile = open("questionsPDF/" + qFilename + "/" + qFilename + ".txt", "w")
    jsonFile = {}
    with open("files/test.json","r") as f:
            jsonFile = json.load(f)
    '''
    qName = re.split("[_]", qFilename)

    if qName[0] == "9709":
        for each in jsonFile:
            questionText = pdfToText("questionsPDF/" + qFilename + "/" + jsonFile[each]["questions"] + ".pdf")
            questionText = preprocess(questionText)
            questionText = " ".join(questionText)
            
            try:
                topic = predict(subjectCode, questionText)
                jsonFile[each]["prediction"] = topic
            except Exception as e:
                print(e)
                pass

    else:
        #if qName == "9701-1": qName = "9701-2"
        qName = "9701-2"

        for q in jsonFile:
            qText = questionText[q]
            qText = preprocess(qText)
            qText = " ".join(qText)
            
            try:
                topic = predict(subjectCode, qText)
                jsonFile[q]["prediction"] = topic
            except Exception as e:
                print(e)
                pass

    for eachq in jsonFile:
            print(eachq)
            print(jsonFile[eachq])
            
            textFile.write(str(eachq)+"\n")
            line = (jsonFile[eachq]["questions"])
            textFile.write(str(line)+"\n")
            line = (jsonFile[eachq]["answers"])
            textFile.write(str(line)+"\n")
            textFile.write(str(jsonFile[eachq]["prediction"])+"\n")

    textFile.close()

    # finishing off

    with open("json/test.json", "w") as f:
            json.dump(jsonFile, f)
            f.close()

    # archive all the files in the folder
    shutil.make_archive("questionsPDF/" + qFilename, "zip", "questionsPDF/" + qFilename)


'''
p = 15
for i in range(p, 17):
    for each in ["13"]:
        qFilename = "9608_s" + str(i) + "_qp_" + each

        # extract paper data and get the markingscheme filename
        word = "[_]"
        qName = re.split(word, qFilename)
        qName[2] = "ms"
        msFilename = "_".join(qName)
        subjectCode = qName[0] + "-" + qName[3][0]   # for AI.predict 

        if subjectCode in ["9702-1", "9702-2"]:
            subjectCode = "9702-1" # for physics paper 1 2 3

        print(qFilename, msFilename)
        main()
'''

main()




