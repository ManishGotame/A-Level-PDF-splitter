# PDF-splitter

[The animation of question being splitted]

PDF-splitter is a parsing library built for extracting questions from Exam Papers. 
It works on both questions papers and marking schemes.

Currently works with Python 3.7

__To report a bug__ or request a feature, please [file an issue](https://github.com/jsvine/pdfplumber/issues/new/choose). __To ask a question__ or request assistance with a specific PDF, please [use the discussions forum](https://github.com/jsvine/pdfplumber/discussions).


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




