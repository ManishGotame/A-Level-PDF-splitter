# PDF-splitter

[The animation of question being splitted]

PDF-splitter is a parsing library built for extracting questions from Exam Papers. 
It works on both questions papers and marking schemes.

Currently works with Python 3.6 or higher.

__To report a bug__ or request a feature, please [file an issue](https://github.com/ManishGotame/PDF-splitter/issues/new/choose).


## Supported Exam Boards
- [Cambridge Assessment International Examinations](https://www.cambridgeinternational.org/)

## 

## Examples

### To split a question paper

```python
from pdfsplitter.qpaper import qparser

paperDict, textData = qparser("9709_s10_qp_11.pdf").parse()

print(paperDict)
```

## Understanding Output

`textData` :
```sh
{'text': '1', 'x0': 0.0, 'x1': 595.0, 'top': Decimal('65.932'), 'bottom': Decimal('170.733'), 'upright': True, 'direction': 1, 'fontname': 'HVQXXC+Times-Bold', 'page_number': 2, 'more': []}

{'text': '2', 'x0': 0.0, 'x1': 595.0, 'top': Decimal('175.733'), 'bottom': Decimal('257.973'), 'upright': True, 'direction': 1, 'fontname': 'HVQXXC+Times-Bold', 'page_number': 2, 'more': []}

{'text': '3', 'x0': 0.0, 'x1': 595.0, 'top': Decimal('262.973'), 'bottom': Decimal('374.733'), 'upright': True, 'direction': 1, 'fontname': 'HVQXXC+Times-Bold', 'page_number': 2, 'more': []}
```

Properties:
| Property | Description |
|----------|-------------|
| `text` | Detected Question. |
| `x0` | Distance of left-side extremity from left side of question. |
| `top` | Distance of top of line from top of question. |
| `bottom` | Distance of bottom of the line from top of question. |
| `page_number` | Page number on which this question was found. |
| `more` | Contains the same properties for other remaining portions of the question |
 
`paperDict` :

```sh
{'1': {'questions': '9709_s10_qp_11-1', 'answers': '', 'prediction': ''}, 
'2': {'questions': '9709_s10_qp_11-2', 'answers': '', 'prediction': ''}, 
'3': {'questions': '9709_s10_qp_11-3', 'answers': '', 'prediction': ''}}
```

### To split a marking scheme
  - This was designed to use the `dict` from qparser.
  - You can send an empty `dict` to get around that.

```python
from pdfsplitter.mscheme import mparser
paperData  = qparser("9709_s10_ms_11.pdf", {}).parse()

print(paperData)
```
```sh
{'1': {'questions': '9709_s10_qp_11-1', 'answers': '9709_s10_ms_11-1', 'prediction': ''}, 
'2': {'questions': '9709_s10_qp_11-2', 'answers': '9709_s10_ms_11-2', 'prediction': ''}, 
'3': {'questions': '9709_s10_qp_11-3', 'answers': '9709_s10_ms_11-3', 'prediction': ''}}
```

```sh
{'1': {'questions': '', 'answers': '9709_s10_ms_11-1', 'prediction': ''}, 
'2': {'questions': '', 'answers': '9709_s10_ms_11-2', 'prediction': ''}, 
'3': {'questions': '', 'answers': '9709_s10_ms_11-3', 'prediction': ''}}
```








