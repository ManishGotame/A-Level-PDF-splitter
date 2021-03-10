'''
    get_font module currently used by marking_scheme 
'''


# font extractor -- extracts the font used by the question numbers and sub-question numbers
import pdfplumber as pp

# we need a better separator for this to work more accurately 

# -> this does not work on paper 1
# -> we need a to build a greedy algorithm that can store the quesiton and sub-questions
# -> this code will only work on marking scheme--accurately 

'''
fontname -> collect the question number and sub question
-> also use the index to store their position
-> find the correct font using the separator
-> after it is found -> group their position -> store them
-> present them in a way that markingscheme requires and return them 
'''

'''
    This code has been updated to work with markingscheme_v2.1.py
    It is only extracting the font belonging to the questions and returning that
'''

# TODO: it works for now, may fail in the future
ac = open("pdfsplitter/utils/allowed_chars.txt", "r").read()
allowed_chars = ac.split()
allowed_number = allowed_chars[:39] # 1 to 40
allowed_number.append("0") # this is specifically for sep module for question number 10, 20, 30

class Pos:
    def __init__(self, v, p):
        self.val = v
        self.pos = p 

def get_median(num_list):
    return num_list[int(len(num_list) + 1/ 2)]

def sep(word):
    # maybe simplify in the future
    '''
        1abcd(a)(b) => separates all the number along with their position ->[1,0]
        1abcd(a)(b) => separates all the sub questions along with their position -> [(a), 5]
        then on the basis of the 0th position of both arrays, a final array is created hopefully with only numbers and sub-question
        then on the basis of the 0th position of both arrays, a final array is created hopefully with only numbers and sub-questions
    '''
    #print(word) 
    subq_list = [] 
    temp_text = "" 
    tempNum_pos = []
    final = []

    num_list = []
    
    for i in range(len(word)):
        each = word[i]

        if i >= len(word) - 1:
            if each in allowed_number: num_list.append(Pos(each, i))
        elif each in allowed_number:
            if word[i+1] in allowed_number:
                each += word[i+1]
                num_list.append(Pos(each, i))
            else:
                num_list.append(Pos(each, i))

    '''
    for each in num_list:
        print(each.val, each.pos) 
    '''
    
    for i in range(len(word)):
        each = word[i]
        temp_text += each
        
        if each == "(":
            temp_text = temp_text[:(len(temp_text)-1)]
            #if len(temp_text) != 0: subq_list.append(Pos(temp_text, i))
            
            temp_text = ""
            temp_text += each

        elif temp_text != "" and each != ")":
            pass
            #temp_text += each

        elif each == ")" and temp_text != "":
            #temp_text += each
            subq_list.append(Pos(temp_text, i))
            #final.append(temp_text)
            
            temp_text = ""

    #if final == []: final.append(word)
    
    '''
    for each in subq_list:
        print(each.val, each.pos) 

    print(len(subq_list), len(num_list)) 
    '''
    
    lim = 0 
    if len(subq_list) >= len(num_list): lim = len(subq_list)
    else: lim = len(num_list) 
    
    while len(subq_list) != 0 or len(num_list) != 0:
        if len(subq_list) == 0:
            final.append(num_list[0].val)
            num_list.pop(0)
        elif len(num_list) == 0:
            final.append(subq_list[0].val)
            subq_list.pop(0)
        else:
            if num_list[0].pos < subq_list[0].pos:
                final.append(num_list[0].val)
                num_list.pop(0)
            else:
                final.append(subq_list[0].val)
                subq_list.pop(0)
    
    #print(final) 
    #exit(0)
    return final 


def cleanup(questionData, questionMetadata):
    #print(questionData)
    qData = []
    qMetadata = []

    temp_metadata = [[],[],[],[],[],[],[]]
    temp_text = ""
    prevVal = [0,0] # 0 -> bottom value 1 -> page number 
    for i in range(len(questionData)):
        if (questionMetadata[i][5] != prevVal[0] or questionMetadata[i][6] != prevVal[1]) and prevVal != [0,0]:
            qData.append(temp_text)
            dataDict = {}

            dataDict['x0'] = min(temp_metadata[0])
            dataDict['x1'] = max(temp_metadata[1])
            dataDict['y0'] = temp_metadata[2][0]
            dataDict['y1'] = max(temp_metadata[3])
            dataDict['top'] = min(temp_metadata[4])
            dataDict['bottom'] = temp_metadata[5][0]
            dataDict['page_number'] = temp_metadata[6][0] - 1
            
            qMetadata.append(dataDict)
            #qMetadata.append([min(temp_metadata[0]), max(temp_metadata[1]), temp_metadata[2][0], max(temp_metadata[3]), min(temp_metadata[4]), temp_metadata[5][0], temp_metadata[6][0]])
            temp_text = ""
            prevVal = [0,0] 
            temp_metadata = [[],[],[],[],[],[],[]]
        
        if prevVal == [0,0] or prevVal == [questionMetadata[i][5], questionMetadata[i][6]]:
            temp_text += questionData[i]
            for index in range(7): temp_metadata[index].append(questionMetadata[i][index])
            
            prevVal = [questionMetadata[i][5], questionMetadata[i][6]]
    qData.append(temp_text)

    dataDict = {}

    dataDict['x0'] = min(temp_metadata[0])
    dataDict['x1'] = max(temp_metadata[1])
    dataDict['y0'] = temp_metadata[2][0]
    dataDict['y1'] = max(temp_metadata[3])
    dataDict['top'] = min(temp_metadata[4])
    dataDict['bottom'] = temp_metadata[5][0]
    dataDict['page_number'] = temp_metadata[6][0] - 1
        
    qMetadata.append(dataDict)
    #qMetadata.append([min(temp_metadata[0]), max(temp_metadata[1]), temp_metadata[2][0], max(temp_metadata[3]), min(temp_metadata[4]), temp_metadata[5][0], temp_metadata[6][0]])

    t_q = qData
    t_mq = qMetadata
    qData = []
    qMetadata = []
    
    # separate them now
    #for each in qData: print(each, sep(each)) 
    
    for index in range(len(t_q)):
        words = sep(t_q[index])
        for each in words:
            each = each.strip()
            if each in allowed_chars:
                qData.append(each)
                qMetadata.append(t_mq[index])
    final = []
    for index in range(len(qData)):
        #print(qData[index], qMetadata[index])
        final.append([qData[index], qMetadata[index]])
    
    return final 

