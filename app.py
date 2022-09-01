import tkinter
import sys
from review_system.logger.log import logging
from functools import partial 
from review_system.exception.exception_handler import AppException
from review_system.component.logics import ReviewSystem


class ReviewEngine:
    def __init__(self):
        try:
            self.review_obj = ReviewSystem()
            logging.info("Starting Review engine")
        except Exception as e:
            raise AppException(e, sys) from e
        
    def start(self):
        try:
            #Buttons to control playback
            btn = tkinter.Button(self.review_obj.window , text="<<Previous (Fast)", width=50, command=partial(self.review_obj.play, -25))
            btn.pack()

            btn = tkinter.Button(self.review_obj.window , text="<<Previous (Slow)", width=50, command=partial(self.review_obj.play, -2))
            btn.pack()

            btn = tkinter.Button(self.review_obj.window , text="Next (Fast)>>", width=50, command=partial(self.review_obj.play, 25))
            btn.pack()

            btn = tkinter.Button(self.review_obj.window , text="Next (Slow)>>", width=50, command=partial(self.review_obj.play, 2))
            btn.pack()

            btn = tkinter.Button(self.review_obj.window , text="Give Out!", width=50, command= self.review_obj.out)
            btn.pack()

            btn = tkinter.Button(self.review_obj.window , text="Give Not Out!", width=50, command= self.review_obj.not_out)
            btn.pack()

            self.review_obj.window.mainloop()
        except Exception as e:
            raise AppException(e, sys) from e



if __name__ == "__main__":
    obj = ReviewEngine()
    obj.start()



