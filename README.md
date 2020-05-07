# EDGAR
Speech Emotion Recognition has been a major area of study in computer science for many years. We propose the Emotion Detection, Gathering, And Response (EDGAR) project: a proposed system for detecting human emotion from voice data while the human is speaking. EDGAR uses a Log Mel Spectrogram in image format to represent speech data. It uses a resnet 18 neural network created in PyTorch to classify the spectrogram into one of 5 emotions (angry, fearful, happy, neutral, sad) with an accuracy around 63%. EDGAR is designed to be able to be implemented into any system, and can be customized to suit a developer's needs. EDGAR has not been tested on limited systems such as the Raspberry Pi. System must have Python support.

# Install

## Python 3 Requirements
Python version 64-bit 3.6.x (3.6.8) (https://www.python.org/ftp/python/3.6.8/python-3.6.8-amd64.exe)
(32-bit should work just fine but only a single link will be provided for the purposes of install instructions)
Click the checkbox to add Python to PATH during the installation.

## PyTorch
It is recommended but not required to make all installations within a Virtual Machine to avoid conflicts with previously installed Python libraries (detailed instructions to setting up a Virtual Machine in Conda can be found at: https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/).

PyTorch version 1.4 or 1.5 
Project started with 1.4 as most recent release, 1.5 came out April 21, 2020 and while a few cases were added to make sure 1.5 would function, the code has been tested and measured using 1.4 and the model was created on version 1.4

CUDA functionality is optional in use and in install, and considering the various available CUDA versions available, including install instructions for every possibility for EDGAR is unrealistic; as such refer to "QUICK START LOCALLY" on https://pytorch.org/ in order to customize an install command specific to OS, Package(recommended: Pip or Conda), Language(Python), CUDA version (your version or choose "none" for a CPU-only PyTorch). If CUDA version is selected on a system that does not have a GPU with CUDA support, PyTorch will simply install the CPU version
![PyTorch install command generator](https://i.imgur.com/ax0Hsf5.png)
One example command for a 1.5, windows, pip, python, cpu-only install would be: 
`pip install torch==1.5.0+cpu torchvision==0.6.0+cpu -f https://download.pytorch.org/whl/torch_stable.html`

If using CUDA or wishing to use CUDA, please follow NVIDIA's CUDA install instructions (windows: https://docs.nvidia.com/cuda/cuda-installation-guide-microsoft-windows/index.html)

CPU-only should be more than enough to run the main functionalities of EDGAR, but CUDA is recommended if creating a new model as there are multiple hours difference in run time.

## Dependencies
Latest release should work for most of the following, but the version used during EDGAR development is provided. If Conda was used to install PyTorch, Conda should be continued to be used to install the following, if Pip was used to install PyTorch then continue using Pip in the command line to install the following:

If the system has python 2 or multiple python 3 installations "pip3" may need to be used rather than "pip"
- `pip install numpy`  (1.18.4) //already installed by PyTorch
- `pip install Pillow`		(7.1.2) //already installed by PyTorch
- `pip install opencv-python` 	(4.2.0.34)
- `pip install keyboard` 		(0.13.5)
- `pip install librosa`		(0.7.2)
- `pip install SpeechRecognition`	(3.8.1)
- `pip install matplotlib`		(3.2.1)
- `pip install PyAudio`		(0.2.11)
- `pip install pydub`		(0.23.1)
- `pip install numba==0.48.0`	(0.48.0)

As of writing these instructions the "numba" package in the pip system has had a bad version release, if any errors are involved sourced from the numba module please either force downgrade numba by running the command `pip install numba==0.48.0`, or install the most recent Microsoft Visual C++ Redistributable for Visual Studio 2015, 2017 and 2019 from  https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads 

(As of 9:30 p.m. 5/6/2020 this bug with numba is known to the developers and 6 hours ago a beta release for 0.49.1 has just been uploaded and can be installed via `pip install numba==0.49.1rc1` https://github.com/numba/numba/issues/5600#issuecomment-624875012) 

## EDGAR Download/Install
Once the previous dependencies have been installed, EDGAR itself can be downloaded from its GitHub page at https://github.com/Alyssb/EDGAR
You have a couple of options for downloading EDGAR, you can either use git via the command line or a git GUI such as [SourceTree](https://www.sourcetreeapp.com/), with either option you can download via HTTPS(recommended) via https://github.com/Alyssb/EDGAR.git or SSH via [git@github.com:Alyssb/EDGAR.git](git@github.com:Alyssb/EDGAR.git)

Or if you don't have a preferred way of cloning repositories setup, you can instead download the project directly by going to https://github.com/Alyssb/EDGAR/archive/master.zip and unzipping the folder (We recommend [7-Zip](https://www.7-zip.org/download.html) but any archiving/zip software should work) to whatever directory you so desire but we recommend making a new folder for EDGAR exclusively to avoid file overriding and ease of use.

# Run
To run the speech classification system component of EDGAR, or what we like to call "Main EDGAR", open the command line/prompt (there are many ways to do this on any given operating system, for windows see here: https://www.lifewire.com/how-to-open-command-prompt-2618089) and change directory to the upper folder of where you placed the EDGAR files, for example if you named the folder "EDGAR-master" your change directory command (on windows) should look similar to this: `cd C:\Users\<username>\documents\EDGAR-master` if you were to search the available folders from this directory you should be able to see the functions folder, but not be inside of it. 
Once the directory has been change run the command (for Windows) `functions\EDGAR.py` to begin the main component of EDGAR. The command prompt and the commands just described should look somewhat like this: 
![run EDGAR component example](https://i.imgur.com/5aNcJls.png)

To create a new model file run the command `dev_tools\functions\pytorchModel.py` from the same directory from the previous step. (highly recommending having CUDA installed, and a CUDA enabled PyTorch, or editing the file to reduce the epoch number to 1 if staying on cpu, as otherwise generating a new model file will take hours) 
You will need an unzipped "mine" folder in the base directory of EDGAR(You can create one using a copy of the IEMOCAP database, running read_sessions.py(also in dev_tools/functions), and running pytorch_format on the generated files from read_Sessions.py(also in dev_tools/functions). A blank file structure needed for the 'mine' folder is provided in dev_tools, first run read_session to generate the list of mel spectrogram numpy files and list of labels while having an unzipped IEMOCAP database folder in the base EDGAR directory, then run pytorch_format while having the 'mine' folder structure in base directory, both steps will take a fair amount of time to complete as thousands of files are being generated and shuffled around. 
Once the numpy files are arranged within the 'mine' folder after pytorch_format, you can then run pytorchModel and generate your own model, it is highly recommended to look inside the pytorchModel file and change desired settings around before running it, including changing the name of the output model file as to not overwrite the provided model.

# The Team and Contact
- Stephen Carr carr021@live.missouristate.edu
- Melanie Jelinek jelinek076@live.missouristate.edu
- Alyssa Slayton alyssaslayton@missouristate.edu
- Cory Jackson cory42@live.missouristate.edu
- Zachary Roy zachary151@missouristate.edu

# License
EDGAR is a MIT licensed work, as per the LICENSE.txt file.
Information about licenses for third-party dependencies can be found inside the third-party-licenses folder.
