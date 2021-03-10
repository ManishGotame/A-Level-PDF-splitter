# TODO: unstable 
# pdfsplit-v3.1.py
# Currently under development of Manish Gotame
# this is relatively accurate and faster then v3.0 
# sped some of the processes and removed unnecessary sub-questions parsing 

# TODO: Comparmentalize the code in the future for reusabilty and inheritance
# TODO: get rid of marksPoint -- unstable, for now, they have been commented out  
# TODO: get rid of that if no other solution suffice 

'''
    why did I not built the prediction into this? Because this code should be able to parse through
    any file without having its AI model built in the first place. So, that lives in sandbox-v2
'''

import os 
import re
import pdfplumber as pp
import numpy 
import cv2
import json 
import datetime 
from PIL import PngImagePlugin
LARGE_ENOUGH_NUMBER = 1000 
PngImagePlugin.MAX_TEXT_CHUNK = LARGE_ENOUGH_NUMBER * (1024**2)

# mainlib stuffs
#from funct import imageToText # TODO: rename funct to utils  
from pdfsplitter.utils.funct import imageToText

# TODO: change the images' name to datetime from random numbers 

# Fixed : In maths paper marksPoint is causing the paper to be cut without their answer space

# TODO: store the text too for prediction sentences to be as accurate as possible
# MCQparser cannot work on ImageToText generated text
# maybe store an extra json file containing the text of the questions for sandbox-v2 to use for prediction

