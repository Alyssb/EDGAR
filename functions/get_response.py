'''
CSC450 SP2020 Group 4
Missouri State University
Displays an image based on calculated emotion
'''
# ********************************** imports **********************************
import tkinter
import cv2
import PIL.Image, PIL.ImageTk

# ********************************** class get_response **********************************
class get_response:
    '''
    init function
    parameters:
        emo_num (integer 0-4):      classification value of emotion
    class variables:
        response_filepath (string): filepath to images, subjective to EDGAR structure
        classification (int):       classification of emotion
    '''
    def __init__(self, emo_num):
        self.response_filepath = ".\\response_image\\"
        self.classification = emo_num


    '''
    function destroy_image
    '''
    def destroy_image(self):
        self.window.destroy()


    '''
    function: get_image
    displays an image based on value passed into class
    calls set_emotion and display_response()
    SHOULD BE SPLIT INTO TWO FUNCTIONS
    class variables:
        window (Tk):    instance of tkinter
        cv_img (image): image loaded using OpenCV
    '''
    def get_image(self):
        self.window = tkinter.Tk()
        self.window.title("Emotion Detected")

        # set filepath to image location
        self.set_emotion()

        # try to oad an image using OpenCV
        try:
            print("image name: " + self.response)
            self.cv_img = cv2.cvtColor(cv2.imread(self.response_filepath + self.response), cv2.COLOR_BGR2RGB)
            self.display_response()
        except Exception as e:
            print(e)
            print("invalid filepath")

    '''
    function: set_emotion
    set filepath to image location
    class variables:
        self.response (string): name of image file to be used
    '''
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

    '''
    function: display_response
    displays the image in a tkinter object for 1 second
    THIS NEEDS TO BE CHANGED BUT IDK HOW
    NOT FILLING IT OUT RIGHT NOW JUST TO CHANGE IT LATER
    THIS IS FRUSTRATING AND TKINTER IS BAD
    local variables:
        height
        width
        no_channels
        canvas
        photo
    '''
    # displays the image
    def display_response(self):
        # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
        height, width, no_channels = self.cv_img.shape
        # Create a canvas that can fit the above image
        canvas = tkinter.Canvas(self.window, width = width, height = height)
        canvas.pack()
        # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
        photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.cv_img))
        print(photo)
        print("test5")
        # Add a PhotoImage to the Canvas
        canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)
        # Run the window loop
        #self.window.mainloop()
        self.window.update()
        self.window.after(1000 ,self.window.destroy())


# ********************************** main **********************************
def main():
    print("Main function of get_response.py")

if __name__ == "__main__":
    main()
