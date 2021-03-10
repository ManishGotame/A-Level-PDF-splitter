from pdfsplitter.qpaper import qparser
from pdfsplitter.mscheme import mparser
from pdfsplitter.utils.mcq import mcq 
from pdfsplitter.utils.extractor import extract

x  = qparser("questions/9701_s18_qp_23.pdf")
jsonfile, text = x.parse()
y = mparser("questions/9701_s18_ms_23.pdf", jsonfile).parse()

print(jsonfile)
print()
print(y)

# not using this for now -- PDF files have some unnecessary text to get rid of  
def getText(filename, qFilename, upperLimit, lowerLimit):
    print(filename) 
    src = fitz.open("questionsPDF/" + qFilename + "/" + filename + ".pdf")
    text = ""
    
    
    for each in src.pages(0):
        e = each.getText("words")
        i = 0 
        
        text2 = []
        for each in e:
            word = each[4]
            wordPos = (each[1] + each[3]) / 2 
            if wordPos >=upperLimit and wordPos <=lowerLimit:
                text2.append(word) 
        
        print(text2) 
        print()
        break

        for x in e:
            print(x)
            print(upperLimit, lowerLimit) 
            print()
            if i == 12: exit(0)
            else: i += 1
            #linePost = (842 - x[1]) - (x[3] - x[1]) / 2   
            linePost = 842 - x[3]
            text = x[4]
            #print(text, linePost, upperLimit, lowerLimit)  
            if linePost >= upperLimit and linePost <= lowerLimit:
                print(text) 
    text = ""
    for each in src.pages(0): text += each.getText("text")
    text = preprocess(text)
    print(text) 
    text = text[:len(text) - 5]
    ftext = []

    for each in text:
        if len(each) > 3: ftext.append(each) 
    text = ftext
    

    return " ".join(text)  