class qparser:
    def __init__(self, fileName):
        self.fileName = fileName
        #self.pdf = pp.open(fileName + ".pdf")
        self.pdf = pp.open(fileName)
        self.pageHeight = 0 
        self.pageWidth = 0
        self.pages = len(self.pdf.pages) 
        self.questionStartLimit = 0 # for detecting partial questions on other pages  
        self.res = 300 # 300 for production 
        self.i = 0
        self.questionsJson = {}
        self.questionsText = {}
        
        # TODO: uncommented for now, if its causes issues, fix this
        #qDirectory = os.listdir("images")
        #if self.fileName not in qDirectory: os.mkdir("images/" + self.fileName)

    def image(self, each, title):
        # TODO: this is so slow

        x0 = float(each['x0'])
        x1 = float(each['x1'])
        top = float(each['top']) - 15
        if top < 0: top = 0
        bottom = float(each['bottom'])
        if bottom > self.pageHeight: bottom = self.pageHeight
        
        img_bbox = (x0, top, x1, bottom)
        page = self.pdf.pages[each["page_number"] - 1]
        crop_img = page.crop(img_bbox)
        img = crop_img.to_image(resolution= self.res)
        imageTitle = str(title) + ".png" 
        print("cropping and saving", imageTitle) 
        img.save("images/" + self.fileName + "/" + imageTitle)
        self.i += 1
        return imageTitle

    def extract(self, questions):
        # get the cropped images, store them, returns their filename, create json file withthe sturcture and return it 
        for each in questions:
            partVal = 1
            qImages = []
            questionNumber = each["text"]
            #print("question number = ", questionNumber)
            #print(each) 
            
            # title = each["text"] + "--" + str(self.i)
            title = self.fileName + "-" + each["text"] + "-" + str(partVal) + "-" + str(self.i)
            imgTitle = self.image(each, title)  
            qImages.append(imgTitle) 

            if each["more"] != []:
                partVal += 1
                # sub questions exist
                subQ = each["more"]
                for eachQ in subQ:
                    # title = each["text"] + "--" + str(self.i)
                    title = self.fileName + "-" + each["text"] + "-" + str(partVal) + "-" + str(self.i)
                    imgTitle = self.image(eachQ, title)
                    qImages.append(imgTitle)
            
            self.questionsJson[str(questionNumber)] = {
                    'questions' : [],
                    'answers' : [],
                    'prediction' : ""
            }

            for each in qImages: self.questionsJson[str(questionNumber)]['questions'].append(each)     
        return self.questionsJson 

    def parse(self): # the main deal is here 
        limit = (0.15 * float(self.pdf.pages[0].width) + 15)
        allowedWords1 = ("(a) (b) (c) (d) (e) (f) (g) (h)").split() 
        allowedWords2 = ("(i) (ii) (iii) (iv) (v) (vi) (vii) (viii)").split()
        # allowedWords1 will have more priority than allowedWords2 
        
        allowedWords = [] # 1 to 40 numbers 
        for i in range(1, 41):
            allowedWords.append(str(i))
        
        prioritySet = None # either allowedWords1 or allowedWords2  
        parsedPages = []
        parsedQuestions = []
        limit = (0.15 * float(self.pdf.pages[0].width) + 15)
        pageText = []
        textChars = ""
        prevQno = ""


        for index in range(1, self.pages):
            font = self.pdf.pages[index].chars[0]['fontname'] # takes the topmost font of a page number -----> changes here, need to get the limit using sub-questions - (a) or (ii)
            page = self.pdf.pages[index]
            text = page.extract_words(extra_attrs=["fontname", "page_number", "top", "bottom"])
            upperLimit = 0 # for marksPoint 
            questions = []
            marksPoint = None # at the end of the page, this stores the last marks point 
            self.pageHeight = float(page.height)
            self.pageWidth = float(page.width)

            for each in text:
                textChars += each["text"] + " "
                if each["fontname"] == font and each['x0'] < limit:
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
                    
                    if each["text"] in allowedWords:
                        print()
                        # print("a", textChars, each["text"])
                        # print(pageText)
                        # pageText.append([ int(each["text"]) - 1, textChars])
                        # textChars = ""

                        if each["text"] == "1":
                            prevQno = each["text"]
                        else:
                            pageText.append([prevQno, textChars])
                            prevQno = each["text"]
                        textChars = ""

                        print()
                        # pageText.append(textChars)
                        if index not in parsedPages: parsedPages.append(index)
                        
                        # if a question's bottom is greater than self.questionStartLimit than the previous question is not complete and partial question is on another page
                        if float(each["bottom"]) > self.questionStartLimit and questions == []:
                            print(each, self.questionStartLimit) 
                            pageData = {
                                    'x0' : 0,
                                    'x1' : self.pageWidth, 
                                    'top' : self.questionStartLimit,
                                    'bottom' : each['top'],
                                    'page_number' : each['page_number']
                                }

                            lastIndex = len(parsedQuestions) - 1
                            if pageData['top'] < pageData['bottom']:
                                parsedQuestions[lastIndex]['more'].append(pageData) 
                        
                        #print(each["text"], "===>", each["fontname"], each["page_number"])
                        print("Question: ", each["text"])
                        each["x0"] = float(0)
                        each['more'] = []
                        upperLimit = each["bottom"]
                        # textChars = ""
                        
                        questions.append(each)


                #if each["text"] in marks: marksPoint = each # keeps changing until the last marksPoint is found
                if questions != []:
                    for eachChar in each["text"]: # keeps changing until the last marksPoint is found
                        if eachChar == "]" and each["bottom"] > upperLimit and questions[len(questions) -1]["page_number"] == each["page_number"] and each["bottom"] > 0.80 * float(self.pageWidth):
                            #print("char==========>", eachChar, each["page_number"])
                            marksPoint = each

            # fix the height and width of nth question to n+1 question 
            for i in range(len(questions)):
                if i != len(questions) - 1:
                    questions[i]["x1"] = self.pageWidth 
                    #questions[i]["x1"] = questions[i+1]["x1"]
                    questions[i]["bottom"] = questions[i+1]["top"]
                else:
                    marksPoint = None
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
                
                lastIndex = len(parsedQuestions) - 1
                marksPoint = None
                
                if marksPoint != None:
                    pageData = {
                        'x0' : 0,
                        'x1' : float(self.pageWidth),
                        'top' : 0,
                        'bottom' : float(marksPoint["bottom"]), # change here 
                        'page_number' : int(index + 1)
                    }
                    parsedQuestions[lastIndex]["more"].append(pageData)
                
                elif len(text) > 80:
                    # the page is not an empty page
                    pageData = {'x0': 0, 
                                'x1': float(self.pageWidth), 
                                'top': 0 , 
                                'bottom': float(self.pageHeight), 
                                "page_number": int(index+1) 
                    }

                    #print(questions[lastIndex]["more"])
                    if parsedQuestions != [] and pageData['top'] < pageData['bottom']:
                        print(pageData)
                        print()
                        parsedQuestions[lastIndex]["more"].append(pageData)

                else: print("Blank Page")
                # if index == 5: exit(0)
        
        pageText.append([prevQno, textChars])

        # pageText has an issue -- reading the text from the library causes mathematics paper 2 to multiple sentence as a single word
        # this causes the classifier to make incorrect prediction
        for var in pageText:
            # TODO: please look for other better cleanup module in AI or somewhere, i think i did a better one before
            finalCollect  = ""
            # for each in var[1]:
            #     if ord(each) >= 97 and ord(each) <= 122 or ord(each) >= 65 and ord(each) <= 90:
            #         fText += each
            #     elif ord(each) == 32: fText += each
            #     elif each == "UCLES": break
            
            # print(var[1])

            for eachWord in var[1].split():
                fText = ""

                if eachWord == "UCLES": break

                if eachWord.lower().strip() != "cid":
                    for eachChar in eachWord:
                        if ord(eachChar) >= 97 and ord(eachChar) <=122 or ord(eachChar) >= 65 and ord(eachChar) <= 90:
                            fText += eachChar.lower()

                    if fText != "": finalCollect += fText + " "

            self.questionsText[var[0]] = finalCollect

        for each in parsedQuestions:
            each["bottom"] -= 5
        
        '''
            getting rid of that last CIE stuff from the last page
            -> find the last page -- can be straight forward or look into more
            -> change the value of bottom from pageHeight to pageHeight - some arbitrary number
        ''' 

        val = 130
        index = len(parsedQuestions) - 1
        if parsedQuestions[index]["more"] != []:
            moreLastIndex = len(parsedQuestions[index]["more"]) - 1
            parsedQuestions[index]["more"][moreLastIndex]["bottom"] -= val
        else:
            parsedQuestions[index]["bottom"] -= val

        #return self.extract(parsedQuestions), self.questionsText
        return parsedQuestions, self.questionsText

