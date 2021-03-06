import fitz 
import os

# TODO:

'''
    looking at the values from pdfsplit
    'x0': 0.0, 'x1': 595.22, 'top': Decimal('64.487'), 'bottom': 842.0

    a - x0
    b - top 
    c - x1  
    d - bottom
'''

# flat pages checking should only be done when a marking scheme is fed
def createPDF(eachq, doc, src, paperType):
    pn = int(eachq["page_number"]) - 1
    
    for each in src.pages(pn, pn+1):
        #if eachq["bottom"] > each.rect[3]: each["bottom"] = each.rect[3]
        #print(each.getText("text"))

        n = fitz.Rect(eachq["x0"], eachq["top"], eachq["x1"], eachq["bottom"])
        flatPage = 0 
        # this is for the marking scheme with width > height
        if (int(eachq["x1"]) > 595.0 and paperType == "ms"):
            flatPage = 1
            each.setRotation(-360)
            n = fitz.Rect(eachq["top"], eachq["x0"], eachq["bottom"], eachq["x1"])
        
        page = doc.newPage(-1, width = n[2], height = n[3] - n[1] + 23)
        page.showPDFpage(page.rect, src, pn, clip = n)

        if flatPage == 1:
            page = page.setRotation(90)


def extract(qfileLoc, paperData, pdfData, fdir):
    '''
        paper title - qfile-qno
        should return a json file? 
    '''
    qfileLoc = qfileLoc.split(".")[0]

    try: qfilename = qfileLoc.split("/")[1]
    except: qfilename = qfileLoc 
    
    paperType = qfilename.split("_")[2]

    #src = fitz.open("questions/" + qfilename+ ".pdf")
    src = fitz.open(qfileLoc + ".pdf") 
    isEmpty = False

    if pdfData == {}:
        print("question paper was not fed before")
        isEmpty = True

    for eachq in paperData:
        print(eachq["text"])
        doc = fitz.open() # empty output PDF
        title = str(qfilename) + "-" + str(eachq["text"])

        eachq["top"] -= 15
        eachq["bottom"] += 3
        if eachq["top"] < 0: eachq["top"] = 0
         
        createPDF(eachq, doc, src, paperType)

        if eachq["more"] != []:
            for mq in eachq["more"]:
                mq["top"] -= 10 
                if mq["top"] < 0: mq["top"] = 0
                createPDF(mq, doc, src, paperType)

        doc.save("questionsPDF/"+ str(fdir) + "/" + title + ".pdf", garbage=3, deflate=True)

        if isEmpty == True:
            pdfData[str(eachq["text"])] = {
                    'questions' : title,  
                    'answers' : "",
                    'prediction' : ""
            }
        else:
            pdfData[str(eachq["text"])]["answers"] = title

    return pdfData 

if __name__ == "__main__": 
    from pdfsplit_v3_1 import qparser
    from markingscheme_v2_1 import mparser 
    
    filename = "9702_s15_ms_42"
    filename = "9702_s15_qp_42"
    filename = "9702_s12_qp_13"
    filename = "9701_s16_ms_41"
    #filename = "9794_s16_qp_01"
    filename = "9702_s16_ms_42"
    filename = "9702_w19_ms_11"
    filename = "9608_s19_ms_12"
    filename = "9702_m17_qp_12"
    filename = "9990_s18_ms_22"
    filename = "9702_s05_qp_4" 

    # did not know markingscheme parser also works well on question papers

    allQuestions = os.listdir("questionsPDF/")
    if filename not in allQuestions: os.mkdir("questionsPDF/" + filename)


    questions , text= qparser(filename).parse()
    of = extract(filename, questions, {}, filename)
     
    # questions = mparser("9709_s19_ms_22", {}).parse()
    # of = extract("9709_s19_ms_22", questions, of)

    for each in of:
        print(each)
        print()
        print(of[each])



