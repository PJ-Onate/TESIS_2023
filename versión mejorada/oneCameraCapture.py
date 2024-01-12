import os

os.environ["PYLON_CAMEMU"] = "3" #Se modifica una variable de entorno

from pypylon import genicam
from pypylon import pylon
import sys
import time
import cv2
import numpy as np
import tkinter as tk

class cameraCapture(tk.Frame):#clase hija de Frame
    def __init__(self):
        self.img0 = [] #img0 es una lista asociada a la clase
        self.windowName = 'title' #se define el nombre de ventana

        try:
            # Create an instant camera object with the camera device found first.
            
            self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
                       
            self.camera.Open()  #Need to open camera before can use camera.ExposureTime, se abre la cámara
            self.camera.ExposureTime.SetValue(65145)#El sensor de imagen de la camara se expone a la luz durante 5 segundos o 500 microsegundos
            self.camera.AcquisitionFrameRate.SetValue(2);
            self.camera.Width=2448 #ancho de imagen
            self.camera.Height=2048 #alto de imagen
            # Print the model name of the camera.
            print("Using device ", self.camera.GetDeviceInfo().GetModelName()) #se imrpime el nombre del disositivo
            print("Exposure time ", self.camera.ExposureTime.GetValue()) #se imprime el tiempo de xposcion del sensor de imagne

            # According to their default configuration, the cameras are
            # set up for free-running continuous acquisition.
            #Grabbing continuously (video) with minimal delay
            self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 

            # converting to opencv bgr format
            self.converter = pylon.ImageFormatConverter()
            self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed
            self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

        except genicam.GenericException as e:
            # Error handling
            print("An exception occurred.", e.GetDescription())
            exitCode = 1

    def getFrame(self):
        try:
            self.grabResult = self.camera.RetrieveResult(30000, pylon.TimeoutHandling_ThrowException)

            if self.grabResult.GrabSucceeded():
                image = self.converter.Convert(self.grabResult) # Access the openCV image data
                self.img0 = image.GetArray()

            else:
                print("Error: ", self.grabResult.ErrorCode)
    
            self.grabResult.Release()
            #time.sleep(0.01)

            return self.img0
            
        except genicam.GenericException as e:
            # Error handling
            print("An exception occurred.", e.GetDescription())
            exitCode = 1


if __name__ == "__main__":
    testWidget = cameraCapture()
    while testWidget.camera.IsGrabbing():
        #input("Press Enter to continue...")
        testWidget.getFrame()

        #If window has been closed using the X button, close program
        # getWindowProperty() returns -1 as soon as the window is closed
        if cv2.getWindowProperty(testWidget.windowName, 0) < 0:
            cv2.destroyAllWindows()
            break
        if testWidget.k == 27: #If press ESC key
            print('ESC')
            cv2.destroyAllWindows()
            break
