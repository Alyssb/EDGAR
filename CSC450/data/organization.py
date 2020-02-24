'''
Alyssa Slayton 2020

This is going to be a bit of a bigger commitment than I originally anticipated...

Initial format of data:
Only including relavent paths
will delete anything not included in this tree to conserve space

C:\\Users\\alyss\\Documents\\EDGAR\\CSC450\\data\\big-boy\\IEMOCAP_full_release\\
    SessionX (1-5)
        dialog
            EmoEvaluation
                Categorical
                    .anvil files and .txt files for each session
                    I DELETED THE .anvil FILES BEFOREHAND
                    on cmd travel to directory and type:
                        del *.anvil
        sentences
            wav
                bunch of directories
                    each one containss a bunch of data

TREE NEEDS TO BE STRUCTURED LIKE THIS FOR THE PROGRAM TO WORK
'''
'''
Final format of data tree:

C:\\Users\\alyss\\Documents\\EDGAR\\CSC450\\data\\IEMOCAP\\
    angry
    fearful
    happy
    neutral
    sad

IEMOCAP has more than this, I only keep the ones we're using.
'''

def main():
    print("hello world.")

if __name__ == '__main__':
    main()