import numpy as np
from tensorflow_core.python import keras
from trainModel import trainModel
from get_melspectrogram import melSpectrogram


def runModel():
#Get input file
#********************** Add input wav file here *******************************
    source_file = "ALL/Sadness/DC_sa07.wav"

#Get numpy metrics for input file
    mSpec = melSpectrogram(source_file)
    source_file_metrics = mSpec.get_MelSpectrogram()

#Convert numpy metrics to format needed for use with model
    reformatted_metrics = (np.expand_dims(source_file_metrics, 0))

#Load model saved from trainModel method
    input_model = keras.models.load_model('saved_model/my_model')

#Convert model to a probablility based one
    probability_model = keras.Sequential([input_model,
                                             keras.layers.Softmax()])

#Get prediction from model for input file
    predictions_single = probability_model.predict(reformatted_metrics)

#print predicted class
    print(predictions_single)
    maxpos = np.argmax(predictions_single[0])
    print(maxpos)
    print(true_label[maxpos])


true_label = ['anger', 'disgust', 'excited', 'fear', 'frustrated',
                  'happy', 'neutral', 'other', 'sad', 'surprised', 'xxx']




# ***************************** main *****************************
def main():
    runModel()

if __name__ == "__main__":
    main()
