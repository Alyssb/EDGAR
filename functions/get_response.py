'''
CSC450 SP 2020 Group 4
03/28/2020
Function to display response to emotion detected
'''

import tkinter
import cv2
import PIL.Image, PIL.ImageTk

class get_response:
    def __init__(self, emo_num): # delete emo_num once get_classification is implemented
        responseFilePath = "C:\\Users\\alyss\\Documents\\EDGAR\\response_image\\" # CHANGE FILE PATH
        # self.classification = get_classification() #<--- uncomment and delete next line once get_classification is implemented
        self.classification = emo_num

    # set the filename for the proper image file
    def set_emotion(self):
        if self.classification == 1:
            self.response = "happy.jpeg"
        elif self.classification == 2:
            self.response = "fear.jpeg"
        elif self.classification == 3:
            self.response = "mad.jpeg"
        elif self.classification == 4:
            self.response = "sad.jpeg"
        elif self.classification == 5:
            self.response = "neutral.jpeg"
        else:
            print(self.emo, " is not a valid classification.")

    def display_response(self):
        window = tkinter.Tk()
        window.title("Emotion Detected")

        self.set_emotion(self.classification)

        # Load an image using OpenCV
        cv_img = cv2.cvtColor(cv2.imread(responseFilePath + emotion), cv2.COLOR_BGR2RGB)

        # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
        height, width, no_channels = cv_img.shape

        # Create a canvas that can fit the above image
        canvas = tkinter.Canvas(window, width = width, height = height)
        canvas.pack()

        # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
        photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv_img))

        # Add a PhotoImage to the Canvas
        canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)

        # Run the window loop
        window.mainloop()

# This will call all 5 response. Close image to get next image to display - only needed for testing purposes
get_response(1)
get_response(2)
get_response(3)
get_response(4)
get_response(5)

def main():
    print("Main function of get_response.py")