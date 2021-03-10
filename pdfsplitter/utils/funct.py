# most of our called functions are stored here
# maybe v2 will get moved here one day, I don't know

import pytesseract as ts
ts.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from PIL import Image
import fitz
import cv2 

def preprocess(sent):
    final = []
    sent = sent.split()
    for eachW in sent:
        rawWord = ""
        for ec in eachW:
            if ord(ec) >= 65 and ord(ec) <= 90 or ord(ec) >= 97 and ord(ec) <= 122: 
                rawWord += ec
        final.append(rawWord)
    newF = []
    for each in final:
        if len(each) != 1 and each != '':
            newF.append(each)
    return newF

def calcScore(eachTopic, allTopic):
    # no use at this point 
    # discared idea 
    import math
    totalDoc = len(allTopic)
    uniqueWords = set(eachTopic)
    tDict = {}
    for eachWord in uniqueWords:
        termFreq = eachTopic.count(eachWord)
        docFreq = 0

        for eachT in allTopic:
            if (eachT.count(eachWord) != 0):
                docFreq += 1
        score = termFreq * math.log(totalDoc/docFreq)
        tDict[eachWord] = score
    return tDict

def processSents(sent):
    final = []
    sent = sent.split()
    for eachW in sent:
        rawWord = ""
        for ec in eachW:
            if ord(ec) < 129:    
                rawWord += ec
        final.append(rawWord)
    newF = []
    for each in final:
        if len(each) != 1 and each != '':
            newF.append(each)
    sent = " ".join(newF)
    return sent 

def getContentTableDirect(parser):
    from pdfminer.pdfparser import PDFParser 
    from pdfminer.pdfdocument import PDFDocument
    
    password = ""
    document = PDFDocument(parser, password)
    outlines = document.get_outlines()
    chapterLevel = 1
    chapter = []
    for (level, title, dest, a, se) in outlines:
        if title[:7] == "Chapter" and len(title) >= 12:  
            chapter.append(title)
            chapter.append("") # this just to align the array with index pos
    return chapter

def getContentTable(bookN): # this is for other scripts to load the book content
    from pdfminer.pdfparser import PDFParser 
    from pdfminer.pdfdocument import PDFDocument
    
    fp = open(bookN, "rb")
    parser = PDFParser(fp)
    
    password = ""
    document = PDFDocument(parser, password)
    outlines = document.get_outlines()
    chapterLevel = 1
    chapter = []
    for (level, title, dest, a, se) in outlines:
        if title[:7] == "Chapter" and len(title) >= 12:  
            chapter.append(processSents(title[11:].lstrip()))
    return chapter

def imageToText(img):
    text = ts.image_to_string(img)
    text = text.replace("\n", " ")
    return text 

def pdfToText(fileLoc):
    '''
        currently this is only used for Mathematics because some genius thought it would be better to build a pdf without proper knowledge
        the parser can handle the textExtract from other papers except for mathematics whose texts just gets concatenated to one another  
        
        for getting the text out of pdf by converting them into images
        -> currently the pdf cropping is bad so the pdf store all the text even after cropping which is makes the AI to return incorrect predictions
        -> Parser can return the text but it fails with Mathematics thus this module has been created to handle that problem for now. 

        -> get the pdf location, go through each page and extract the image and gextract the text from them, return all the text


        -> Maybe a good idea to use both text extract and image extract and compare both prediction and ultimately use the image extract prediction?

    '''
    
    doc = fitz.open(fileLoc)
    mat = fitz.Matrix(2,2)
    text = ""

    for epage in doc:
        pix = epage.getPixmap(matrix=mat)
        pix.writePNG("pdfsplitter/images/temp/test.png")

        img = cv2.imread("pdfsplitter/images/temp/test.png")
        
        text += imageToText(img)
    
    return text 










