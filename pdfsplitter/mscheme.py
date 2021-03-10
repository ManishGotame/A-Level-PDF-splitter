# pageText in normal parser is only for Paper 1 for now 
# TODO: the answer it returns in the dict is only for Paper 1 MCQs, improve that in the future

# TODO: make it work on any possible quesitons detected in the paper -- it crashes if it cannot detect question number 1 

# this is relatively accurate and faster then v2.0 
# sped some of the processes and removed unnecessary sub-questions parsing 

# we will reorder and rewrite the whole thing bros 

'''
    program flow as far as I understand 
    -> Load pdf -> getfont()  
    -> loop through pdf -> extract questions or answers from a page -> do some logic with them
    -> store them 
    -> get the images -> append some extra images if found -> store them -> return json file  


    qparser - questions json
    aparser - answers json
    -> merge them, if some questions or answers are not found then get rid of them and generate a final pdf
    -> also store the log somewhere to be reviwed for potential identification of bugs
    -> get the json file and upload it to the server 
'''

import os
import re
import pdfplumber as pp
import numpy 
import cv2
import json 
import datetime 
import imutils 
from PIL import PngImagePlugin
LARGE_ENOUGH_NUMBER = 1000 
PngImagePlugin.MAX_TEXT_CHUNK = LARGE_ENOUGH_NUMBER * (1024**2)

from pdfsplitter.utils.funct import imageToText
from pdfsplitter.utils.fonts import get_font

