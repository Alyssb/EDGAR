'''
CSC450 SP 2020 Group 4
03/28/2020
Function to display response to emotion detected
'''

import tkinter
import cv2
import PIL.Image, PIL.ImageTk

class get_response:
    # takes an integer value 1-5
    # will get input from get_classification.py once implemented
    def __init__(self, emo_num):
        self.responseFilePath = "C:\\Users\\PremiumHamsters\\Documents\\EDGAR\\response_image\\" # CHANGE FILE PATH
        self.classification = emo_num
        # self.classification = get_classification() #<--- uncomment and delete next line once get_classification is implemented

    # gets the image and then displays it. Kind of spaghetti rn
    def get_image(self):
        self.window = tkinter.Tk()
        self.window.title("Emotion Detected")

        self.set_emotion()

        # Load an image using OpenCV
        try:
            self.cv_img = cv2.cvtColor(cv2.imread(self.responseFilePath + self.response), cv2.COLOR_BGR2RGB)
            self.display_response()
        except Exception as e:
            print(e)
            print("invalid filepath")

    # set the filename for the proper image file
    def set_emotion(self):
        if self.classification == 0:
            self.response = "mad.jpeg"
        elif self.classification == 1:
            self.response = "fear.jpeg"
        elif self.classification == 2:
            self.response = "happy.jpeg"
        elif self.classification == 3:
            self.response = "neutral.jpeg"
        elif self.classification == 4:
            self.response = "sad.jpeg"
        else:
            print(self.classification, " is not a valid classification.")

    # displays the image
    def display_response(self):
        # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
        height, width, no_channels = self.cv_img.shape

        # Create a canvas that can fit the above image
        canvas = tkinter.Canvas(self.window, width = width, height = height)
        canvas.pack()

        # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
        photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.cv_img))

        # Add a PhotoImage to the Canvas
        canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)

        # Run the window loop
        #self.window.mainloop()
        self.window.update()
        self.window.after(1000 ,self.window.quit())

def main():
    print("Main function of get_response.py")

if __name__ == "__main__":
    main()