if __name__ == "__main__": 
    filename = "9231_s05_qp_2"
    filename = "9709_m20_qp_32"
    #filename = "9700_w13_qp_42"
    #filename = "9702_s03_qp_1"
    #filename = "9608_w17_qp_22"
    #filename = "9709_s17_qp_12"
    #filename = "9701_s16_qp_21"
    #filename = "9700_s16_qp_22"
    #filename = "9709_s10_qp_21"
    #filename = "9709_s14_qp_43"
    #filename ="9709_s03_qp_6"
    #filename = "9709_s14_qp_53"
    #filename = "7010_s14_qp_12" #- ordering bug paper 
    #filename = "9791_s16_qp_02"
    #filename = "9709_s14_qp_63"
    #filename = "9231_s12_qp_22"
    #filename = "9702_s09_qp_4"
    #filename = "9709_s13_qp_22"

    # filename = "9700_s13_qp_11"
    # filename = "9702_s12_qp_13"
    #filename = "9709_s13_qp_22"
    #filename = "9794_s16_qp_01"
    #filename = "9794_s16_qp_03"
    filename = "9702_s16_qp_32"
    filename = "9702_s18_qp_22"
    
    filename = "9702_s15_qp_42"
    filename = "9702_s12_qp_13"
    '''
    with open("files/" + filename + ".json", "w") as f:
        json.dump(fileData, f, sort_keys=True, indent=4)
        f.close()
    '''
   
    x, y = qparser(filename).parse()

    # print(self.questionsText)    
    # for each in x:
    #     print(each, x[each])

    for each in y:
        print(each)
        print()
        print(y[each])