class mparser:
    def __init__(self, fileName, jsonFile):
        self.fileName = fileName
        self.imageDir = fileName
        self.pdf = pp.open(fileName)
        self.pageHeight = 0 
        self.pageWidth = 0
        self.pages = len(self.pdf.pages) 
        self.questionStartLimit =  84 # for detecting partial questions on other pages  
        self.res = 300 # 300 for production 
        self.i = 0
        self.font = None

        self.a1, self.a2, self.a3, self.a4 = [], [], [], []
        for i in range(1, 41):
            self.a1.append(str(i))
            # > 2016 papers -- a sneaky way but it works
            self.a2.append(str(i) + "(a)")
            self.a3.append(str(i) + "(a)(i)")
            self.a4.append(str(i) + "(i)")

        self.mcqList = ["9702-1", "9701-1", "9700-1"] 
        # physics, chemistry and biology

        if jsonFile == {}:
            self.noQ = True
            self.questionsJson = {} # load the json file created from pdfsplitv-3.1.py 
            #qDirectory = os.listdir("images")
            #if self.imageDir not in qDirectory: os.mkdir("images/" + self.imageDir) 
        else:
            self.noQ = False
            self.questionsJson = jsonFile
            # change the fileName to the question paper fileName
            # filename = "9702_s17_ms_11"
            ws = re.split("[_]", self.imageDir)
            self.imageDir = ws[0] + "_" + ws[1]  + "_qp_" + ws[3] # 9702_s17_ms_11 => 9702_s17_qp_11

    def image(self, each, title):
        '''
            Deprecated 
            This is very slow. Instead of extracting images, we are splitting the pdfs 
        '''
        #imgData = [] 
        x0 = float(each['x0'])
        x1 = float(each['x1'])
        top = float(each['top']) - 8
        if top < 0: top = 0
        bottom = float(each['bottom']) + 5
        if bottom > self.pageHeight: bottom = self.pageHeight
        
        img_bbox = (x0, top, x1, bottom)
        page = self.pdf.pages[each["page_number"] - 1]
        crop_img = page.crop(img_bbox)
        img = crop_img.to_image(resolution= self.res)
        imageTitle = str(title) + ".png"
        print("cropping and saving", imageTitle)
        img.save("images/" + self.imageDir + "/" + imageTitle)
        self.i += 1
        return imageTitle

    def extract(self, questions):
        '''
            Deprecated
        '''
        # get the cropped images, store them, returns their filename, create json file withthe sturcture and return it 
        for each in questions:
            partVal = 1
            qImages = []
            questionNumber = each["text"]
            #print("question number = ", questionNumber)
            #print(each) 
            
            # title = "ans-" + each["text"] + "--" + str(self.i)
            title = self.fileName + "-" + each["text"] + "-" + str(partVal) + "-" + str(self.i)

            imgTitle = self.image(each, title)  
            qImages.append(imgTitle) 

            if each["more"] != []:
                # sub questions exist
                subQ = each["more"]
                for eachQ in subQ:
                    #title = each["text"] + "--" + str(self.i)
                    title = self.fileName + "-" + each["text"] + "-" + str(partVal) + "-" + str(self.i)
                    imgTitle = self.image(eachQ, title)
                    qImages.append(imgTitle)
            
            if self.noQ == True:
                self.questionsJson[str(questionNumber)] = {
                        'questions' : [],
                        'answers' : [],
                        'prediction' : ""
                }

            for each in qImages: self.questionsJson[str(questionNumber)]['answers'].append(each)     
        return self.questionsJson 
    
    def checkFont(self, wordFont): 
        '''
            if a font was found, use that to check for question numbers
            else: use the boundary logic to look for question number for which fontcheck should be true
        '''
        if self.font != "":
            if wordFont == self.font:
                return True
            else: return False
        else: return True 

    def mcqParser(self): # for multiple choice paper 1 only upto 2016  
        # this is the first iteration -- should be buggy 
        print("mcq parser")
        parsedQuestions = []
        data = []
        qno = []
        opt = ["A", "B", "C", "D"]

        for i in range(1, 41):
            qno.append(str(i))

        for index in range(1, self.pages):
            page = self.pdf.pages[index]
            self.pageHeight = float(page.height)
            self.pageWidth = float(page.width)

            text = page.extract_words(extra_attrs=["page_number"])

            for each in text:
                if each["bottom"] > 67:
                    if each["text"] in qno or each["text"] in opt:
                        data.append(each)

        # TODO: I think the boundary margins are being messed up from here
        for index in range(0, len(data)-1, 2):
            #print(data[index]["text"], data[index+1]["text"])
            finalDict = {
                'text': data[index]["text"],
                'answer': data[index+1]["text"],
                'x0': data[index]["x0"] -5 ,
                'x1': data[index+1]['x1'] + 5,
                'top': data[index]['top'] + 10,
                'bottom': data[index+1]['bottom'] - 1,
                'page_number': data[index]["page_number"],
                'more': []}
            parsedQuestions.append(finalDict)
        
        #return self.extract(parsedQuestions)
        return parsedQuestions
        
    def checkQuestion(self, word):
        '''
            some question papers have question order as 10, 10(a), 10(b)
            This caused the parser to identiy the first and second as separate questions
            Fix: remove 10(a) 10(a)(i) once 10 is found and repeat the same if another is found
        
            TODO: does this work on 2(i) or not?
            answer: No
            Fix: 
        '''
        found = False
        for index in range(len(self.a1)):
            if word == self.a1[index]:
                found = True
            elif word == self.a2[index]:
                found = True
            elif word == self.a3[index]:
                found = True
            elif word == self.a4[index]:
                found = True
            
            if found == True:
                self.a2.pop(index)
                self.a3.pop(index)
                self.a1.pop(index)
                self.a4.pop(index)
                return True
        
        return False

    def normalParser(self):
        '''
            parser for papers with normal questioning -- no MCQ style marking scheme
        '''
        limit = (0.15 * float(self.pdf.pages[0].width) + 15)
        allowedWords1 = ("(a) (b) (c) (d) (e) (f) (g) (h)").split() 
        allowedWords2 = ("(i) (ii) (iii) (iv) (v) (vi) (vii) (viii)").split()
        # allowedWords1 will have more priority than allowedWords2 
        
        self.font = get_font(self.fileName) 

        # allowedWords = [] # 1 to 40 numbers 
        
        prioritySet = None # either allowedWords1 or allowedWords2  
        parsedPages = []
        parsedQuestions = []
        limit = (0.15 * float(self.pdf.pages[0].width) + 15)
        
        # for extracting the text
        pageText = []
        textChars = ""
        prevQno = ""

        for index in range(1, self.pages):
            #font = self.pdf.pages[index].chars[0]['fontname'] # takes the topmost font of a page number -----> changes here, need to get the limit using sub-questions - (a) or (ii)
            page = self.pdf.pages[index]
            text = page.extract_words(extra_attrs=["fontname", "page_number", "top", "bottom"])
            upperLimit = 0 # for marksPoint 
            questions = []
            marksPoint = None # at the end of the page, this stores the last marks point 
            self.pageHeight = float(page.height)
            self.pageWidth = float(page.width)
            

            for each in text:
                textChars += each["text"] + " "
                #print(each, self.checkFont(each["fontname"]))
                if self.checkFont(each["fontname"]) and each['x0'] < limit and each["bottom"] > 67:
                    #print(each)
                    #print()

                    if prioritySet == None:
                        if each["text"].strip() in allowedWords1:
                            # priority 1
                            prioritySet = "allowedWords1"
                            limit = float(each["x0"])

                        elif each["text"].strip() in allowedWords2:
                            # priority 2
                            prioritySet = "allowedWords2"
                            limit = float(each["x0"])

                    elif prioritySet == "allowedWords2":
                        if each["text"].strip() in allowedWords1:
                            # priority 1 
                            prioritySet = "allowedWords1"
                            limit = float(each["x0"])
                    
                    if self.questionStartLimit == 0 and each["text"].strip() == "1":
                        self.questionStartLimit = float(each["bottom"]) # TODO: y1 or bottom or top
                    
                    if self.checkQuestion(each["text"]):
                        # text extract
                        if len(pageText) == 0:
                            prevQno = each["text"]
                            pageText.append(["empty"])
                        else:
                            pageText.append([prevQno, textChars.split()[0] ])
                            prevQno = each["text"]
                        textChars = ""
                        # ends here

                        if index not in parsedPages: parsedPages.append(index)
                        
                        # if a question's bottom is greater than self.questionStartLimit than the previous question is not complete and partial question is on another page
                        if float(each["bottom"]) > self.questionStartLimit and questions == []:
                            #print(each, self.questionStartLimit) 
                            # TODO: and maybe here
                            pageData = {
                                    'x0' : 0,
                                    'x1' : self.pageWidth, 
                                    'top' : self.questionStartLimit,
                                    'bottom' : each['top'],
                                    'page_number' : each['page_number'],
                                    'answer': ""
                                }

                            lastIndex = len(parsedQuestions) - 1
                            if float(pageData['bottom']) - float(pageData['top']) > 0 and lastIndex != -1:
                                parsedQuestions[lastIndex]['more'].append(pageData) 
                        
                        #print(each["text"], "===>", each["fontname"], each["page_number"])
                        print("Question: ", each["text"], each["page_number"])
                        each["x0"] = float(0)
                        each['more'] = []
                        upperLimit = each["bottom"]
                        
                        questions.append(each)

            # fix the height and width of nth question to n+1 question 
            for i in range(len(questions)):
                if i != len(questions) - 1:
                    questions[i]["x1"] = self.pageWidth 
                    #questions[i]["x1"] = questions[i+1]["x1"]
                    questions[i]["bottom"] = questions[i+1]["top"]
                else:
                    if marksPoint != None:
                        # take the last question from parsedQuestion and change its x1 and y0 value 
                        questions[i]["x1"] = self.pageWidth
                        #questions[i]["x1"] = marksPoint["x1"]
                        questions[i]["bottom"] = marksPoint["bottom"] + 5  
                    else:
                        # set the height and width as x1 and y0
                        questions[i]["x1"] = self.pageWidth
                        questions[i]["bottom"] = self.pageHeight
                
                parsedQuestions.append(questions[i]) 
                #print(self.pageWidth, self.pageHeight) 
            
            # after the page is parsed -- if the questions exist -- check if it was empty or not

            if index not in parsedPages: # this means [questions] array is empty 
                parsedPages.append(index)
                text = ""
                for each in page.chars: text += each["text"]
                # go through the page and find any marksPoint, if point, crop it upto that point
                # else go the normal route of taking the entire page
                marksPoint = None

                for each in page.extract_words(extra_attrs=["top", "bottom"]):
                    #if each["text"] in marks: marksPoint = each
                    for eachChar in each["text"]:
                        if eachChar == "]":
                            marksPoint = each
                            marksPoint = None # marking scheme has some issues with this  

                lastIndex = len(parsedQuestions) - 1
                if marksPoint != None:
                    pageData = {
                        'x0' : 0,
                        'x1' : float(self.pageWidth),
                        'top' : 0,
                        'bottom' : float(marksPoint["bottom"]), # change here 
                        'page_number' : int(index + 1),
                        'answer': ""
                    }
                    parsedQuestions[lastIndex]["more"].append(pageData)
                
                elif len(text) > 80:
                    # the page is not an empty page
                    pageData = {'x0': 0, 
                                'x1': float(self.pageWidth), 
                                'top': 0 , 
                                'bottom': float(self.pageHeight), 
                                "page_number": int(index+1),
                                'answer': ""
                    }

                    #print(questions[lastIndex]["more"])
                    if parsedQuestions != []:
                        parsedQuestions[lastIndex]["more"].append(pageData)

                else: print("Blank Page")
        
        pageText.append([prevQno, textChars.split()[0]])
        for each in parsedQuestions: self.cleanup(each)
        
        pageText = pageText[1:]  

        for index in range(len(parsedQuestions)):
            parsedQuestions[index]["answer"] = str(pageText[index][1])

        '''
        for each in parsedQuestions:
            print(each["text"])
            print()
        '''

        #return self.extract(parsedQuestions)
        return parsedQuestions 
    
    def cleanup(self, eachq):
        eachq["bottom"] -= 5
        eachq["top"] += 5
        # This should be buggy  
        '''
            This issue has not been found in pdfsplit-v3.1 yet but in markingscheme
            1(a) - return 1
            4(a)(i) - return 4 
            we're not doing sub-question splitting (that idea was discarded after seeing its unreliability) thus, only return number 
        
            input -> {'text': '1(a)', 'x0': 0.0, 'x1': 842.0, 'top': Decimal('81.757'), 'bottom': 595.0, 'upright': True, 'direction': 1, 'fontname': 'LALAAJ+Arial', 'page_number': 4, 'more': []}  
        
            output -> {'text': '1', 'x0': 0.0, 'x1': 842.0, 'top': Decimal('81.757'), 'bottom': 595.0, 'upright': True, 'direction': 1, 'fontname': 'LALAAJ+Arial', 'page_number': 4, 'more': []}

            simply storing question numbers until we get "("
        '''
        qNumber = ""
        for e in eachq['text']:
            if e != "(": qNumber += e
            else: break 
        
        eachq['text'] = qNumber 

    def parse(self): # the main deal is here
        # do some logic here and then got for normal or mcqparser
        qName = re.split("[_]", self.fileName)
        subCode = qName[0] + "-" + qName[len(qName)-1][0]
        year = int("20" + qName[1][1:])

        if subCode in self.mcqList and year <= 2016: return self.mcqParser()
        else: return self.normalParser()        


