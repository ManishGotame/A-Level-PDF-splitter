'''
    This is a parser built for Multiple Choice questions -- mainly for Physics, Chemistry and Biology at the moment
    Separates questions from their respective options to increase the accuracy of questions models training. At least that's what it is built for.
'''

def parseWords(posArray, w):
    s , e = 0, 0 # initially 
    questions = []
    for eachPos in posArray:
        eachPos = eachPos[::-1]
        e = eachPos[0]
        text = w[s:e]
        vals = []
        # calculation of median length of the sentence 
        # right now approximation is used
        # in the real past paper, you can check for the question number to set the length
        for i in range(3):
            sumVal = len(w[eachPos[i]+1: eachPos[i+1]])
            vals.append(sumVal)
        vals = sorted(vals)
        s = eachPos[3] + vals[2] 
        text = " ".join(text)
        questions.append(text)
    return questions

def mcq(words): 
    checkWords = ["D", "C", "B", "A"]
    w = words.split()
    queue = []

    for i in range(len(w)):
        eachWord = w[i]
        if eachWord in checkWords:
            queue.append([eachWord, i])

    queue = queue[::-1]
    pos = 0
    optionsVals = []
    c = []
    while (len(queue) != 0):
        first = queue[0]
        queue.pop(0)
        if pos == 0: c = []
        if (first[0] == checkWords[pos]):
            c.append(first[1]) 
            pos += 1
            if (pos == 4):
                pos = 0
                optionsVals.append(c)

    optionsVals = optionsVals[::-1]
    if len(optionsVals) != 0:
        words = parseWords(optionsVals, w)
        return words
    else: return None


# # testing an idea of parsing multiple choice question papers <= 2016 
# import pdfplumber as pp 

# filename = "9702_s15_ms_11"
# pdf = pp.open("questions/" + filename + ".pdf")
# pages = len(pdf.pages) 

# data = []
# finalData = [] # should store question number, x0, x1, top and bottom for imageExtract to work
# qno = []
# opt = ["A", "B", "C", "D"]
# pageHeight = 800

# for i in range(1, 41):
#     qno.append(str(i))

# for index in range(1, pages):
#     page = pdf.pages[index]
#     pageHeight = pdf.pages[index].height
#     text = page.extract_words()
#     for each in text:
#         if each["bottom"] > 67:
#             print(each["text"])
#             if each["text"] in qno or each["text"] in opt:
#                 data.append(each)


# print(data)

# # assume that the first word in the question number

# for index in range(0, len(data)-1, 2):
#     print(data[index]["text"], data[index+1]["text"])

#     finalDict = {
#         'text': data[index]["text"],
#         'x0': data[index]["x0"],
#         'x1': data[index+1]['x1'],
#         'top': data[index]['top'],
#         'bottom': data[index+1]['bottom']
#     }

#     finalData.append(finalDict)

# i = 0
# res = 200
# for each in finalData:
#     x0 = float(each['x0'])
#     x1 = float(each['x1'])
#     top = float(each['top']) - 5
#     if top < 0: top = 0
#     bottom = float(each['bottom']) + 5
#     if bottom > pageHeight: bottom = pageHeight
    
#     img_bbox = (x0, top, x1, bottom)
#     page = pdf.pages[1]
#     crop_img = page.crop(img_bbox)
#     img = crop_img.to_image(resolution= res)
#     imageTitle = "test-" + str(i) + ".png" 
#     print("cropping and saving", imageTitle) 
#     img.save("images/" + imageTitle)
#     i += 1
