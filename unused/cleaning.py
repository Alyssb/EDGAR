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
from os import rename, remove, listdir, mkdir


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
            temp[i] = subsession + "\\" + temp[i]
        return(temp)

    def getGuideFilesList(self, session):
        temp = listdir(session + "\\dialog\\EmoEvaluation\\Categorical\\")
        for i in range(len(temp)):
            temp[i] = session + "\\dialog\\EmoEvaluation\\Categorical\\" + temp[i]
        return(temp)

def makeFolders(root):
    mkdir(root + "IEMOCAP\\")
    root = root + "IEMOCAP\\"
    emotions = ["angry", "happy", "sad", "neutral", "frustrated", "excited", "fearful", "surprised", "disgusted", "other"]
    for emotion in emotions:
        mkdir(root + emotion)

class classify:

    def __init__(self, wav, c1, c2, c3, finalRoot):
        self.wav = wav
        self.finalRoot = finalRoot
        self.classes = []
        self.classes.append(self.getClass(c1))
        self.classes.append(self.getClass(c2))
        self.classes.append(self.getClass(c3))
        self.getMajority(self.classes)
    
    def getClass(self, c):
        if("Neutral" in c[1]):
            return('neutral')
        elif("Anger" in c[1]):
            return('angry')
        elif("Disgust" in c[1]):
            return('disgusted')
        elif("Surprise" in c[1]):
            return("surprised")
        elif("Frustration" in c[1]):
            return("frustrated")
        elif("Happiness" in c[1]):
            return("happy")
        elif("Sadness" in c[1]):
            return("sad")
        elif("Fear" in c[1]):
            return("fearful")
        elif("Excited" in c[1]):
            return("excited")
        else:
            return("other")

    def getMajority(self, classes):
        # probably a more efficient way to do this
        if(classes[0] == classes[1] == classes[2]):
            self.moveToFolder(classes[0])
        elif(classes[0] == classes[1] or classes[0] == classes[2]):
            self.moveToFolder(classes[0])
        elif(classes[1] == classes[2]):
            self.moveToFolder(classes[1])
        else:
            self.moveToFolder("other")

    def moveToFolder(self, c):
        tempwav = self.wav.split("\\")[-1]
        # once again probably a better way to do this but I don't know what it is
        if(c == 'neutral'):
            rename(self.wav, self.finalRoot + "neutral\\" + tempwav)
        elif(c == 'angry'):
            rename(self.wav, self.finalRoot + "angry\\" + tempwav)
        elif(c == 'disgusted'):
            rename(self.wav, self.finalRoot + "disgusted\\" + tempwav)
        elif(c == 'surprised'):
            rename(self.wav, self.finalRoot + "surprised\\" + tempwav)
        elif(c == 'frustrated'):
            rename(self.wav, self.finalRoot + "frustrated\\" + tempwav)
        elif(c == 'happy'):
            rename(self.wav, self.finalRoot + "happy\\" + tempwav)
        elif(c == 'sad'):
            rename(self.wav, self.finalRoot + "sad\\" + tempwav)
        elif(c == 'fearful'):
            rename(self.wav, self.finalRoot + "fearful\\" + tempwav)
        elif(c == 'excited'):
            rename(self.wav, self.finalRoot + "excited\\" + tempwav)
        elif(c == 'other'):
            rename(self.wav, self.finalRoot + "other\\" + tempwav)


def main():
    initRoot = "C:\\Users\\alyss\\Documents\\EDGAR\\CSC450\\data\\big-boy\\IEMOCAP_full_release\\"
    finalRoot = "C:\\Users\\alyss\\Documents\\EDGAR\\CSC450\\data\\"

    makeFolders(finalRoot)

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
                classify(wavs[i], file1[i].split(' '), file2[i].split(' '), file3[i].split(' '), finalRoot)

            # print(len(wavs), " ", len(open(file1).read().split("\n")), " ", len(file2), " ", len(file3))
        
    wavs = traversal.getWavs(subsessions[0])

    
if __name__ == '__main__':
    main()