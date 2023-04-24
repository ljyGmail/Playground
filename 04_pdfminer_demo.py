# from pdfminer.high_level import extract_text

# text = extract_text('sample.pdf')
# print(repr(text))

# from io import StringIO
# from pdfminer.high_level import extract_text_to_fp
# output_string = StringIO()
# with open('sample.pdf', 'rb') as fin:
#     extract_text_to_fp(fin, output_string)

# print(output_string.getvalue().strip())

# from io import StringIO
# from pdfminer.high_level import extract_text_to_fp
# from pdfminer.layout import LAParams
# output_string = StringIO()
# with open('sample.pdf', 'rb') as fin:
#     extract_text_to_fp(fin, output_string, laparams=LAParams(),
#                        output_type='html', codec=None)

# print(output_string.getvalue().strip())

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer
import os
import pdf2image
import numpy as np
import PIL
from PIL import Image
import io
from pathlib import Path  # it's just my favorite way to handle files

pdf_path = r"/home/ljy/Desktop/Workspace/PythonWorkspace/Playground/sample.pdf"


# PART 1: GET LTBOXES COORDINATES IN THE IMAGE ----------------------
# Open a PDF file.
fp = open(pdf_path, 'rb')

# Create a PDF parser object associated with the file object.
parser = PDFParser(fp)

# Create a PDF document object that stores the document structure.
# Password for initialization as 2nd parameter
document = PDFDocument(parser)

# Check if the document allows text extraction. If not, abort.
if not document.is_extractable:
    raise PDFTextExtractionNotAllowed

# Create a PDF resource manager object that stores shared resources.
rsrcmgr = PDFResourceManager()

# Create a PDF device object.
device = PDFDevice(rsrcmgr)

# BEGIN LAYOUT ANALYSIS
# Set parameters for analysis.
laparams = LAParams()

# Create a PDF page aggregator object.
device = PDFPageAggregator(rsrcmgr, laparams=laparams)

# Create a PDF interpreter object.
interpreter = PDFPageInterpreter(rsrcmgr, device)


# here is where i stored the data
boxes_data = []
page_sizes = []


def parse_obj(lt_objs, verbose=0):
    # loop over the object list
    for obj in lt_objs:
        # if it's a textbox, print text and location
        if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
            if verbose > 0:
                print("%6d, %6d, %s" %
                      (obj.bbox[0], obj.bbox[1], obj.get_text()))
            data_dict = {
                "startX": round(obj.bbox[0]), "startY": round(obj.bbox[1]),
                "endX": round(obj.bbox[2]), "endY": round(obj.bbox[3]),
                "text": obj.get_text()}
            boxes_data.append(data_dict)
        # if it's a container, recurse
        elif isinstance(obj, pdfminer.layout.LTFigure):
            parse_obj(obj._objs)


# loop over all pages in the document
for page in PDFPage.create_pages(document):
    # read the page into a layout object
    interpreter.process_page(page)
    layout = device.get_result()
    # extract text from this object
    parse_obj(layout._objs)
    mediabox = page.mediabox
    mediabox_data = {"height": mediabox[-1], "width": mediabox[-2]}
    page_sizes.append(mediabox_data)

# PART 2: NOW GET PAGE TO IMAGE -------------------------------------
firstpage_size = page_sizes[0]
firstpage_image = pdf2image.convert_from_path(
    pdf_path)[0]  # without 'size=...'
# show first page with the right size (at least the one that pdfminer says)
# firstpage_image.show()
firstpage_image.save("firstpage.png")

# the magic numbers
dpi = 200/72
vertical_shift = 5  # I don't know, but it's need to shift a bit
page_height = int(firstpage_size["height"] * dpi)



with open('result.txt', 'w') as fp:
    fp.write(f'len(boxes_data): {len(boxes_data)}')
    fp.write(f'boxes_data: {boxes_data}\n\n\n')

    # loop through boxes (we'll process only first page for now)
    for i, _ in enumerate(boxes_data):

        # first box data
        startX, startY, endX, endY, text = boxes_data[i].values()

        # correction PDF --> PIL
        startY = page_height - int(startY * dpi) - vertical_shift
        endY = page_height - int(endY * dpi) - vertical_shift
        startX = int(startX * dpi)
        endX = int(endX * dpi)
        startY, endY = endY, startY

        # turn image to array
        image_array = np.array(firstpage_image)
        # get cropped box
        box = image_array[startY:endY, startX:endX, :]
        convert2pil_image = PIL.Image.fromarray(box)
        # show cropped box image
        # convert2pil_image.show()
        png = "crop_" + str(i) + ".png"
        convert2pil_image.save(png)
        # print this does not match with the text, means there's an error
        print(startX, startY, endX, endY, text)
        fp.write(f'==>{startX}, {startY}, {endX}, {endY}: {text}')