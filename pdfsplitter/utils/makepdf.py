import fitz # I love fitz so much  
# done!

q = [
    fitz.open("pdfs/testpdf0.pdf"), 
    fitz.open("pdfs/testpdf1.pdf"),
    fitz.open("pdfs/testpdf2.pdf"),
    fitz.open("pdfs/testpdf3.pdf"),
    fitz.open("pdfs/testpdf4.pdf"),
    fitz.open("pdfs/testpdf11.pdf"),
    fitz.open("pdfs/testpdf39.pdf"),
]

doc = fitz.open()

questionPosition = 0
maxHeight = 842.0
maxWidth = 595.0

for src in q:
    pageCnt = (src.pageCount)

    for pn in range(0, pageCnt):
        each = src.loadPage(pn)
        n = each.rect

        if (questionPosition + n[3] >= maxHeight):
            questionPosition = 0 

        if questionPosition == 0: 
            page = doc.newPage(
                -1,
                width = maxWidth,
                height = maxHeight 
            )
        
        page.showPDFpage(
            fitz.Rect(n[0], questionPosition + n[1], n[2], questionPosition + n[3] + 100),
            src,
            pn,
            clip = n
        )
        questionPosition += n[3]

doc.save("testpdf.pdf", garbage=3, deflate=True)


exit(0) 

src = fitz.open("questions/9702_s15_qp_42.pdf")
doc =  fitz.open()
pn = 7
pn -= 1

for each in src.pages(pn, pn+1):
    r = each.rect # gets the entire page rectangle 
    #n = fitz.Rect(0,20, 595, 550)
    n = fitz.Rect(0, 0, 595.22, 250)
    
    page = doc.newPage(
        -1, 
        width = n[2],
        height = r[3] 
    )

    page.showPDFpage(
            fitz.Rect(0,0, 595.22, 250),
            src,  
            pn,
            clip = n
    )
    
    n2 = fitz.Rect(0, 0, 595, 150)
    
    page.showPDFpage(
            fitz.Rect(0, 150, 595.22, 150+150+100),
            src,  
            pn,
            clip = n2
    )
    

doc.save("testpdf.pdf", garbage=3, deflate=True)
