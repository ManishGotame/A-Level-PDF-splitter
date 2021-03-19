# PDF-splitter
<p align="center">
  <img src="https://github.com/ManishGotame/ALevel-PDF-splitter/blob/main/images/anim-splitter.gif" alt="animation"/>
</p>

### A parsing library built for extracting questions from Exam Papers. 
### It works on both questions papers and marking schemes.

Currently works with Python 3.6 or higher.

__To report a bug__ or request a feature, please [file an issue](https://github.com/ManishGotame/PDF-splitter/issues/new/choose).


## Supported Exam Boards
- [Cambridge Assessment International Examinations](https://www.cambridgeinternational.org/)


## Examples

# To split a question paper 

### Sample Questions Paper :

<p align="center">
  <img src="https://github.com/ManishGotame/ALevel-PDF-splitter/blob/main/images/qimg.PNG" alt="question paper"/>
</p>

```python
from pdfsplitter.qpaper import qparser

paperData, questionsText = qparser("9709_s10_qp_11.pdf").parse()

print(paperData)
print(questionsText)
```

`paperData` :
```sh
{'text': '1', 'x0': 0.0, 'x1': 595.0, 'top': Decimal('65.932'), 'bottom': Decimal('170.733'), 'upright': True, 'direction': 1, 'fontname': 'HVQXXC+Times-Bold', 'page_number': 2, 'more': []}

{'text': '2', 'x0': 0.0, 'x1': 595.0, 'top': Decimal('175.733'), 'bottom': Decimal('257.973'), 'upright': True, 'direction': 1, 'fontname': 'HVQXXC+Times-Bold', 'page_number': 2, 'more': []}

{'text': '3', 'x0': 0.0, 'x1': 595.0, 'top': Decimal('262.973'), 'bottom': Decimal('374.733'), 'upright': True, 'direction': 1, 'fontname': 'HVQXXC+Times-Bold', 'page_number': 2, 'more': []}
```

Properties :
| Property | Description |
|----------|-------------|
| `text` | Detected Question. |
| `x0` | Distance of left-side extremity from left side of question. |
| `top` | Distance of top of line from top of question. |
| `bottom` | Distance of bottom of the line from top of question. |
| `page_number` | Page number on which this question was found. |
| `more` | Contains the same properties given above for other remaining portions of the question |

##

`questionsText` :

```sh
{
  '1': 'the acute angle x radians is such that tan x k where k is a positive constant express in terms of k i tan x ii tan x iii sin x ', 
  '2': 'find the rstterms in the expansion of x in descending powers of x ii hence the coefcient of x in the expansion of', 
  '3': 'the ninth term of an arithmetic progression is and the sum of the find the of the progression and the common difference the nth term of the progression is ii find the value of n '
}

```


##
# To split a marking scheme
  - It does not return `questionsText` like qparser.

```python
from pdfsplitter.mscheme import mparser
paperData = mparser("9709_s10_ms_11.pdf", {}).parse()

print(paperData)
```

##
# To Extract questions and answers as separate PDFs

`Note` : This is still very messy. I will improve this in the future.

Using both qparser and mparser for the example.

Arguments:
- Location of the file
- `paperData`
- empty / previous `dict` file
- filename without its extension

```python
from pdfsplitter.qpaper import qparser
from pdfsplitter.mscheme import mparser

from pdfsplittter.utils.extractor import extract

paperData, questionsText = qparser("9709_s10_qp_11.pdf").parse()
paperData = qparser("9709_s10_ms_11.pdf", {}).parse()

paperDict = extract("9709_s10_qp_11.pdf", paperData, {}, "9709_s10_qp_11")
paperDict = extract("9709_s10_ms_11.pdf", paperData, paperDict, "9709_s10_ms_11")

print(paperDict)
```

##
`paperDict` :

```sh
{'1': {'questions': '9709_s10_qp_11-1', 'answers': '9709_s10_ms_11-1', 'prediction': ''}, 
'2': {'questions': '9709_s10_qp_11-2', 'answers': '9709_s10_ms_11-2', 'prediction': ''}, 
'3': {'questions': '9709_s10_qp_11-3', 'answers': '9709_s10_ms_11-3', 'prediction': ''}}
```
`Extract Questions as Images`:
- need to clean up some code and speed it up

`Extracted Questions as PDFs` :
<p align="center">
  <img src="https://github.com/ManishGotame/ALevel-PDF-splitter/blob/main/images/qimg1.PNG" alt="qimg1"/>
</p>
<p align="center">
  <img src="https://github.com/ManishGotame/ALevel-PDF-splitter/blob/main/images/qimg2.PNG" alt="qimg2"/>
</p>
<p align="center">
  <img src="https://github.com/ManishGotame/ALevel-PDF-splitter/blob/main/images/qimg3.PNG" alt="qimg3"/>
</p>

Note: `prediction` is used to store machine learning predctions of topics which is not included in this repository.






