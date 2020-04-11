#Stephen Carr
# Function to display response to emotion detected
import tkinter
import cv2
import PIL.Image, PIL.ImageTk

# set the response that will call the correct image for the emotion displayed
def set_emotion(emo):
    if emo == 1:
        response = "happy.jpeg"
    if emo == 2:
        response = "fear.jpeg"
    if emo == 3:
        response = "mad.jpeg"
    if emo == 4:
        response = "sad.jpeg"
    if emo == 5:
        response = "neutral.jpeg"

    return response


def get_response(emo_num):  # emo_num can be removed once the get_classification function has been written

    window = tkinter.Tk()
    window.title("Emotion Detected")

    # classification = get_classification() <--- This would be how the responder gets the classification
    classification = emo_num  # set to number 1 till get_classification() created

    responseFilePath = "/Users/stephencarr/EDGAR/response_image/" #CHANGE FILE PATH

    emotion = set_emotion(classification)

    # Load an image using OpenCV
    cv_img = cv2.cvtColor(cv2.imread(responseFilePath+ emotion), cv2.COLOR_BGR2RGB)

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
