'''
CSC450 SP2020 Group 4
Missouri State University

Displays an output based on calculated emotion

FUNCTIONAL REQUIREMENTS
FR.04
NFR.07
'''
# ********************************** imports **********************************
import cv2
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
        # self.response_filepath = ".\\response_image\\"
        self.classification = emo_num


    '''
    FR.04   EDGAR must show classification to the user
    NFR.07  EDGAR shall respond with detected emotion in less than 1 second

    function: get_image
    displays an output based on value passed into class
    calls set_emotion()
    '''
    def get_output(self):
        # set filepath to image location
        self.set_emotion()

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
            print(self.classification, " is not a valid classification.")


# ********************************** main **********************************
def main():
    print("Main function of get_response.py")

if __name__ == "__main__":
    main()