if __name__ == "__main__": 
    filename = "9231_s05_qp_2"
    filename = "9709_m20_qp_32"
    #filename = "9700_w13_qp_42"
    #filename = "9702_s12_qp_13"
    #filename = "9608_w17_qp_22"
    #filename = "9709_s17_qp_12"
    #filename = "9700_s13_qp_11"
    #filename = "9701_s16_qp_21"
    #filename = "9700_s16_qp_22"
    #filename = "9709_s10_qp_21"
    #filename = "9709_s14_qp_43"
    #filename ="9709_s03_qp_6"
    #filename = "9709_s14_qp_53"
    # filename = "7010_s14_qp_12" #- ordering bug paper 
    #filename = "9791_s16_qp_02"
    #filename = "9709_s14_qp_63"
    # filename = "9231_s12_qp_22"
    #filename = "9702_s09_qp_4"
    #filename = "9608_s16_ms_23"
    # filename = "9709_w10_ms_11"
    # filename = "9701_s13_ms_22" # works 100% fine 
    #filename = "9701_s11_ms_21" 
    # filename = "9702_s05_ms_2" # failed to detect question number 1 -- its font was slightly different other questions 
    #filename = "9709_s16_ms_23"
    #filename = "9702_s10_ms_43"
    #filename = "9700_s14_ms_21"
    filename = "9990_s18_ms_22"
    # filename = "9702_s18_ms_22"
    # filename = "9608_s16_ms_11"
    # filename = "9702_s17_ms_11"

    # filename = "9702_w18_ms_42"
    filename = "9794_s16_ms_01"
    filename = "9709_s19_ms_22"
    filename = "9702_w18_ms_42"
    filename = "9702_s18_ms_22"
    #filename = "9702_s10_ms_43"
    filename = "9709_s19_ms_22"
    filename = "9608_s16_ms_11"
    filename = "9702_w19_ms_11"
    # filename = "9702_s15_ms_11"
    # filename = "9702_s15_ms_11"
    filename = "9702_s14_ms_42"

    '''
    with open("files/" + filename + ".json", "w") as f:
        json.dump(fileData, f, sort_keys=True, indent=4)
        f.close()
    '''
    
    x = mparser(filename, {}).parse()

    for each in x:
        print(each)
        print()

    '''
    for each in x:
        print(each, x[each])

        for eachOne in x[each]['answers']:
            img = cv2.imread("images/" + eachOne)
            img = imutils.resize(img, 600)
            cv2.imshow(str(each), img)
            cv2.waitKey(0)
    '''

















