'''
CSC450 SP2020 Group 4
Missouri State University

Displays an output based on calculated emotion
Able to display an image, but does not
NOTE: DISPLAYING IMAGE WILL SIGNIFICANTLY SLOW EXECUTION

FUNCTIONAL REQUIREMENTS
FR.04   EDGAR must show classification to the user
NFR.07  EDGAR shall respond with detected emotion in less than 1 second
'''
# ********************************** imports **********************************

import cv2
import tkinter
import PIL.Image, PIL.ImageTk

# ********************************** class get_response **********************************
class get_response:
    '''
    init function
    parameters:
        emo_num (integer 0-4):      classification value of emotion
    class variables:
        classification (int):       classification of emotion
    '''
    def __init__(self, emo_num):
        self.classification = emo_num


    '''
    FR.04   EDGAR must show classification to the user
    NFR.07  EDGAR shall respond with detected emotion in less than 1 second

    function: get_output
    displays an output based on value passed into class
    calls set_emotion()
    '''
    def get_output(self):
        # set filepath to image location
        self.set_emotion()
        # self.display_emotion()  # uncomment to use EDGAR with images
        print("\nTHE DETECTED EMOTION IS:\t" + self.response + "\n")


    '''
    FR.04   EDGAR must show classification to the user
    NFR.07  EDGAR shall respond with detected emotion in less than 1 second
    
    function: set_emotion
    set output to proper emotion
    class variables:
        self.response (string): name of emotion to be outputted
    '''
    # set the filename for the proper image file
    def set_emotion(self):
        if self.classification == 0:
            self.response = "ANGER"
        elif self.classification == 1:
            self.response = "FEAR"
        elif self.classification == 2:
            self.response = "HAPPY"
        elif self.classification == 3:
            self.response = "NEUTRAL"
        elif self.classification == 4:
            self.response = "SAD"
        else:
            self.response = "INVALID"
            print(self.classification, " is not a valid classification.")


    '''
    FR.04   EDGAR must show classification to the user

    function display_emotion
    BRIEFLY displays an image to represent the detected emotion
    local variables:
        window (Tk):        instance of tkinter
        cv_img (image):     image loaded using OpenCV
        height (int):       height of image to be displayed
        width (int):        width of image to be displayed
        no_channels (int):  number of channels in image to be displayed
        canvas (Canvas):    canvas to pack image into
        photo (PhotoImage): image created
    '''
    def display_emotion(self):
        window = tkinter.Tk()
        window.title("Emotion Detected")

        cv_img = cv2.cvtColor(cv2.imread("./response_image/" + self.response + ".jpeg"), cv2.COLOR_BGR2RGB)

        # get the image dimensions (OpenCV stores image data as a NumPy ndarray)
        height, width, no_channels = cv_img.shape

        # create a canvas that can fit the above image
        canvas = tkinter.Canvas(window, width = width, height = height)
        canvas.pack()

        # use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
        photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv_img))

        # add a a PhotoImage to the Canvas
        canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)

        window.update()
        window.after(3000, window.destroy())


# ********************************** main **********************************
def main():
    print("Main function of get_response.py")

if __name__ == "__main__":
    main()
