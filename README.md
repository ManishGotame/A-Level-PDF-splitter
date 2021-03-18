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

jsonFile, textData = qparser("9709_s10_qp_11.pdf").parse()

print(jsonFile)
```

### To split a marking scheme
  - This is designed to merge the JsonFile from qparser.
  - You can send an empty jsonFile to get around that.

```python
from pdfsplitter.mscheme import mparser
jsonFile = {}
jsonFile = qparser("9709_s10_ms_11.pdf", jsonFile).parse()

print(jsonFile)
```
```sh
{'text': '1', 'x0': 0.0, 'x1': 595.0, 'top': Decimal('65.932'), 'bottom': Decimal('170.733'), 'upright': True, 'direction': 1, 'fontname': 'HVQXXC+Times-Bold', 'page_number': 2, 'more': []}

{'text': '2', 'x0': 0.0, 'x1': 595.0, 'top': Decimal('175.733'), 'bottom': Decimal('257.973'), 'upright': True, 'direction': 1, 'fontname': 'HVQXXC+Times-Bold', 'page_number': 2, 'more': []}

{'text': '3', 'x0': 0.0, 'x1': 595.0, 'top': Decimal('262.973'), 'bottom': Decimal('374.733'), 'upright': True, 'direction': 1, 'fontname': 'HVQXXC+Times-Bold', 'page_number': 2, 'more': []}

{'text': '4', 'x0': 0.0, 'x1': 595.0, 'top': Decimal('379.733'), 'bottom': Decimal('563.493'), 'upright': True, 'direction': 1, 'fontname': 'HVQXXC+Times-Bold', 'page_number': 2, 'more': []}

{'text': '5', 'x0': 0.0, 'x1': 595.0, 'top': Decimal('568.493'), 'bottom': Decimal('685.772'), 'upright': True, 'direction': 1, 'fontname': 'HVQXXC+Times-Bold', 'page_number': 2, 'more': []}

{'text': '6', 'x0': 0.0, 'x1': 595.0, 'top': Decimal('690.772'), 'bottom': 837.0, 'upright': True, 'direction': 1, 'fontname': 'HVQXXC+Times-Bold', 'page_number': 2, 'more': []}

{'text': '7', 'x0': 0.0, 'x1': 595.0, 'top': Decimal('65.932'), 'bottom': Decimal('417.452'), 'upright': True, 'direction': 1, 'fontname': 'HVQXXC+Times-Bold', 'page_number': 3, 'more': []}

{'text': '8', 'x0': 0.0, 'x1': 595.0, 'top': Decimal('422.452'), 'bottom': 837.0, 'upright': True, 'direction': 1, 'fontname': 'HVQXXC+Times-Bold', 'page_number': 3, 'more': []}

{'text': '9', 'x0': 0.0, 'x1': 595.0, 'top': Decimal('65.932'), 'bottom': Decimal('229.773'), 'upright': True, 'direction': 1, 'fontname': 'HVQXXC+Times-Bold', 'page_number': 4, 'more': []}

{'text': '10', 'x0': 0.0, 'x1': 595.0, 'top': Decimal('234.773'), 'bottom': 707.0, 'upright': True, 'direction': 1, 'fontname': 'HVQXXC+Times-Bold', 'page_number': 4, 'more': []}
```


```sh
{'1': {'questions': '9709_s10_qp_11-1', 'answers': '', 'prediction': ''}, 
'2': {'questions': '9709_s10_qp_11-2', 'answers': '', 'prediction': ''}, 
'3': {'questions': '9709_s10_qp_11-3', 'answers': '', 'prediction': ''}, 
'4': {'questions': '9709_s10_qp_11-4', 'answers': '', 'prediction': ''}, 
'5': {'questions': '9709_s10_qp_11-5', 'answers': '', 'prediction': ''}, 
'6': {'questions': '9709_s10_qp_11-6', 'answers': '', 'prediction': ''}, 
'7': {'questions': '9709_s10_qp_11-7', 'answers': '', 'prediction': ''}, 
'8': {'questions': '9709_s10_qp_11-8', 'answers': '', 'prediction': ''}, 
'9': {'questions': '9709_s10_qp_11-9', 'answers': '', 'prediction': ''}, 
'10': {'questions': '9709_s10_qp_11-10', 'answers': '', 'prediction': ''}}
```




