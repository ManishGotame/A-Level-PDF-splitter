# PDF-splitter

PDF-splitter is a parsing library built for extracting questions from Exam Papers. 
It works on both questions papers and marking schemes.

## Supported Exam Boards
- [Cambridge Assessment International Examinations](https://www.cambridgeinternational.org/)

## Examples

### To split a question paper

```python
from pdfsplitter.qpaper import qparser

jsonFile, textData = qparser("9709_s10_qp_11.pdf").parse()

print(jsonFile)
```

- To split a marking scheme

```python
from pdfsplitter.mscheme import mparser

jsonFile = qparser("9709_s10_ms_11.pdf", {}).parse()

print(jsonFile)
```




