'''
CSC450 SP 2020 Group 4
03/28/2020
takes in int as input from the model,
and interprets that int into a more human readable string to see results of classification

currently called by EDGAR_demo.py


variables:
result: int parameter obtained for model output
true-label: list of strings to associate int(result) to strings for output to console

functions:
main: function to simulate to function call
response(int): prints string to console as output, no return
'''


def response(result):
    #true_label = ['anger', 'disgust', 'excited', 'fear', 'frustrated',
                  #'happy', 'neutral', 'other', 'sad', 'surprised']#, 'xxx' , 'all'
    true_label = ['anger', 'fear', 'happy', 'neutral', 'sad'] #just the 5
    
    if result < len(true_label):
        print("\nThe model has determined that you just spoke in the emotion of:", true_label[result])
    else: #error stuff
        print("\nout of bounds... somehow...")
        print("result number:", result)
        print("max int for labels:", len(true_label)-1)


def main():
    response(0) #test

if __name__ == '__main__':
    main()
