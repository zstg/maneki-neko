#!/usr/bin/env python
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore, QtGui

from PyQt5.QtWidgets import QMainWindow,  QApplication,  QDialog, QMessageBox
from time import sleep
import os, subprocess

# globals
app = QApplication(sys.argv)

programInstallQueue = []    # list of all apps selected for install
programInstallQueueLen = 0  # number of all apps selected for install, 0 is temporary value and
                            # will be updated when proceeding to install
defaultAPPSList = []

lastPage=3  # the last page of the app is the 3rd page
            # 1st-> welcome page    2nd-> overview on Stratos   3rd -> last page with buttons to install programs, distro etc
            # 4th-> program installer



WORK_DIR = os.getcwd() # gets working directory of the python script
                       # at install location value shoulda be /opt/maneki-neko
                       # to HARDCODE this , change WORK_DIR to /opt/maneki-neko

class welcomeScreen(QMainWindow):

    # CLASS variables
    defaultWEBlist     = ['librewolf']                 # list of all Web browsers marked for install by DEFAULT
    defaultMEDIAlist   = ['vlc']                       # list of all Media players marked for install by DEFAULT
    defaultOFFICElist  = ['onlyoffice']                # list of all Office Suites marked for install by DEFAULT
    defaultTXTlist     = ['stratmacs','stratvim']      # list of all Text Editors marked for install by DEFAULT
    defaultMISClist    = ['evince','gsconnect']        # list of all Miscellaneous programs marked for install by DEFAULT
    

    def __init__(self):
        global defaultAPPSList
        # init the class
        super(welcomeScreen,self).__init__()
        # load the ui file
        loadUi(WORK_DIR + "/src/ui/welcomeScreen.ui",self)
        defaultAPPSList = self.defaultWEBlist + self.defaultMEDIAlist + self.defaultOFFICElist + self.defaultTXTlist + self.defaultMISClist
        # always init window to first page
        self.windowStackedWidget.setCurrentIndex(0)
        # if AUTOSTART already enabled, then update the text of the autostartCheckBox
        self.updateAutostartCheckBoxState()
        
        # Buttons
        self.nextButton.clicked.connect(self.moveForward)   # also self.proceedToInstall
        self.backButton.clicked.connect(self.moveBackward)  
        self.distroInstallerButton.clicked.connect(self.runDistroInstallerScript)
        self.openDISCORDbutton.clicked.connect(self.openDISCORD_Link)
        self.openMASTODONbutton.clicked.connect(self.openMASTODON_Link)
        self.openMATRIXbutton.clicked.connect(self.openMATRIX_Website)
        self.autostartCheckBox.clicked.connect(self.setupAutostart)
        self.creditsButton.clicked.connect(self.openCreditsDialog)

        # package-installer page related-stuffs
        self.packageInstallerButton.clicked.connect(self.openPackageInstallerPage)
        self.MISClistWidget.itemClicked.connect(self.setMISCDescription)
        self.WEBlistWidget.itemClicked.connect(self.setWEBDescription)
        self.TXTlistWidget.itemClicked.connect(self.setTXTDescription)
        self.MEDIAlistWidget.itemClicked.connect(self.setMEDIADescription)
        self.OFFICElistWidget.itemClicked.connect(self.setOFFICEDescription)
        
        # functions to auto select default apps to be installed in UI
        self.selectDefaultApps()
        return

    def proceedToInstall(self):
        global programInstallQueue, programInstallQueueLen

        # clear list if not empty
        if programInstallQueue != []:
            programInstallQueue == []

        # update values in program install queue
        WEBprogramInstallQueue = []
        # for every item listed in the listwidget
        for i in range(0,self.WEBlistWidget.count()):
            item = self.WEBlistWidget.item(i)
            # if the current item is checked
            if item.checkState() == QtCore.Qt.Checked:
                # append the program name to the list
                WEBprogramInstallQueue.append(item.text().lower())

        MEDIAprogramInstallQueue = []
        for i in range(0,self.MEDIAlistWidget.count()):
            item = self.MEDIAlistWidget.item(i)
            # if the current item is checked
            if item.checkState() == QtCore.Qt.Checked:
                # append the program name to the list
                MEDIAprogramInstallQueue.append(item.text().lower())

        OFFICEprogramInstallQueue = []
        for i in range(0,self.OFFICElistWidget.count()):
            item = self.OFFICElistWidget.item(i)
            # if the current item is checked
            if item.checkState() == QtCore.Qt.Checked:
                # append the program name to the list
                OFFICEprogramInstallQueue.append(item.text().lower())

        TXTprogramInstallQueue = []
        for i in range(0,self.TXTlistWidget.count()):
            item = self.TXTlistWidget.item(i)
            # if the current item is checked
            if item.checkState() == QtCore.Qt.Checked:
                # append the program name to the list
                TXTprogramInstallQueue.append(item.text().lower().split()[0])
   
        MISCprogramInstallQueue = []
        for i in range(0,self.MISClistWidget.count()):
            item = self.MISClistWidget.item(i)
            # if the current item is checked
            if item.checkState() == QtCore.Qt.Checked:
                # append the program name to the list
                MISCprogramInstallQueue.append(item.text().lower().split()[0])

        # update the class variable
        programInstallQueue =[ 
            WEBprogramInstallQueue, MEDIAprogramInstallQueue, OFFICEprogramInstallQueue,    \
                    TXTprogramInstallQueue, MISCprogramInstallQueue 
        ]

      

        programInstallQueueLen = len(WEBprogramInstallQueue) + len(MEDIAprogramInstallQueue) + \
                                len(OFFICEprogramInstallQueue) + len(TXTprogramInstallQueue) + len(MISCprogramInstallQueue)

        # if programQueue is empty ie not filled
        # send popup message and exit function
        if programInstallQueueLen == 0:
            message = QMessageBox.critical(self,"Cannot Install","No programs marked for install.")
            return
        # now call the install dialog
        dialog = installDialog()
        if dialog.exec_():
            return

    def selectDefaultApps(self):

        for i in range(0,self.WEBlistWidget.count()):
            item = self.WEBlistWidget.item(i)
            # check if the current list widget item (ie package) is in the list of default packages
            # marked for install
            if item.text().lower()in self.defaultWEBlist:
                item.setCheckState(QtCore.Qt.Checked)
  
        for i in range(0,self.MEDIAlistWidget.count()):
            item = self.MEDIAlistWidget.item(i)
            # check if the current list widget item (ie package) is in the list of default packages
            # marked for install
            if item.text().lower()in self.defaultMEDIAlist:
                item.setCheckState(QtCore.Qt.Checked)
     

        for i in range(0,self.OFFICElistWidget.count()):
            item = self.OFFICElistWidget.item(i)
            # check if the current list widget item (ie package) is in the list of default packages
            # marked for install
            if item.text().lower()in self.defaultOFFICElist:
                item.setCheckState(QtCore.Qt.Checked)
  

        for i in range(0,self.TXTlistWidget.count()):
            item = self.TXTlistWidget.item(i)
            # check if the current list widget item (ie package) is in the list of default packages
            # marked for install
            if item.text().lower().split()[0] in self.defaultTXTlist:
                item.setCheckState(QtCore.Qt.Checked)


        for i in range(0,self.MISClistWidget.count()):
            item = self.MISClistWidget.item(i)
            # check if the current list widget item (ie package) is in the list of default packages
            # marked for install
            if item.text().lower().split()[0] in self.defaultMISClist:
                item.setCheckState(QtCore.Qt.Checked)
        return

    def setMISCDescription(self):
        # function that shows details of selected package on description widget of MISC category
        refDict = { "atril"     : 11,    \
                    "evince"    : 12,    \
                    "github"    : 13,    \
                    "obsidian"  : 14,    \
                    "gsconnect" : 15
                }
        # using try-except block to avoid error if user directly ticks the options without selecting the items fully
        try:
        # to determine the selected app
            selectedApp = self.MISClistWidget.currentItem().text().lower().split()[0]
        # EXPLANATION: suppose I selected "Atril PDF Document Viewer"
        # 1. self.MISClistWidget.currentItem().text() = "Atril PDF Document Viewer"
        # 2. self.MISClistWidget.currentItem().text().lower() = "atril pdf document viewer"
        # 3. self.MISClistWidget.currentItem().text().lower().split() = ["atril", "pdf","document", "viewer"]
        # 4. self.MISClistWidget.currentItem().text().lower().split()[0] = "atril"
            self.packageDetailsStackedWidget.setCurrentIndex(refDict[selectedApp])
        except AttributeError:
            pass
        return

    def setWEBDescription(self):
        # function that shows details of selected package on description widget of WEB category
        refDict = { "firefox"     : 0,    \
                    "chromium"    : 1,    \
                    "librewolf"   : 2,    \
                    "brave"       : 3
                }
        try:
        # to determine the selected app
            selectedApp = self.WEBlistWidget.currentItem().text().lower()
        # EXPLANATION: suppose I selected "Atril PDF Document Viewer"
        # 1. self.MISClistWidget.currentItem().text() = "Atril PDF Document Viewer"
        # 2. self.MISClistWidget.currentItem().text().lower() = "atril pdf document viewer"
        # 3. self.MISClistWidget.currentItem().text().lower().split() = ["atril", "pdf","document", "viewer"]
        # 4. self.MISClistWidget.currentItem().text().lower().split()[0] = "atril"
            self.packageDetailsStackedWidget.setCurrentIndex(refDict[selectedApp])
        except AttributeError:
            pass
        return

    def setTXTDescription(self):
        # function that shows details of selected package on description widget of TXT category
        refDict = { "stratmacs"   : 8,    \
                    "stratvim"    : 9,    \
                    "vscodium"    : 10
                }
        try:
        # to determine the selected app
            selectedApp = self.TXTlistWidget.currentItem().text().lower().split()[0]
        # EXPLANATION: suppose I selected "Atril PDF Document Viewer"
        # 1. self.MISClistWidget.currentItem().text() = "Atril PDF Document Viewer"
        # 2. self.MISClistWidget.currentItem().text().lower() = "atril pdf document viewer"
        # 3. self.MISClistWidget.currentItem().text().lower().split() = ["atril", "pdf","document", "viewer"]
        # 4. self.MISClistWidget.currentItem().text().lower().split()[0] = "atril"
            self.packageDetailsStackedWidget.setCurrentIndex(refDict[selectedApp])
        except AttributeError:
            pass
        return

    def setMEDIADescription(self):
        # function that shows details of selected package on description widget of TXT category
        refDict = { "vlc"   : 4,    \
                    "mpv"   : 5
                }
        try:
        # to determine the selected app
            selectedApp = self.MEDIAlistWidget.currentItem().text().lower()
        # EXPLANATION: suppose I selected "Atril PDF Document Viewer"
        # 1. self.MISClistWidget.currentItem().text() = "Atril PDF Document Viewer"
        # 2. self.MISClistWidget.currentItem().text().lower() = "atril pdf document viewer"
        # 3. self.MISClistWidget.currentItem().text().lower().split() = ["atril", "pdf","document", "viewer"]
        # 4. self.MISClistWidget.currentItem().text().lower().split()[0] = "atril"
            self.packageDetailsStackedWidget.setCurrentIndex(refDict[selectedApp])
        except AttributeError:
            pass
        return

    def setOFFICEDescription(self):
        # function that shows details of selected package on description widget of TXT category
        refDict = { "onlyoffice"    : 6,    \
                    "libreoffice"   : 7
                }
        try:
        # to determine the selected app
            selectedApp = self.OFFICElistWidget.currentItem().text().lower()
        # EXPLANATION: suppose I selected "Atril PDF Document Viewer"
        # 1. self.MISClistWidget.currentItem().text() = "Atril PDF Document Viewer"
        # 2. self.MISClistWidget.currentItem().text().lower() = "atril pdf document viewer"
        # 3. self.MISClistWidget.currentItem().text().lower().split() = ["atril", "pdf","document", "viewer"]
        # 4. self.MISClistWidget.currentItem().text().lower().split()[0] = "atril"
            self.packageDetailsStackedWidget.setCurrentIndex(refDict[selectedApp])
        except AttributeError:
            pass
        return

    def updateAutostartCheckBoxState(self):
        # purpose of this function is to update the text of 
        # autostart checkbox to Enabled if the desktop file already exists
        home = os.path.expanduser("~")
        filePath = home + "/.config/autostart/maneki_neko.desktop"
        # print("updateAutostartCheckBoxState(): file path to autostart directory:",filePath)

        if os.path.isfile(filePath):
            # the file exists so update the checkbox text
            self.autostartCheckBox.setText("Autostart Maneki Neko (Enabled)")
            self.autostartCheckBox.setChecked(True)

        return

    def disableBackAtFirstPage(self):
        currentIndex = self.windowStackedWidget.currentIndex() #current index of the window
        # disable back button if at first page
        if currentIndex == 0:
            self.backButton.setEnabled(False)
            return

    def moveForward(self):
        global lastPage
        currentIndex = self.windowStackedWidget.currentIndex() #current index of the window
        
        # if already in last page then exit
        if currentIndex+1 == lastPage:
            print("Exiting...")
            app.exec_()
            exit()
        
        # if at the 4th page ie. program installer button
        # the 'next' button gets morphed to 'install' button
        # adding the install functionality for the button at the 4th page only
        elif currentIndex+1 == 4:
            self.proceedToInstall()
            return

        # change page by one forward
        self.windowStackedWidget.setCurrentIndex(currentIndex+1)

        # now enable back button
        self.backButton.setEnabled(True)


        # morph the button to "Exit" button on last page
        currentIndex = self.windowStackedWidget.currentIndex() #updated index of the window
        if currentIndex+1 == lastPage:
            self.morphNextButton()
        return

    def moveBackward(self):
        currentIndex = self.windowStackedWidget.currentIndex()

        # go back until currentIndex is 0
        if currentIndex >= 0:
            self.windowStackedWidget.setCurrentIndex(currentIndex-1)
        
        # call func to disable back button at first page
        self.disableBackAtFirstPage()

        # to undo morph (from "Exit" to "Next")
        self.morphNextButton()

        return
    
    def morphNextButton(self):
        currentIndex = self.windowStackedWidget.currentIndex()

        # set button label to "Next" as long as it is not on last page
        # if at 1st, 2nd page, button says "Next"
        if currentIndex+1 < lastPage: 
            self.nextButton.setText("Next")
        
        # if at the Package installer page, morph button to "Install"
        elif currentIndex+1 == 4:
            self.nextButton.setText("Install")
        # if button at 3rd page, it says "exit"
        else:
            self.nextButton.setText("Exit")

    def runDistroInstallerScript(self):

        # work need to be done
        print("executing the installer script")

        # the command to execute
        # pls change this
        command = ["gnome-terminal", "--", '/usr/local/bin/StratOS-configure-distro']

        temporary = subprocess.Popen(command,stdout=subprocess.PIPE)

        # get the STDOUT
        result=temporary.communicate()

        #print(result)

        return

    def openPackageInstallerPage(self):
        # change the page
        currentIndex = self.windowStackedWidget.currentIndex()
        self.windowStackedWidget.setCurrentIndex(currentIndex+1)
        # morph Next button to install button

        self.morphNextButton()
        return

    def runThemeChangerScript(self):
        # work need to be done
        print("executing the installer script")

        # the command to execute
        # pls change this
        command = ["gnome-terminal", "--", '/usr/local/bin/StratOS-configure-theme']

        temporary = subprocess.Popen(command,stdout=subprocess.PIPE)

        # get the STDOUT
        result=temporary.communicate()

        #print(result)

        return

    def runBrowserInstallerScript(self):
        # work need to be done
        print("executing the installer script")

        # the command to execute
        # pls change this

        command = ["gnome-terminal", "--", '/usr/local/bin/StratOS-configure-browser']

        temporary = subprocess.Popen(command,stdout=subprocess.PIPE)

        # get the STDOUT
        result=temporary.communicate()

        #print(result)

        return

    def openWebsite(self):
        # command to open the URL
        command = ["xdg-open", "stratos-linux.github.io"]
        run = subprocess.Popen(command)
        return
    
    def openMASTODON_Link(self):
        # command to open the URL
        command = ["xdg-open", "https://fosstodon.org/@StratOS"]
        run = subprocess.Popen(command)

        return

    def openMATRIX_Website(self):
        # command to open the URL
        command = ["xdg-open", "https://matrix.to/#/#stratos:matrix.org"]
        run = subprocess.Popen(command)

        return
    
    def openDISCORD_Link(self):
        # command to open the URL
        command = ["xdg-open", "https://discord.gg/8sysF4ex"]
        run = subprocess.Popen(command)

        return  

    def openCreditsDialog(self):
        dialog = creditsWindow()
        if dialog.exec_():
            return

    def setupAutostart(self):
        # define home and hence the full file path for the DESKTOP FILE
        home = os.path.expanduser("~")
        #filePath = home + "/.config/autostart/maneki_neko.desktop" # full path to desktop file
        

        # create the desktop file and save it in $HOME/.config/autostart when the checkBox is checked
        if self.autostartCheckBox.isChecked():
            # returns this running script's file name
          #  thisScriptFileName = os.path.basename(__file__)

            # opening the file in write mode
            with open(filePath,"w") as f:

                fileContent=f"""
[Desktop Entry]
Type=Application
Name=StratOS Maneki-Neko
GenericName=Welcome Screen App
Comment=Welcome Screen Application for StratOS
Exec=/usr/local/bin/maneki-neko
Icon={WORK_DIR}/src/png/logo.png
Comment=StratOS welcome screen
X-GNOME-Autostart-enabled=true
Path={WORK_DIR}
Terminal=false
StartupNotify=false
                    """
                f.write(fileContent)
                # end of with block
            print("setupAutostart(): create desktop file: OK")

            #make file executable
            command = ["chmod", "+x", filePath] 
            run = subprocess.Popen(command)
            print("setupAutostart(): make desktop file executable: OK")

            print("Maneki Neko autostart Enabled")

            # update checkbox text for feedback
            self.autostartCheckBox.setText("Autostart Maneki Neko (Enabled)")

        else:
            try:
                os.remove(filePath)
                # update checkbox text for feedback
                self.autostartCheckBox.setText("Autostart Maneki Neko (Disabled)")
                print("setupAutostart(): remove: Maneki Neko autostart Disabled")


            except Exception as E:
                print("setupAutostart(): remove: desktop file was not found anyway")
                self.autostartCheckBox.setText("Autostart Maneki Neko")

        return


