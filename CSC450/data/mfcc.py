'''
This is a script which 
WILL
    calculate mel frequency cepstral coefficients for a given vile using aubio
    print them out
    and probably other things as I think of them
'''
import aubio
from os import system, remove

# gets a list of filenames
# will include filenames.txt
def getFiles(root):
    system("dir /b /a-d " + root + "filenames.txt")
    return(open(root + "filenames.txt").read().split())

def main():
    root = "c:\\Users\\alyss\\Documents\\EDGAR\CSC450\\data\\smallSet"  # root for file directory

    print("running...")

if __name__ == "__main__":
    main()