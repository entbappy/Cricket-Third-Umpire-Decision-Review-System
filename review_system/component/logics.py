import tkinter  #For makes GUI
import cv2 
import sys
import os
import PIL.Image, PIL.ImageTk  
from functools import partial  #For give agruments into the functions
import threading #It prevents from block program
import imutils  #It resizes photos
import time
from review_system.logger.log import logging
from review_system.exception.exception_handler import AppException
from review_system.config.configuration import AppConfiguration


class ReviewSystem:
    """
    ReviewSystem is a class 
    It contains all the functionality needed to do the review 
    """

    def __init__(self, app_config = AppConfiguration()):
        """
        Initiate the ReviewSystem class
        """
        try:
            self.templates_config = app_config.get_templates_config()
            self.root_app_config = app_config.get_root_app_config()

            self.SET_WIDTH = self.root_app_config.screen_width
            self.SET_HEIGHT = self.root_app_config.screen_height
            self.stream = cv2.VideoCapture(os.path.join(self.templates_config.clips_dir, self.templates_config.clip_name))
            self.flag = True

            self.window = tkinter.Tk()
            self.window.title("Cricket Third Umpire Decision Review System")

            #To canvas welcome.png into GUI
            self.canvas  = tkinter.Canvas(self.window, width= self.SET_WIDTH , height= self.SET_HEIGHT)
            self.cv_img = cv2.cvtColor(cv2.imread(os.path.join(self.templates_config.sprites_dir,"welcome.png")), cv2.COLOR_BGR2RGB)
            self.photo = PIL.ImageTk.PhotoImage(image= PIL.Image.fromarray(self.cv_img))
            image_on_canvas = self.canvas.create_image(0,0,anchor=tkinter.NW, image= self.photo)
            self.canvas.pack()

        except Exception as e:
            raise AppException(e, sys) from e

    

    # This function for button to speed control
    def play(self,speed):
        try:
            #Play the video reverse mode
            frame1 = self.stream.get(cv2.CAP_PROP_POS_FRAMES)
            self.stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)

            grabbed,frame = self.stream.read()
            if not grabbed:
                exit()
            frame = imutils.resize(frame , width= self.SET_WIDTH , height= self.SET_HEIGHT)
            frame = PIL.ImageTk.PhotoImage(image= PIL.Image.fromarray(frame))
            self.canvas.image = frame
            self.canvas.create_image(0,0 ,image=frame ,anchor=tkinter.NW)
            
            if self.flag:
                self.canvas.create_text(170,25 , fill="red", font= "Time 27 italic bold", text="Decision Pending...")
            self.flag = not self.flag
            
        
            logging.info(f"You clicked on play. Speed is {speed}")

        except Exception as e:
            raise AppException(e, sys) from e

    
    #It will give the final decision
    def pending(self,decision):
        try:
            #1.Display decision pending image
            frame = cv2.cvtColor(cv2.imread(os.path.join(self.templates_config.sprites_dir,"pending.png")), cv2.COLOR_BGR2RGB)
            frame = imutils.resize(frame, width= self.SET_WIDTH, height= self.SET_HEIGHT)
            frame = PIL.ImageTk.PhotoImage(image= PIL.Image.fromarray(frame))  #To get image object
            self.canvas.image = frame
            self.canvas.create_image(0,0 ,image=frame ,anchor=tkinter.NW)
            #2.Wait for 2 sec
            time.sleep(2)
            
            #3.Display sponsor image
            frame = cv2.cvtColor(cv2.imread(os.path.join(self.templates_config.sprites_dir,"sponsor.png")), cv2.COLOR_BGR2RGB)
            frame = imutils.resize(frame, width= self.SET_WIDTH, height= self.SET_HEIGHT)
            frame = PIL.ImageTk.PhotoImage(image= PIL.Image.fromarray(frame))  #To get image object
            self.canvas.image = frame
            self.canvas.create_image(0,0 ,image=frame ,anchor=tkinter.NW)
            #4.Wait for 1.5 sec
            time.sleep(1.5)
            
            #5.Display out/not out
            if decision == 'out':
                decisionImg = 'out.png'
            else:
                decisionImg = 'not out.png'
            frame = cv2.cvtColor(cv2.imread(os.path.join(self.templates_config.sprites_dir,decisionImg)), cv2.COLOR_BGR2RGB)
            frame = imutils.resize(frame, width= self.SET_WIDTH, height= self.SET_HEIGHT)
            frame = PIL.ImageTk.PhotoImage(image= PIL.Image.fromarray(frame))  #To get image object
            self.canvas.image = frame
            self.canvas.create_image(0,0 ,image=frame ,anchor=tkinter.NW)

        except Exception as e:
            raise AppException(e, sys) from e
    

    #This function will return out 
    def out(self):
        try:
            thread = threading.Thread(target=self.pending, args=("out",))
            thread.daemon = 1
            thread.start()
            logging.info("Player is out")
        except Exception as e:
            raise AppException(e, sys) from e

    
    #This function will return not out 
    def not_out(self):
        thread = threading.Thread(target=self.pending, args=("not out",))
        thread.daemon = 1
        thread.start()
        logging.info("Player is not out")