def main():
    global app
    mainScreen = welcomeScreen()
    print("Program launch OK")
    mainScreen.setWindowIcon(QtGui.QIcon(WORK_DIR + "/src/png/maneki_neko.png"))
    mainScreen.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting...")
    
    return



class creditsWindow(QDialog):
    def __init__(self):
        # init the class and the ui file
        super(creditsWindow,self).__init__()
        loadUi(WORK_DIR + "/src/ui/creditsDialog.ui",self)

        self.openBedrockSiteButton.clicked.connect(self.openBedrockWebsite)
        self.openGithubRepo.clicked.connect(self.openRepo)

        return
    
    def openBedrockWebsite(self):
        # the command to open the website
        command = ['xdg-open', 'https://bedrocklinux.org/']

        # run the command
        run = subprocess.Popen(command)
        return

    def openRepo(self):
        # the command to open the website
        command = ['xdg-open', 'https://github.com/stratos-linux']

        # run the command
        run = subprocess.Popen(command)
        return


class installDialog(QDialog):
   

    def __init__(self):
        super(installDialog,self).__init__()
        loadUi(WORK_DIR + "/src/ui/installDialog.ui", self)
        self.cancelButton.clicked.connect(self.reject)
        self.updateInstallQueueLabel()
        self.proceedButton.clicked.connect(self.invokeInstallScript)

    def updateInstallQueueLabel(self):
        global programInstallQueue

        # update the OTHER labels
        # if the user is going to install the defaults
        if programInstallQueue == defaultAPPSList:
            self.commentLabel.setText("These programs will be installed by default:")
            self.headingLabel.setText("You haven't selected any programs to install!")
        else:
            if programInstallQueueLen == 1:
                self.headingLabel.setText("You're about to install 1 program.")
                self.commentLabel.setText("The program you selected is:")

            else:
                self.headingLabel.setText(f"You're about to install {programInstallQueueLen} programs.")
                self.commentLabel.setText("The programs you selected are:")


        labelString = ""
        for category in programInstallQueue:
            for app in category:
                labelString += app + ", " # append the app name to empty string
        
        # remove trailing space and comma
        labelString = labelString[:-2]

        self.installQueueLabel.setText(labelString)
        return
    
    def invokeInstallScript(self):
        global programInstallQueue
        # function that calls the external shell script to begin installation
        print("Installing programs....")

        BrowserInstallQueue = programInstallQueue[0]
        PlayerInstallQueue = programInstallQueue[1]
        OfficeSuiteInstallQueue = programInstallQueue[2]
        TextEditorInstallQueue = programInstallQueue[3]
        MiscInstallQueue = programInstallQueue[4]

        print(programInstallQueue)

    
        self.accept()
        return

if __name__ == "__main__":
    main()
