# Import libraries 
from PIL import Image
import test_venv
import pytesseract
import pdfplumber
from pdf2image import convert_from_path
import os

test_venv.is_venv()

# Path of the pdf
PDF_file = "sample_1.pdf"
dirName = "sample_1"
pytesseract.pytesseract.tesseract_cmd = 'C:/Users/Ginny Sun/AppData/Local/Tesseract-OCR/tesseract.exe'

if not os.path.exists(dirName):
    os.mkdir(dirName)

''' 
Part #1 : Converting PDF to images and text
'''
if not os.path.exists(dirName + "/jpg"):
    os.mkdir(dirName + "/jpg")
if not os.path.exists(dirName + "/text"):
    os.mkdir(dirName + "/text")

# Store all the pages of the PDF in a variable
# For image extraction
pages = convert_from_path(PDF_file, 500)
# For text extraction
pdf = pdfplumber.open(PDF_file)
text_pages = pdf.pages

# Counter to store images of each page of PDF to image
image_counter = 1

# Iterate through all the pages stored above
for page in pages:
    # Declaring filename for each page of PDF as JPG
    # For each page, filename will be:
    # PDF page 1 -> page_1.jpg
    # PDF page 2 -> page_2.jpg
    # ....
    # PDF page n -> page_n.jpg
    if not os.path.isfile(dirName + "/jpg/page_" + str(image_counter) + ".jpg"):
        filename = dirName + "/jpg/page_" + str(image_counter) + ".jpg"
        # Save the image of the page in system
        page.save(filename, 'JPEG')

    if not os.path.isfile(dirName + "/text/page_" + str(image_counter) + ".txt"):
        filename = dirName + "/text/page_" + str(image_counter) + ".txt"
        # Extract text from page
        text = text_pages[image_counter - 1].extract_text()
        # Save the image of the page in system
        f = open(filename, "a")
        if text is None:
            text = ""
        f.write(text)
        f.close()

    # Increment the counter to update filename
    image_counter = image_counter + 1
pdf.close()

''' 
Part #2 - Recognizing text from the images using OCR 
'''

if not os.path.exists(dirName + "/tesseract"):
    os.mkdir(dirName + "/tesseract")

# Iterate from 1 to total number of pages 
for i in range(1, image_counter):
    # Set filename to recognize text from
    # Again, these files will be:
    # page_1.jpg
    # page_2.jpg
    # ....
    # page_n.jpg
    filename = dirName + "/jpg/page_" + str(i) + ".jpg"

    out_file = dirName + "/tesseract/page_" + str(i) + ".txt"
    # Recognize the text as string in image using pytesserct
    # language support via https://github.com/tesseract-ocr/tessdata
    text = str(pytesseract.image_to_string(Image.open(filename), lang='por'))
    # Save the image of the page in system
    f = open(out_file, "a")
    if text is None:
        text = ""

    # The recognized text is stored in variable text
    # Any string processing may be applied on text
    # Here, basic formatting has been done:
    # In many PDFs, at line ending, if a word can't
    # be written fully, a 'hyphen' is added.
    # The rest of the word is written in the next line
    # Eg: This is a sample text this word here GeeksF-
    # orGeeks is half on first line, remaining on next.
    # To remove this, we replace every '-\n' to ''.
    text = text.replace('-\n', '')
    f.write(text)
    f.close()


