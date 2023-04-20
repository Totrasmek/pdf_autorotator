# requires tesseract and poppler to be installed and on path
# tesseract: https://www.google.com/search?q=tesseract+ocr&ei=uJ9AZNjvCZL24-EP74SowAk&ved=0ahUKEwjYq_-osbf-AhUS-zgGHW8CCpgQ4dUDCBA&uact=5&oq=tesseract+ocr&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIOCAAQigUQsQMQgwEQkQIyCAgAEIoFEJECMggIABCKBRCRAjIICAAQigUQkQIyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQ6CggAEEcQ1gQQsAM6CggAEIoFELADEEM6DQgAEOQCENYEELADGAE6DwguEIoFEMgDELADEEMYAjoICC4QigUQkQI6CwgAEIAEELEDEIMBOgUILhCABEoECEEYAFD4AliGCWDFCmgBcAF4AIABpwGIAe0EkgEDMC40mAEAoAEByAETwAEB2gEGCAEQARgJ2gEGCAIQARgI&sclient=gws-wiz-serp
# poppler: https://github.com/oschwartz10612/poppler-windows/releases/
# Remember to pip install the below imports (PIL, pytesseract, pdf2image, PyPDF2)

from PIL import Image # image object for handing to OCR
import cv2 # image object

import pytesseract # OCR

from pdf2image import convert_from_path # converts pdf to images

from PyPDF2 import PdfReader, PdfWriter # edits pdfs

from os import remove, listdir # to remove files and get a list of all goal pdfs
from os.path import isfile,join # to get a list of all goal pdfs
import psutil # for closing image displays

import random


# converts ONLY THE FIRST PAGE Of a given pdf to an image
def pdf2im(pdf_path,out_name,pages=None):

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
# asks user to confirm rotation angle
def get_rotate_angle(pdf_path):

    image_name = 'out.png'
    pdf2im(pdf_path,image_name)
    image = cv2.imread(image_name)#Image.open(image_name)
    
    data = pytesseract.image_to_osd(image)
    
    orientation_confidence = float(find_substring(data,"Orientation confidence: ","\n"))
    rotation_angle = int(find_substring(data,"Rotate: ","\n"))
    
    cv2.imshow("Window",image)
    cv2.waitKey(0)
    #image.show()
    
    print("OCR's guessed rotation angle: " + str(rotation_angle) + " degrees clockwise\n Confidence: " + str(orientation_confidence))
    
    user_input = ""
    
    while(True):
        user_input = input("Is this rotation angle correct? y/n:  ")
        if (user_input == "y"):
            break
        elif (user_input == "n"):
            rotation_angle = int(input("Please enter an alternative rotation angle (multiple of 90deg):  "))
            while(rotation_angle%90 != 0):
                rotation_angle = input("Please enter an alternative rotation angle (multiple of 90deg):  ")
            break
    
    cv2.destroyAllWindows()

    
    print("PDF to be rotated by " + str(rotation_angle) + " degrees")
    
    remove(image_name)
    
    return rotation_angle
    

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

    print(pdf_path)
    
    angle = get_rotate_angle(pdf_path)
    rotate_pdf(pdf_path,angle)
    
    print("\n\n\n\n")


if __name__ == '__main__':
    pdf_directory = "pdfs"
    pdf_files = [file for file in listdir(pdf_directory) if isfile(join(pdf_directory, file))]
    for file in pdf_files:
        rotate_pdf("pdfs//"+file,random.randint(1,3)*90)
        orient_pdf("pdfs//"+file)