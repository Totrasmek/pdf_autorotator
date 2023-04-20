# requires tesseract and poppler to be installed and on path
# tesseract: https://www.google.com/search?q=tesseract+ocr&ei=uJ9AZNjvCZL24-EP74SowAk&ved=0ahUKEwjYq_-osbf-AhUS-zgGHW8CCpgQ4dUDCBA&uact=5&oq=tesseract+ocr&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIOCAAQigUQsQMQgwEQkQIyCAgAEIoFEJECMggIABCKBRCRAjIICAAQigUQkQIyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQ6CggAEEcQ1gQQsAM6CggAEIoFELADEEM6DQgAEOQCENYEELADGAE6DwguEIoFEMgDELADEEMYAjoICC4QigUQkQI6CwgAEIAEELEDEIMBOgUILhCABEoECEEYAFD4AliGCWDFCmgBcAF4AIABpwGIAe0EkgEDMC40mAEAoAEByAETwAEB2gEGCAEQARgJ2gEGCAIQARgI&sclient=gws-wiz-serp
# poppler: https://github.com/oschwartz10612/poppler-windows/releases/
# Remember to pip install the below imports (PIL, pytesseract, pdf2image, PyPDF2)

from PIL import Image # image object for handing to OCR

import pytesseract # OCR

from pdf2image import convert_from_path # converts pdf to images

from PyPDF2 import PdfReader, PdfWriter # edits pdfs

import os # to remove files


# converts ONLY THE FIRST PAGE Of a given pdf to an image
def pdf2im(pdf_path,out_name,pages=None):

    print("Converting PDF to image")

    pages = convert_from_path(pdf_path)
    pages[0].save(out_name,'PNG')


# finds a substring between two given strings
def find_substring(source_string,start_string,end_string):

    returnVal = None
    
    try:
        start_index = source_string.index(start_string)+len(start_string)
        end_index = source_string[start_index:-1].index(end_string)
        returnVal = source_string[start_index:start_index+end_index]
        
    except ValueError:
        print('Failed to identify either the start or end index, and so could not find substring')
    
    return returnVal


# uses OCR to determine the angle needed to rotate a pdf upright
# fails if the OCR's orientation confidence is less than the threshold
def get_rotate_angle(pdf_path,OCR_threshold = 1.0):

    image_name = 'out.png'
    pdf2im("WP0184A-E0119-RF-PointToPoint-(Scanned).pdf",image_name)
    image = Image.open(image_name)
    
    print("Finding necessary rotation angle with OCR")
    
    data = pytesseract.image_to_osd(image)
    
    orientation_confidence = float(find_substring(data,"Orientation confidence: ","\n"))
    rotation_angle = int(find_substring(data,"Rotate: ","\n"))
    
    print("OCR orientation confidence is " + str(orientation_confidence))
    print("Rotation angle is " + str(rotation_angle))
    
    if (orientation_confidence > OCR_threshold):
        rotate_angle = -rotation_angle
        
        print("PDF to be rotated by " + str(rotate_angle) + " degrees")
    else:
        rotate_angle = 0
        
        print("Confidence below threshold of " + str(OCR_threshold))
    
    os.remove(image_name)
    
    return rotate_angle
    

# rotates a pdf by a given angle
def rotate_pdf(pdf_path,angle):

    if (angle%90 != 0):
        print("Requested rotation angle is not a multiple of 90deg. No rotation applied to "+pdf_path)
        
    elif (angle == 0):
        print("No rotation requested")
        
    else:

        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        
        for page in reader.pages:
            page.rotate(angle)
            writer.add_page(page)

        with open(pdf_path,"wb") as pdf_out:
            writer.write(pdf_out)

# orients a pdf upright
def orient_pdf(pdf_path):

    print("Orienting pdf " + pdf_path)
    
    angle = get_rotate_angle(pdf_path)
    rotate_pdf(pdf_path,angle)

pdf_name = "WP0184_E0708-RF-Point to Point (Scanned).pdf"

rotate_pdf(pdf_name,90)
orient_pdf(pdf_name)

