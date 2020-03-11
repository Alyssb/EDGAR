def response(result):
    true_label = ['anger', 'disgust', 'excited', 'fear', 'frustrated',
                  'happy', 'neutral', 'other', 'sad', 'surprised', 'xxx']#
    print("The model has determined that you just spoke in the emotion of: ", true_label[result])