def get_font(filename): 
    check_list = ["(i)", "(ii)", "(iii)", "(iv)", "(v)", "(a)", "(b)", "(c)", "(d)","(e)", "(f)"]

    #with pp.open("questions/" + filename + ".pdf") as pdf:  
    #pdf = pp.open("questions/" + filename + ".pdf")
    pdf = pp.open(filename) 
    pageHeight = float(pdf.pages[1].height)
    pageWidth = float(pdf.pages[1].width)
    noPages = len(pdf.pages)
    
    font_name = []
    dictionary_font ={}
    charMetadata = {}

    upperLimit = 60
    distFromLowPage = 38 
    x0Limit = 125 # this has to be experimented upon
    x0Limit = 0.25 * pageWidth 
    for index in range(1, noPages):
        word = pdf.pages[index]
        allchars = word.chars
        text = "" 
        for each in allchars:
            text += (each['text'])
            if each['fontname'] not in font_name and each['text'] != " " and each['bottom'] > upperLimit and each['x0'] < x0Limit and each['bottom']< pageHeight - distFromLowPage:
                font_name.append(each['fontname'])
                dictionary_font[each['fontname']] = []
                dictionary_font[each['fontname']].append(each['text'])
                charMetadata[each['fontname']] = []
                
                x0_val = float(each['x0'])
                x1_val = float(each['x1'])
                y0_val = float(each['y0'])
                y1_val = float(each['y1'])
                top_val = float(each['top'])
                bottom_val = float(each['bottom'])
                pageNumber = each['page_number']
                
                charMetadata[each['fontname']].append([x0_val, x1_val, y0_val, y1_val, top_val, bottom_val, pageNumber])
            else:
                if each['x0'] < x0Limit and each['text'] != " " and each['bottom'] > upperLimit and each['bottom'] < pageHeight - distFromLowPage:
                    dictionary_font[each['fontname']].append(each['text'])
                    x0_val = float(each['x0'])
                    x1_val = float(each['x1'])
                    y0_val = float(each['y0'])
                    y1_val = float(each['y1'])
                    top_val = float(each['top'])
                    bottom_val = float(each['bottom'])
                    pageNumber = each['page_number']
                    
                    charMetadata[each['fontname']].append([x0_val, x1_val, y0_val, y1_val, top_val, bottom_val, pageNumber])
        #print(text)


    fontName = ""
    maxScore = 0 
    for eachFontname in font_name:
        currentScore = 0
        textData = "".join(dictionary_font[eachFontname])
        
        subqData = sep(textData)
        
        # for each in subqData:
        #     print("what", each)
        # print()


        for eachChar in subqData: 
            if eachChar in check_list:
                currentScore += 1
        
        if currentScore > maxScore:
            maxScore = currentScore
            fontName = eachFontname 

        #print("=====", eachFontname, "====", currentScore) 
        word = "".join(dictionary_font[eachFontname])
        #print(word) 
        #print()

    #print()
    #print(fontName)
    
    '''    
    for index in range(len(dictionary_font[fontName])):
        print(dictionary_font[fontName][index], charMetadata[fontName][index])
    #charMetadata[fontName].pop(2)
    collect = cleanup(dictionary_font[fontName], charMetadata[fontName])
    '''
    return fontName 

if __name__ == "__main__":
    #filename = "9709_s14_ms_63" 
    filename = "9700_s14_ms_21"
    #filename = "9706_s14_ms_21"
    #filename = "9702_s09_qp_4"
    #filename = "9702_s12_qp_13" # -> cannot read the first question page
    #filename = "9709_s14_qp_63"

    #filename = "9709_s16_ms_23"
    #filename = "9709_s14_qp_63"
    #filename = "9702_s05_ms_2" # -> weird -> it was solved by increasing the x0 limit condition
    #filename = "9709_s10_ms_51"
    #filename = "9709_w04_ms_4" # -> failed
    #filename = "9709_w04_ms_7" # -> failed
    #filename = "9709_s05_ms_2" # -> failed

    #filename = "9231_s12_ms_22"
    #filename = "9702_s09_ms_4"
    #filename = "9702_s12_ms_22"
    #filename = "9702_s14_ms_23"
    #filename = "9709_w04_ms_2"
    #filename = "9709_s14_ms_63"
    #filename = "9702_s18_ms_22"
    #filename = "9701_s07_ms_2" 
    filename = "9608_s16_ms_11"
    filename = "9990_s18_ms_22"
    filename = "9608_s16_ms_23" 

    
    final = get_font(filename) 
    
    for each in final:
        print(each[0])


