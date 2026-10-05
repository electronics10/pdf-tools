## OCR
Use the command line tool ocrmypdf: `ocrmypdf input.pdf output.pdf`. Check the [documentation](https://github.com/ocrmypdf/OCRmyPDF) for more information.

## Split
We may want to split the pdf occasionally if the files are too large for prompting to NotebookLM or other AI context window. Using commercial is tedious and unnecessary. Open the terminal in the directory `./Fun_Projects/pdf_tools`. Check the code in `split.py`.

## Bookmark
Although it is possible to automate the process of setting up bookmarks with image recognition, I found it actually more stable to do it manually. Check up the code `./Fun_Projects/pdf_tools/bookmark.py`. You can define the bookmark structure manually. One might want to utilize commercial AI models to help with it. For example, ask ChatGPT: "Could you read the table of contents as attached and structure it like this {Paste from bookmark.py}?"