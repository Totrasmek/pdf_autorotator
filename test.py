# requires tesseract and poppler to be installed and on path
# tesseract: https://www.google.com/search?q=tesseract+ocr&ei=uJ9AZNjvCZL24-EP74SowAk&ved=0ahUKEwjYq_-osbf-AhUS-zgGHW8CCpgQ4dUDCBA&uact=5&oq=tesseract+ocr&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIOCAAQigUQsQMQgwEQkQIyCAgAEIoFEJECMggIABCKBRCRAjIICAAQigUQkQIyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQ6CggAEEcQ1gQQsAM6CggAEIoFELADEEM6DQgAEOQCENYEELADGAE6DwguEIoFEMgDELADEEMYAjoICC4QigUQkQI6CwgAEIAEELEDEIMBOgUILhCABEoECEEYAFD4AliGCWDFCmgBcAF4AIABpwGIAe0EkgEDMC40mAEAoAEByAETwAEB2gEGCAEQARgJ2gEGCAIQARgI&sclient=gws-wiz-serp
# poppler: https://github.com/oschwartz10612/poppler-windows/releases/
# Remember to pip install the below imports (PIL, pytesseract, pdf2image, PyPDF2)

import PIL # image object for handing to OCR
import matplotlib.pyplot
import numpy

import pytesseract # OCR

import pdf2image # converts pdf to images

import PyPDF2 # edits pdfs

import os # to remove files and get a list of all goal pdfs
import random

matplotlib.pyplot.ion()
matplotlib.pyplot.figure(0,figsize=(13,8))
matplotlib.pyplot.axis('off')
matplotlib.pyplot.grid(False)

# converts ONLY THE FIRST PAGE Of a given pdf to an image
def pdf2im(pdf_path,out_name,pages=None):

    pages = pdf2image.convert_from_path(pdf_path)
    pages[0].save(out_name,'JPEG')


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

    image_name = 'out.jpg'
    pdf2im(pdf_path,image_name)
    
    image_PIL = PIL.Image.open(image_name)
    image = numpy.asarray(image_PIL)
    
    data = pytesseract.image_to_osd(image_PIL)
    
    orientation_confidence = float(find_substring(data,"Orientation confidence: ","\n"))
    rotation_angle = int(find_substring(data,"Rotate: ","\n"))
    
    
    matplotlib.pyplot.imshow(image)
    matplotlib.pyplot.show()

    print("OCR's guessed rotation angle: " + str(rotation_angle) + " degrees clockwise\nConfidence: " + str(orientation_confidence))
    
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

    print("PDF to be rotated by " + str(rotation_angle) + " degrees")
    
    return rotation_angle
    

# rotates a pdf by a given angle
def rotate_pdf(pdf_path,angle):

    if (angle%90 != 0):
        print("Requested rotation angle is not a multiple of 90deg. No rotation applied")
        
    elif (angle == 0):
        print("No rotation requested")
    
    else:
        reader = PyPDF2.PdfReader(pdf_path)
        writer = PyPDF2.PdfWriter()
        
        for page in reader.pages:
            page.rotate(angle)
            writer.add_page(page)

        with open(pdf_path,"wb") as pdf_out:
            writer.write(pdf_out)

# orients a pdf upright
def orient_pdf(pdf_path):

    print(pdf_path[6:-1])
    
    angle = get_rotate_angle(pdf_path)
    rotate_pdf(pdf_path,angle)
    
    print("\n\n")

if __name__ == '__main__':
    pdf_directory = "pdfs"
    pdf_files = [file for file in os.listdir(pdf_directory) if os.path.isfile(os.path.join(pdf_directory, file))]
    for file in pdf_files:
        orient_pdf("pdfs//"+file)
        
    matplotlib.pyplot.close()