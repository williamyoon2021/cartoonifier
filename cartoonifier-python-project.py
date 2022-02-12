import code
from turtle import color
import cv2 #image processing
import easygui # open filebox
import numpy as np #store image
import imageio #read image stored at particular path
import matplotlib.pyplot as plt #visualization and plotting
import os #os interaction
import tkinter as tk #create graphical user interfaces
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image

def upload():
    ImagePath=easygui.fileopenbox() #method in easyGUI that returns path of chosen file as string
    cartoonify(ImagePath)

def cartoofify(ImagePath):
    #read image
        originalmage = cv2.imread(ImagePath) #store images in form of numbers
        originalmage = cv2.cvtColor(originalmage,cv2.COLOR_BGR2RGB)

        if originalmage is None:
            print("Cannot find image. Choose appropriate file")
            sys.exit()

        ReSized1 = cv2.resize(originalmage, (960, 540))
        #plt.imshow(ReSized1, cmap='gray')

        #convert image to grayscale
        grayScaleImage = cv2.cvtColor(originalmage, cv2.COLOR_BGR2GRAY)
        #cvtColor(image,flag) transforms image into colour-spaced 'flag'
        ReSized2 = cv2.resize(grayScaleImage, (960, 540))
        #plt.imshow(ReSize2, cmap='gray') to display resultant image

        #applying median blur to smoothen an image
        smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
        ReSized3 = cv2.resize(smoothGrayScale, (960, 540))
        #plt.imshow(ReSized3, cmap='gray')

        #retreiving edges for cartoon effect using thresholding technique
        getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,9,9)

        reSized4 = cv2.resize(getEdge, (960,540))
        #plt.imshow(ReSized4, cmap='gray')

        #applying bilateral filter to remove noise & keep edge sharp
        colorImage = cv2.bilateralFilter(originalmage, 9, 300, 300)
        ReSized5 = cv2.resize(colorImage, (960, 540))
        #plt.imshow(ReSized5, cmap='gray)

        #masking edged image with "BEAUTIFY" image
        cartoonImage = cv.bitwise_and(colorImage, colorImage, mask=getEdge)
        ReSized6 = cv2.resize(cartoonImage, (960, 540))
        #plt.imshow(ReSized6, cmap='gray')

        #Plotting whole transition
        images=[ReSized1,ReSized2,ReSized3,ReSized4,ReSized5,ReSized6]
        fig, axes = plt.subplots(3,2, figsize=(8,8), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace=0.1,wspace=0.1))
        for i, ax in enumerate(axes.flat):
            ax.imshow(images[i], cmap='gray')
            #save button code
        plt.show()

        def save(ReSized6, ImagePath):
            #saving an image using imwrite()
            newName="cartoonified_Image"
            path1 = os.path.dirname(ImagePath)
            extension = os.path.splitext(ImagePath)[1]
            path = os.path.join(path1, newName+extension)
            cv2.imwrite(path, cv2.cvtColor(ReSized6, cv2.COLOR_RGB2BGR))
            I = "Image saved by name " + newName + " at " + path
            tk.messagebox.showinfo(title=None, message=I)

        top=tk.Tk()
        top.geometry('400x400')
        top.title("Cartoonify Image !")
        top.configure(background='white')
        label=Label(top,background='#CDCDCD', font=('calibri',20,'bold'))

        upload=Button(top,text="Cartoonify Image",command=upload,padx=10,pady=5)
        upload.configure(background='#354156',foreground='white', font=('calibri', 10,'bold'))
        upload.pack(size=TOP,pady=50)

        save1=Button(top,text="Save cartoon image", command=lambda:save(ImagePath,ReSized6),padx=30,pady=5)
        save1.configure(background='#364156',foreground='white',font=('calibri',10,'bold'))
        save1.pack(size=TOP,pady=50)

        top.mainloop()

