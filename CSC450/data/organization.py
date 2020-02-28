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

each .txt file corresponds to one subdirectory in sentences\\wav\\

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
from os import walk, remove, listdir, mkdir


class travelFolders:
    def __init__(self, root):
        self.root = root

    def getSessions(self):
        contents = listdir(self.root)
        sessions = []
        for i in contents:
            if i[0] == 'S':     # just checking if the item is a session name
                sessions.append(self.root + i)
        return(sessions)

    def getSubsessions(self, session):
        contents = listdir(session + "\\sentences\\wav")
        subsessions = []
        for i in contents:
            subsessions.append(session + "\\sentences\\wav\\" + i)
        return(subsessions)

    def getWavs(self, subsession):
        temp = listdir(subsession)
        for i in range(len(temp)):
            temp[i] = subsession + temp[i]
        return(temp)

    def getGuideFilesList(self, session):
        temp = listdir(session + "\\dialog\\EmoEvaluation\\Categorical\\")
        for i in range(len(temp)):
            temp[i] = session + "\\dialog\\EmoEvaluation\\Categorical\\" + temp[i]
        return(temp)

def makeFolders(root):
    # mkdir(root + "IEMOCAP\\")
    root = root + "IEMOCAP\\"
    emotions = ["angry", "happy", "sad", "neutral", "frustrated", "excited", "fearful", "surprised", "disgusted", "other"]
    for emotion in emotions:
        mkdir(root + emotion)

def getClass(c):
    if("Neutral" in c[1]):
        return('neutral')
    elif("Anger" in c[1]):
        return('angry')
    elif("Disgust" in c[1]):
        return('disgust')
    elif("Surprise" in c[1]):
        return("surprise")
    elif("Frustration" in c[1]):
        return("frustrated")
    elif("Happiness" in c[1]):
        return("happy")
    elif("Sadness" in c[1]):
        return("sad")
    elif("Fear" in c[1]):
        return("fear")
    elif("Excited" in c[1]):
        return("excited")
    else:
        return("other")

def classify(wav, c1, c2, c3):
    # this is going to be yucky sorry
    classes = []
    classes.append(getClass(c1))
    classes.append(getClass(c2))
    classes.append(getClass(c3))

    print(classes)

def main():
    initRoot = "C:\\Users\\alyss\\Documents\\EDGAR\\CSC450\\data\\big-boy\\IEMOCAP_full_release\\"
    finalRoot = "C:\\Users\\alyss\\Documents\\EDGAR\\CSC450\\data\\"

    '''
    RUN THIS ONCE
    THIS WILL CREATE THE FOLDERS FOR YOUR FILES.
    MAKE SURE FINALROOT IS UPDATED TO YOUR FILEPATH
    '''
    # makeFolders(finalRoot)

    finalRoot = finalRoot + "IEMOCAP\\"

    traversal = travelFolders(initRoot)
    sessions = traversal.getSessions()
    for session in sessions:
        subsessions = traversal.getSubsessions(session)
        contentFiles = traversal.getGuideFilesList(session)
        for i in range(len(subsessions)):
            wavs = traversal.getWavs(subsessions[i])
            file1 = open(contentFiles[i*3]).read().split("\n")
            file2 = open(contentFiles[i*3+1]).read().split("\n")
            file3 = open(contentFiles[i*3+2]).read().split("\n")
            for i in range(len(wavs)-1):
                classify(wavs[i], file1[i].split(' '), file2[i].split(' '), file3[i].split(' '))

            # print(len(wavs), " ", len(open(file1).read().split("\n")), " ", len(file2), " ", len(file3))
        
    wavs = traversal.getWavs(subsessions[0])

    
    print("traveling")

if __name__ == '__main__':
    main()