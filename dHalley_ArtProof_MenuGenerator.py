
#https://stackoverflow.com/questions/8651742/dynamically-adding-and-removing-widgets-in-pyqt

import os, sys, shutil
import Tkinter
import tkFileDialog
from functools import partial
import collections

from PyQt4 import QtGui as qg
from PyQt4 import QtCore as qc

#list of scripts
listOfScripts = []
dictOfMenuScripts = collections.OrderedDict()

class Main(qg.QMainWindow):
    def __init__(self, parent = None):
        super(Main, self).__init__(parent)
        self.initUI()

    def initUI(self):

        self.setWindowTitle("Script Transfer and Maya Menu Generator")

        """
        
        PALETTE DECLARATIONS

        """

        #widget palette
        mainWindow_Palette = qg.QPalette()
        mainWindowColor = qg.QColor(75, 75, 75)
        mainWindow_Palette.setColor(qg.QPalette.Background, mainWindowColor)
        self.setPalette(mainWindow_Palette)

        self.scrollWidgetColor = (43, 43, 43)
        
        self.fontColor = (200, 200, 200)
        self.buttonColor = (95, 95, 95)
        self.buttonPressedColor = (82,133,166)

        buttonFont = qg.QFont()
        buttonFont.setPointSize(12)
        buttonFont.setBold(True)

        labelFont = qg.QFont()
        labelFont.setPointSize(10)

        #directory path
        self.directoryPath = ''
        

        """
        
        MENU BUTTONS DECLARATIONS

        """
        topButton_Seperator = qg.QFrame()
        topButton_Seperator.setFrameShape(qg.QFrame.VLine)
        topButton_Seperator.setFrameShadow(qg.QFrame.Sunken)

        buttonMenu_layout = qg.QHBoxLayout()
        self.scriptTransfer_btn = qg.QPushButton("Transfer Scripts To Maya")
        self.scriptTransferHelp_btn = qg.QPushButton("?")

        self.mayaMenuGen_btn = qg.QPushButton("Make Maya Menu")
        self.mayaMenuGenHelp_btn = qg.QPushButton("?")

        self.scriptTransfer_btn.setFont(buttonFont)
        self.scriptTransferHelp_btn.setFont(buttonFont)
         
        self.mayaMenuGen_btn.setFont(buttonFont)
        self.mayaMenuGenHelp_btn.setFont(buttonFont)

        self.mayaMenuGen_btn.setStyleSheet("QPushButton { background-color: rgb%s; color: rgb%s; border: none;} QPushButton:pressed {background-color: rgb%s; color: rgb%s;} QPushButton:hover {background-color: rgb%s; color: rgb%s;}" % (self.buttonColor, self.fontColor, self.buttonPressedColor, self.fontColor, self.buttonPressedColor, self.fontColor ))
        
        self.scriptTransfer_btn.setStyleSheet("QPushButton { background-color: rgb%s; color: rgb%s; border: none;}" % (self.buttonPressedColor, self.fontColor, ))
        self.scriptTransferHelp_btn.setStyleSheet("QPushButton { background-color: rgb%s; color: rgb%s; border: none;}" % (self.buttonColor, self.fontColor, ))
        
        self.mayaMenuGen_btn.setStyleSheet("QPushButton { background-color: rgb%s; color: rgb%s; border: none;}" % (self.scrollWidgetColor, self.fontColor, ))
        self.mayaMenuGenHelp_btn.setStyleSheet("QPushButton { background-color: rgb%s; color: rgb%s; border: none;}" % (self.scrollWidgetColor, self.fontColor, ))
   

        buttonMenu_layout.addWidget(self.scriptTransfer_btn)
        buttonMenu_layout.addWidget(self.scriptTransferHelp_btn)
        
        buttonMenu_layout.addWidget(topButton_Seperator)
        buttonMenu_layout.addWidget(self.mayaMenuGen_btn)
        buttonMenu_layout.addWidget(self.mayaMenuGenHelp_btn)


        self.stacked_layout = qg.QStackedLayout()

        """

        COMBOBOX FOR MAYA VERS DECLARATION


        """

        #comboBox to serve as drop down of the type of maya Version"
        self.mayaVer_comboBox = qg.QComboBox()
        self.mayaVer_comboBox.setEditable(True)
        self.mayaVer_comboBox.setStyleSheet("QComboBox { background-color: rgb%s; color: rgb%s;}" % (self.buttonColor, self.fontColor,))
               
        #inserts dummy at index 0
        self.mayaVer_comboBox.addItem(" ")


        #comboBox to serve as drop down of the type of maya Version"
        self.mayaVer_comboBox2 = qg.QComboBox()
        self.mayaVer_comboBox2.setEditable(True)
        self.mayaVer_comboBox2.setStyleSheet("QComboBox { background-color: rgb%s; color: rgb%s;}" % (self.buttonColor, self.fontColor,))
               
        #inserts dummy at index 0
        self.mayaVer_comboBox2.addItem(" ")
        self.mayaVer_comboBox2.currentIndexChanged.connect(lambda: self.resetMenuScriptList())
        self.mayaVer_comboBox2.currentIndexChanged.connect(lambda: self.loadScriptsinMaya())
        
        """

        DECLARATIONS FOR SCRIPT TRANSFER UI


        """
        
        
        scriptTrans_widget = qg.QWidget()
        scriptTrans_widget.setLayout(qg.QVBoxLayout())  


        scriptTrans_Seperator = qg.QFrame()
        scriptTrans_Seperator.setFrameShape(qg.QFrame.HLine)
        scriptTrans_Seperator.setFrameShadow(qg.QFrame.Sunken)

        #button to call load directory function
        self.findDir_btn = qg.QPushButton('Select Source Directory')
        self.findDir_btn.setFont(buttonFont)
        #self.findDir_btn.setFlat(True)
        self.findDir_btn.setStyleSheet("QPushButton { background-color: rgb%s; color: rgb%s; border: none;} QPushButton:pressed {background-color: rgb%s; color: rgb%s;} QPushButton:hover {background-color: rgb%s; color: rgb%s;}" % (self.buttonColor, self.fontColor, self.buttonPressedColor, self.fontColor, self.buttonPressedColor, self.fontColor ))
        self.findDir_btn.clicked.connect(lambda: self.findDir())

        #button to call load directory function
        self.cancelDir_btn = qg.QPushButton('X')
        self.cancelDir_btn.setFont(buttonFont)
        self.cancelDir_btn.setDisabled(True)
        #self.findDir_btn.setFlat(True)
        self.cancelDir_btn.setStyleSheet("QPushButton { background-color: rgb%s; color: rgb%s; border: none;}" % (self.scrollWidgetColor, self.fontColor, ))
        self.cancelDir_btn.clicked.connect(lambda: self.resetScriptList())
        
        #button to transfer scripts but is currently set to print name of scripts
        self.transfer_btn = qg.QPushButton("Transfer Scripts")
        self.transfer_btn.setFont(buttonFont)
        self.transfer_btn.setDisabled(True)

        self.transfer_btn.setDisabled(True)
        self.transfer_btn.setStyleSheet("QPushButton { background-color: rgb%s; color: rgb%s; border: none;}" % (self.scrollWidgetColor, self.fontColor, ))
        

        #self.transfer_btn.setFlat(True)
        #self.transfer_btn.setStyleSheet("QPushButton { background-color: rgb%s; color: rgb%s; border: none;} QPushButton:pressed {background-color: rgb%s; color: rgb%s;} QPushButton:hover {background-color: rgb%s; color: rgb%s;}" % (self.buttonColor, self.fontColor, self.buttonPressedColor, self.fontColor, self.buttonPressedColor, self.fontColor ))
        #self.transfer_btn.setEnabled(False)

        # main button
        #self.addButton = qg.QPushButton('Load Scripts')

        #label to show chosen directory
        self.directory_lbl = qg.QLabel(None)
        self.directory_lbl.setAlignment(qc.Qt.AlignCenter)
        self.directory_lbl.setFont(labelFont)
        directory_lbl_Palette = self.directory_lbl.palette()        
        directory_lbl_Palette.setColor(self.directory_lbl.foregroundRole(), qg.QColor.fromRgb(self.fontColor[0], self.fontColor[1], self.fontColor[2]))
        self.directory_lbl.setPalette(directory_lbl_Palette)


        # scroll area widget contents - layout
        #self.scriptList_scrollLayout = qg.QFormLayout()
        self.scriptList_scrollLayout = qg.QFormLayout()

        # scroll area widget contents
        self.scriptList_scrollWidget = qg.QWidget()
        self.scriptList_scrollWidget.setLayout(self.scriptList_scrollLayout)

        # scroll area
        self.scriptList_scrollArea = qg.QScrollArea()
        self.scriptList_scrollArea.setWidgetResizable(True)
        self.scriptList_scrollArea.setObjectName("Scripts")
        self.scriptList_scrollArea.setWidget(self.scriptList_scrollWidget)

        scriptList_Palette = self.scriptList_scrollWidget.palette()        
        scriptList_Palette.setColor(self.scriptList_scrollWidget.backgroundRole(), qg.QColor.fromRgb(self.scrollWidgetColor[0], self.scrollWidgetColor[1], self.scrollWidgetColor[2]))
        scriptList_Palette.setColor(self.scriptList_scrollWidget.foregroundRole(), qg.QColor.fromRgb(self.fontColor[0], self.fontColor[1], self.fontColor[2]))
        self.scriptList_scrollWidget.setPalette(scriptList_Palette)
         
        # main layout
        #self.scriptTrans_widget = qg.QVBoxLayout()

        self.dirButtonLayout = qg.QHBoxLayout()
        self.dirButtonLayout.addWidget(self.findDir_btn)
        self.dirButtonLayout.addWidget(self.cancelDir_btn)

        self.dirLayout = qg.QVBoxLayout()

        # add all main to the main vLayout
        #self.scriptTrans_widget.addWidget(self.addButton)
        self.dirLayout.addLayout(self.dirButtonLayout)
        self.dirLayout.addWidget(self.directory_lbl)
        
        self.scriptsToTransfer_lbl = qg.QLabel(None)
        self.scriptsToTransfer_lbl.setAlignment(qc.Qt.AlignCenter)
        self.scriptsToTransfer_lbl.setFont(labelFont)

        scriptsToTransfer_lbl_Palette = self.scriptsToTransfer_lbl.palette()        
        scriptsToTransfer_lbl_Palette.setColor(self.scriptsToTransfer_lbl.foregroundRole(), qg.QColor.fromRgb(self.fontColor[0], self.fontColor[1], self.fontColor[2]))
        self.scriptsToTransfer_lbl.setPalette(scriptsToTransfer_lbl_Palette)


        #self.scriptList_scrollLayoutCombined = qg.QHBoxLayout()
        self.scriptsToMaya_layout = qg.QHBoxLayout()
        self.scriptsToMaya_layout.addWidget(self.scriptsToTransfer_lbl)
        self.scriptsToMaya_layout.addWidget(self.mayaVer_comboBox)

        self.scriptsToTransfer_layout = qg.QVBoxLayout()
        self.scriptsToTransfer_layout.addWidget(self.scriptList_scrollArea)              
        self.scriptsToTransfer_layout.addWidget(self.transfer_btn)
        self.transfer_btn.clicked.connect(lambda: self.transferToMaya())

        self.transfer_btn.clicked.connect(self.printListOfScripts)

        scriptTrans_widget.layout().addLayout(self.dirLayout)
        scriptTrans_widget.layout().addLayout(self.scriptsToMaya_layout)
        scriptTrans_widget.layout().addLayout(self.scriptsToTransfer_layout)
        #self.scriptList_scrollLayoutCombined.layout().addLayout(self.scriptsToTransfer_layout)
        #self.scriptList_scrollLayoutCombined.layout().addLayout(self.scriptsToMenu_layout)


        """

        DECLARATIONS FOR MAYA MENU GENERATION UI


        """

        makeMenu_widget = qg.QWidget()
        makeMenu_widget.setLayout(qg.QVBoxLayout())  

        self.makeMenu_btn = qg.QPushButton("Make Menu")
        self.makeMenu_btn.setFont(buttonFont)
        #self.makeMenu_btn.setFlat(True)
        self.makeMenu_btn.setStyleSheet("QPushButton { background-color: rgb%s; color: rgb%s; border: none;} QPushButton:pressed {background-color: rgb%s; color: rgb%s;} QPushButton:hover {background-color: rgb%s; color: rgb%s;}" % (self.buttonColor, self.fontColor, self.buttonPressedColor, self.fontColor, self.buttonPressedColor, self.fontColor ))
        
        #self.makeMenu_btn.setDisabled(True)
        #self.makeMenu_btn.setStyleSheet("QPushButton { background-color: rgb%s; color: rgb%s; border: none;}" % (self.scrollWidgetColor, self.fontColor, ))
        

        self.loadAvailableScripts_btn = qg.QPushButton("Load Scripts")
        self.loadAvailableScripts_btn.setFont(buttonFont)
        self.loadAvailableScripts_btn.setFlat(True)
        self.loadAvailableScripts_btn.setStyleSheet("QPushButton { background-color: rgb%s; color: rgb%s; border: none;} QPushButton:pressed {background-color: rgb%s; color: rgb%s;} QPushButton:hover {background-color: rgb%s; color: rgb%s;}" % (self.buttonColor, self.fontColor, self.buttonPressedColor, self.fontColor, self.buttonPressedColor, self.fontColor ))
        self.loadAvailableScripts_btn.clicked.connect(self.loadScriptsinMaya)

        self.menuList_scrollLayout = qg.QFormLayout()

        # scroll area widget contents
        self.menuList_scrollWidget = qg.QWidget()
        self.menuList_scrollWidget.setLayout(self.menuList_scrollLayout)

        self.menuList_scrollArea = qg.QScrollArea()
        self.menuList_scrollArea.setWidgetResizable(True)
        self.menuList_scrollArea.setWidget(self.menuList_scrollWidget)


        menuList_Palette = self.menuList_scrollWidget.palette()        
        menuList_Palette.setColor(self.menuList_scrollWidget.backgroundRole(), qg.QColor.fromRgb(self.scrollWidgetColor[0], self.scrollWidgetColor[1], self.scrollWidgetColor[2]))
        menuList_Palette.setColor(self.menuList_scrollWidget.foregroundRole(), qg.QColor.fromRgb(self.fontColor[0], self.fontColor[1], self.fontColor[2]))
        self.menuList_scrollWidget.setPalette(menuList_Palette)

        self.scriptsToMenu_layout = qg.QHBoxLayout()
        self.chooseScriptsForMenu_lbl = qg.QLabel("Load Scripts from Maya ")
        self.chooseScriptsForMenu_lbl.setAlignment(qc.Qt.AlignCenter)
        self.chooseScriptsForMenu_lbl.setFont(labelFont)

        chooseScriptsForMenu_lbl_Palette = self.chooseScriptsForMenu_lbl.palette()        
        chooseScriptsForMenu_lbl_Palette.setColor(self.chooseScriptsForMenu_lbl.foregroundRole(), qg.QColor.fromRgb(self.fontColor[0], self.fontColor[1], self.fontColor[2]))
        self.chooseScriptsForMenu_lbl.setPalette(chooseScriptsForMenu_lbl_Palette)

        self.nameForMenu_layout = qg.QHBoxLayout()
        self.nameForMenu_lbl = qg.QLabel("Name for Maya Menu ")
        self.nameForMenu_lbl.setAlignment(qc.Qt.AlignCenter)
        self.nameForMenu_lbl.setFont(labelFont)

        nameForMenu_lbl_Palette = self.nameForMenu_lbl.palette()        
        nameForMenu_lbl_Palette.setColor(self.nameForMenu_lbl.foregroundRole(), qg.QColor.fromRgb(self.fontColor[0], self.fontColor[1], self.fontColor[2]))
        self.nameForMenu_lbl.setPalette(nameForMenu_lbl_Palette)

        self.nameForMenu_le = qg.QLineEdit("")

        self.nameForMenu_le.setStyleSheet("QLineEdit { background-color: rgb%s; color: rgb%s; border: none;}" % (self.scrollWidgetColor, self.fontColor,  ))
       
        self.nameForMenu_layout.addWidget(self.nameForMenu_lbl)        
        self.nameForMenu_layout.addWidget(self.nameForMenu_le)

        self.availableScriptsForMenu_lbl = qg.QLabel("")
        self.availableScriptsForMenu_lbl.setAlignment(qc.Qt.AlignCenter)
        self.availableScriptsForMenu_lbl.setFont(labelFont)

        availableScriptsForMenu_lbl_Palette = self.availableScriptsForMenu_lbl.palette()        
        availableScriptsForMenu_lbl_Palette.setColor(self.availableScriptsForMenu_lbl.foregroundRole(), qg.QColor.fromRgb(self.fontColor[0], self.fontColor[1], self.fontColor[2]))
        self.availableScriptsForMenu_lbl.setPalette(availableScriptsForMenu_lbl_Palette)

        self.scriptsToMenu_layout.addWidget(self.chooseScriptsForMenu_lbl)
        self.scriptsToMenu_layout.addWidget(self.mayaVer_comboBox2)

        self.mayaMenu_layout = qg.QVBoxLayout()
        self.mayaMenu_layout.addWidget(self.availableScriptsForMenu_lbl)
        self.mayaMenu_layout.addWidget(self.menuList_scrollArea)        
        self.mayaMenu_layout.addWidget(self.makeMenu_btn)

        self.makeMenu_btn.clicked.connect(lambda: self.makeMenu())

        #makeMenu_widget.layout().addLayout(self.dirLayout)
        makeMenu_widget.layout().addLayout(self.scriptsToMenu_layout)
        makeMenu_widget.layout().addLayout(self.nameForMenu_layout)
        makeMenu_widget.layout().addLayout(self.mayaMenu_layout)
        
        
        

        self.scriptTransfer_btn.clicked.connect(lambda: self.mainTransferBtn())
        self.scriptTransferHelp_btn.clicked.connect(lambda: self.scriptsHelpWindow())
        

        self.mayaMenuGen_btn.clicked.connect(lambda: self.mainMenuBtn())
        self.mayaMenuGenHelp_btn.clicked.connect(lambda: self.mayaMenuHelpWindow())



        
        self.stacked_layout.addWidget(scriptTrans_widget)
        self.stacked_layout.addWidget(makeMenu_widget)
        # central widget
        self.centralWidget = qg.QWidget()
        self.centralWidget.setLayout(qg.QVBoxLayout())
        self.centralWidget.layout().addLayout(buttonMenu_layout)
        self.centralWidget.layout().addLayout(self.stacked_layout)

        # set central widget
        self.setCentralWidget(self.centralWidget)

    def mainTransferBtn(self):
        self.stacked_layout.setCurrentIndex(0) 
        self.scriptTransfer_btn.setDisabled(True)
        self.mayaMenuGen_btn.setEnabled(True)
        
        self.scriptTransfer_btn.setStyleSheet("QPushButton { background-color: rgb%s; color: rgb%s; border: none;}" % (self.buttonPressedColor, self.fontColor, ))
        self.mayaMenuGen_btn.setStyleSheet("QPushButton { background-color: rgb%s; color: rgb%s; border: none;}" % (self.scrollWidgetColor, self.fontColor, ))
   
        self.scriptTransferHelp_btn.setEnabled(True)
        self.scriptTransferHelp_btn.setStyleSheet("QPushButton { background-color: rgb%s; color: rgb%s; border: none;}" % (self.buttonColor, self.fontColor, ))

        self.mayaMenuGenHelp_btn.setDisabled(True)
        self.mayaMenuGenHelp_btn.setStyleSheet("QPushButton { background-color: rgb%s; color: rgb%s; border: none;}" % (self.scrollWidgetColor, self.fontColor, ))
   

    def mainMenuBtn(self):
        self.stacked_layout.setCurrentIndex(1) 
        self.scriptTransfer_btn.setEnabled(True)
        self.mayaMenuGen_btn.setDisabled(True)
       
        self.mayaMenuGen_btn.setStyleSheet("QPushButton { background-color: rgb%s; color: rgb%s; border: none;}" % (self.buttonPressedColor, self.fontColor, ))
        self.scriptTransfer_btn.setStyleSheet("QPushButton { background-color: rgb%s; color: rgb%s; border: none;}" % (self.scrollWidgetColor, self.fontColor, ))
        
        self.mayaMenuGenHelp_btn.setEnabled(True)
        self.mayaMenuGenHelp_btn.setStyleSheet("QPushButton { background-color: rgb%s; color: rgb%s; border: none;}" % (self.buttonColor, self.fontColor, ))
           
        self.scriptTransferHelp_btn.setDisabled(True)
        self.scriptTransferHelp_btn.setStyleSheet("QPushButton { background-color: rgb%s; color: rgb%s; border: none;}" % (self.scrollWidgetColor, self.fontColor, ))

        if self.mayaVer_comboBox2.currentText() == " ":
            self.fillComboBox(self.mayaVer_comboBox2, str(self.loadMayaDir()))
   

    """
    
    PATH RELATED FUNCTIONS


    """

    def osPath(self, filePath):
        print filePath
        print type(filePath)
        if os.path.isdir(filePath):
            return True
        else:
            return False

    #function to find directory and return path
    def findDir(self):

        Tkinter.Tk().withdraw() # Close the root window
        self.directoryPath = tkFileDialog.askdirectory()

        #print self.directoryPath
        #print type(self.directoryPath)
        self.directory_lbl.setText("Selected Directory: " + self.directoryPath)
        self.scriptsToTransfer_lbl.setText("Select Scripts to Transfer to Maya ")

        global listOfScripts

        if not listOfScripts:
            
            self.loadScriptsinDir(self.directoryPath)

            self.findDir_btn.setText('Source Directory Selected')
            self.findDir_btn.setDisabled(True)
            self.findDir_btn.setStyleSheet("QPushButton { background-color: rgb%s; color: rgb%s; border: none;}" % (self.scrollWidgetColor, self.fontColor, ))
        
            self.cancelDir_btn.setEnabled(True)
            self.cancelDir_btn.setStyleSheet("QPushButton { background-color: rgb%s; color: rgb%s; border: none;} QPushButton:pressed {background-color: rgb%s; color: rgb%s;} QPushButton:hover {background-color: rgb%s; color: rgb%s;}" % (self.buttonColor, self.fontColor, self.buttonPressedColor, self.fontColor, self.buttonPressedColor, self.fontColor ))
            
            self.transfer_btn.setEnabled(True)
            self.transfer_btn.setStyleSheet("QPushButton { background-color: rgb%s; color: rgb%s; border: none;} QPushButton:pressed {background-color: rgb%s; color: rgb%s;} QPushButton:hover {background-color: rgb%s; color: rgb%s;}" % (self.buttonColor, self.fontColor, self.buttonPressedColor, self.fontColor, self.buttonPressedColor, self.fontColor ))
            

        elif listOfScripts:
            listOfScripts[:] = []

            self.loadScriptsinDir(self.directoryPath)

            self.findDir_btn.setText('Source Directory Selected')
            self.findDir_btn.setDisabled(True)
            self.findDir_btn.setStyleSheet("QPushButton { background-color: rgb%s; color: rgb%s; border: none;}" % (self.scrollWidgetColor, self.fontColor, ))
        
            self.cancelDir_btn.setEnabled(True)
            self.cancelDir_btn.setStyleSheet("QPushButton { background-color: rgb%s; color: rgb%s; border: none;} QPushButton:pressed {background-color: rgb%s; color: rgb%s;} QPushButton:hover {background-color: rgb%s; color: rgb%s;}" % (self.buttonColor, self.fontColor, self.buttonPressedColor, self.fontColor, self.buttonPressedColor, self.fontColor ))
            
            self.transfer_btn.setEnabled(True)
            self.transfer_btn.setStyleSheet("QPushButton { background-color: rgb%s; color: rgb%s; border: none;} QPushButton:pressed {background-color: rgb%s; color: rgb%s;} QPushButton:hover {background-color: rgb%s; color: rgb%s;}" % (self.buttonColor, self.fontColor, self.buttonPressedColor, self.fontColor, self.buttonPressedColor, self.fontColor ))
            

    def getPath(self, filePath):
        if self.osPath(filePath): 
            return os.listdir(filePath)

    """

    GENERALLY USED FUNCTIONS

    """

    #function to print name of scripts
    def printListOfScripts(self):
        global listOfScripts
        print listOfScripts

    def printScriptList(self):
        for x in self.menuList_scrollWidget.children():
            #if isinstance(x, qg.QCheckBox):
            print "checkBox: %s" %(x.objectName())

    def resetScriptList(self):
        for x in self.scriptList_scrollWidget.children():
            if isinstance(x, qg.QCheckBox):
                x.deleteLater()
                x = None

        self.findDir_btn.setText('Select Source Directory')
        self.findDir_btn.setEnabled(True)
        self.findDir_btn.setStyleSheet("QPushButton { background-color: rgb%s; color: rgb%s; border: none;} QPushButton:pressed {background-color: rgb%s; color: rgb%s;} QPushButton:hover {background-color: rgb%s; color: rgb%s;}" % (self.buttonColor, self.fontColor, self.buttonPressedColor, self.fontColor, self.buttonPressedColor, self.fontColor ))
    
        self.cancelDir_btn.setDisabled(True)
        self.cancelDir_btn.setStyleSheet("QPushButton { background-color: rgb%s; color: rgb%s; border: none;}" % (self.scrollWidgetColor, self.fontColor, ))
        
        self.transfer_btn.setDisabled(True)
        self.transfer_btn.setStyleSheet("QPushButton { background-color: rgb%s; color: rgb%s; border: none;}" % (self.scrollWidgetColor, self.fontColor, ))
        

        self.directory_lbl.setText("")

    def loadMayaDir(self):
        userName = os.environ.get('USERNAME')

        mayaPath = "C:\Users\\" + userName + "\Documents\maya\\"

        return mayaPath

    #fills comboBox with maya versions
    def fillComboBox(self, comboBox, filePath):
        
        if self.osPath(filePath) and comboBox.isEditable(): 
            
            #clears default entry of comboBox
            comboBox.removeItem(comboBox.currentIndex())

            mayaPath = filePath
            
            print "Paths:", mayaPath
            
            for ver in os.listdir(mayaPath):
                
                if "20" in ver:
                    print ver
                    comboBox.addItem(ver)

            comboBox.setEditable(False)

    """

    FUNCTIONS TO TRANSFER SCRIPTS TO MAYA VER

    """

    #function to add button 
    def addWidget(self, scriptName):
        self.scriptList_scrollLayout.addRow(checkBoxes(scriptName))        
        #self.menuList_scrollLayout.addRow(checkBoxes(scriptName))


    #function to iterate through directory and call function to create button when python script is found
    def loadScriptsinDir(self, path):

        if self.getPath(path):
            scriptPath = self.getPath(path)

            #print scriptPath            


            for file in os.listdir(path):
                
                if file.endswith(".py") or file.endswith(".mel") or file.endswith(".ui"):
                    tempScriptName = str(file)
                    #print tempScriptName
                    #self.scriptName = property(lambda self: self.tempScriptName)
                    #self.scriptName = property(lambda self: "foo")
                    
                    self.addWidget(tempScriptName)

            self.fillComboBox(self.mayaVer_comboBox, str(self.loadMayaDir()))
            #self.fillComboBox(self.mayaVer_comboBox2, str(self.loadMayaDir()))

        else:
            print "BAD PATH"       

    def transferToMaya(self):        
        mayaPath = self.loadMayaDir() + self.mayaVer_comboBox.currentText() + "\scripts"
        print mayaPath
        print self.directoryPath
        for script in os.listdir(self.directoryPath):
            #print script
            if script in listOfScripts:
                
                scriptFileName = os.path.join(self.directoryPath, script)
                #print "scriptName: " + scriptFileName
                shutil.copy(str(scriptFileName), str(mayaPath))
                #self.centralWidget.addWidget(checkBoxes())

        self.popupWindow("Successfully Transferred Selected Scripts to Maya " + self.mayaVer_comboBox.currentText())

    def popupWindow(self, message):

        WidgetColor = (60, 60, 60)

        popupWindow = qg.QMessageBox()
        
        popupWindow.setInformativeText(message)
        popupWindow.setStandardButtons(qg.QMessageBox.Ok)

        popupWindow.setStyleSheet("QMessageBox { background-color: rgb%s; color: rgb%s;}" % (WidgetColor, self.fontColor, ))

        popupWindow.exec_()

    def scriptsHelpWindow(self):

        WidgetColor = (60, 60, 60)

        popupWindow = qg.QMessageBox()
        
        message = "Scripts Transfer is intended to be a tool to simplify the process of getting scripts into the preferred version of Maya. \n \
        The steps to use this tool are as follows: \n \
        1. Select the directory the user has their script inventory \n \
        2. The user should designate the version of Maya they want to send the scripts to \n \
        3. The user would then pick from the generated list of the scripts they want to send to their designated version of Maya \n \
        4. Pressing the Transfer Scripts button will send the selected scripts to the corresponding directory for scripts in the designated version of Maya \
        "

        popupWindow.setInformativeText(message)
        popupWindow.setStandardButtons(qg.QMessageBox.Ok)

        """
        help_Palette = qg.QPalette()       
        help_Palette.setColor(qg.QPalette().Background, qg.QColor(WidgetColor[0], WidgetColor[1], WidgetColor[2]))
        help_Palette.setColor(qg.QPalette().ButtonText, qg.QColor.fromRgb(self.fontColor[0], self.fontColor[1], self.fontColor[2]))
        help_Palette.setColor(qg.QPalette().Text, qg.QColor(self.fontColor[0], self.fontColor[1], self.fontColor[2]))
        help_Palette.setColor(qg.QPalette().Base, qg.QColor(self.fontColor[0], self.fontColor[1], self.fontColor[2]))
        
        popupWindow.setPalette(help_Palette)
        """
        popupWindow.setStyleSheet("QMessageBox { background-color: rgb%s; color: rgb%s;}" % (WidgetColor, self.fontColor, ))

        popupWindow.exec_()

    def mayaMenuHelpWindow(self):

        WidgetColor = (60, 60, 60)

        popupWindow = qg.QMessageBox()
        
        message = "Make Maya Menu is intended to be a tool to simplify the process of make a Maya menu from the available scripts in the the preferred version of Maya. \n \
        The steps to use this tool are as follows: \n \
        1. Choose the prefferred version of Maya. The tool will determine if there are scripts within Maya's local script folder. \n \
        2. If there are available scripts a list of scripts will be generated. If there are no scripts available nothing will be generated. \n \
        3. If a list of scripts is generated, select the scripts that would be added to the Maya menu and add a description for the script as it will appear in the Maya menu \n \
        4. Pressing the Make Menu button will create a Maya menu entry from the selected scripts in the designated version of Maya \
        "

        popupWindow.setInformativeText(message)
        popupWindow.setStandardButtons(qg.QMessageBox.Ok)

        """
        help_Palette = qg.QPalette()       
        help_Palette.setColor(qg.QPalette().Background, qg.QColor(WidgetColor[0], WidgetColor[1], WidgetColor[2]))
        help_Palette.setColor(qg.QPalette().ButtonText, qg.QColor.fromRgb(self.fontColor[0], self.fontColor[1], self.fontColor[2]))
        help_Palette.setColor(qg.QPalette().Text, qg.QColor(self.fontColor[0], self.fontColor[1], self.fontColor[2]))
        help_Palette.setColor(qg.QPalette().Base, qg.QColor(self.fontColor[0], self.fontColor[1], self.fontColor[2]))
        
        popupWindow.setPalette(help_Palette)
        """
        popupWindow.setStyleSheet("QMessageBox { background-color: rgb%s; color: rgb%s;}" % (WidgetColor, self.fontColor, ))

        popupWindow.exec_()

    """

    FUNCTIONS TO MAKE MENU FOR MAYA VER

    """
    

    def makeMenu(self):
        global dictOfMenuScripts        

        if not dictOfMenuScripts:
            self.popupWindow("NO SCRIPTS ARE SELECTED TO MAKE A MAYA MENU")
        elif self.nameForMenu_le.text() == "":
            self.popupWindow("PROVIDE A NAME FOR THE MENU")
        else: 
            self.writeMenuFile()
            self.writeSetupFile()

    def writeSetupFile(self):
        mayaPath = self.loadMayaDir() + self.mayaVer_comboBox2.currentText() + "\scripts"

        userSetup = "userSetup"
        menuName = self.nameForMenu_le.text()
        menuExt = ".mel"

        userSetupFileName = userSetup + menuExt

        menuFileName = menuName + menuExt

        evalLine = "print (\"Sourcing Menu...\\n\"); \n \
        eval (\"" + "source \\\"" + menuFileName + "\\\"\");"

        setupFile = open(mayaPath + "\\" + userSetupFileName, "w+")

        setupFile.write(evalLine)

        setupFile.close()

    def writeMenuFile(self):
        mayaPath = self.loadMayaDir() + self.mayaVer_comboBox2.currentText() + "\\scripts"


        menuUIName = self.nameForMenu_le.text()
        menuName = self.nameForMenu_le.text()
        menuExt = ".mel"
        menuFunction = ""
        menuCatchVar = ""
        menuTestCase = ""
        menuFileName = menuName + menuExt

        global dictOfMenuScripts
        
        menuCatchVar = "string $menuName; \n \
        if (catch($menuName = `menu -q -label " + menuName + "`)) \n \
        {" + " \n \
            print \"no menu\"; \n \
        } \n \
        else \n \
        { \n \
            if($menuName == \"" + menuUIName + "\") \n \
                deleteUI " + menuName + "; \n \
        }\n"

        menuFunction = "global proc " + menuName + "() \n \
        {" + "\n \
        menu -parent MayaWindow -tearOff true -label \"" + menuUIName + "\"" + menuName + "; \n"
        
        for x, y in dictOfMenuScripts.items():
            scriptName = x.split(".")
            print dictOfMenuScripts[x]["Menu Description"]
            menuFunction += "menuItem -p " + menuName + " -l " + "\""+ dictOfMenuScripts[x]["Menu Description"] + "\"" + " -c \"python(\\\"import " + scriptName[0] + "\\\")\"; \n"
       
        menuFunction += "}\n"

        menuTestCase = "if ( ! `about -b`) \n \
        { \n" + menuName + "(); \n }\n"

        menuFile = open(mayaPath + "\\" + menuFileName, "w+")

        menuFile.write(menuCatchVar + menuFunction + menuTestCase)

        menuFile.close()

        self.popupWindow("Successfully Made Menu for Maya ")

    #function to add button 
    def addMenuWidget(self, scriptName):
        self.menuList_scrollLayout.addRow(makeMenuWidget(scriptName))        
        #self.menuList_scrollLayout.addRow(checkBoxes(scriptName))

    def loadScriptsinMaya(self):

        print self.mayaVer_comboBox2.currentText()
        mayaPath = self.loadMayaDir() + str(self.mayaVer_comboBox2.currentText()) + "\scripts"

        print mayaPath

        foundScripts = False                 

        for file in os.listdir(mayaPath):
            
            if file.endswith(".py") or file.endswith(".mel"):
                tempScriptName = str(file)
                #print tempScriptName
                #self.scriptName = property(lambda self: self.tempScriptName)
                #self.scriptName = property(lambda self: "foo")
                
                self.addMenuWidget(tempScriptName)
                foundScripts = True


        if foundScripts:
            self.availableScriptsForMenu_lbl.setText("Available Scripts for Maya " + self.mayaVer_comboBox2.currentText())
            
        elif not foundScripts:
            self.availableScriptsForMenu_lbl.setText("No Scripts Available for Maya " + self.mayaVer_comboBox2.currentText())


    def resetMenuScriptList(self):
        for x in self.menuList_scrollWidget.children():
            if not isinstance(x, qg.QLayout):
                x.deleteLater()
                x = None

class checkBoxes(qg.QCheckBox):
    def __init__(self, scriptName = '', parent = None):
        super(checkBoxes, self).__init__(parent)

        self.fontColor = (200, 200, 200)
        self.buttonPressedColor = (82,133,166)
        #self.setStyleSheet("QPushButton { background-color: rgb%s; color: rgb%s; border: none;}" % (self.buttonPressedColor, self.fontColor, ))
        
        checkBox_Palette = self.palette()        
        checkBox_Palette.setColor(qg.QPalette.Text, qg.QColor.fromRgb(self.fontColor[0], self.fontColor[1], self.fontColor[2]))
        self.setPalette(checkBox_Palette)
        self.setObjectName(scriptName)
        self.setText(scriptName)
        self.setChecked(False)
        #self.stateChanged.connect(lambda:self.btnstate(self.b1))
        #layout.addWidget(self.b1)

        #calls function on click to change button color and add script name to list in Main class
        self.clicked.connect(lambda: self.buttonClicked(self.text()))

    #function called when button is clicked
    def buttonClicked(self, text):
        if self.isChecked():
            self.addScriptToList(str(text))
            self.setButtonColor()
        else:
            self.removeScriptFromList(str(text))
            self.resetButtonColor()

    #add text of button to list in Main class
    def addScriptToList(self, script):
        
        global listOfScripts
        #print str(self.parent().objectName())
        listOfScripts.append(script)

    def removeScriptFromList(self, script):
        
        global listOfScripts
        listOfScripts.remove(script)

    #sets button color on click
    def setButtonColor(self):
        self.fontColor = (200, 200, 200)
        self.buttonPressedColor = (82,133,166)
        #self.setStyleSheet("QPushButton { background-color: rgb%s; color: rgb%s; border: none;}" % (self.buttonPressedColor, self.fontColor, ))
        
        checkBox_Palette = self.palette()        
        checkBox_Palette.setColor(qg.QPalette.Text, qg.QColor.fromRgb(self.fontColor[0], self.fontColor[1], self.fontColor[2]))
        self.setPalette(checkBox_Palette)

    def resetButtonColor(self):
        self.setStyleSheet("")

class makeMenuWidget(qg.QWidget):
    def __init__(self, scriptName = '', parent = None):
        super(makeMenuWidget, self).__init__(parent)

        self.setObjectName(scriptName)

        self.scrollWidgetColor = (75, 75, 75)
        self.fontColor = (200, 200, 200)

        self.setLayout(qg.QHBoxLayout())

        self.NameOfScript_checkBox = qg.QCheckBox(scriptName) 
        self.NameOfScript_checkBox.setDisabled(True)

        scriptName_Seperator = qg.QFrame()
        scriptName_Seperator.setFrameShape(qg.QFrame.VLine)
        scriptName_Seperator.setFrameShadow(qg.QFrame.Sunken)        

        scriptMenuName_layout = qg.QVBoxLayout()

        tempName = scriptName.split(".")

        self.menuNameForScript_lbl = qg.QLabel("Give "+ tempName[0] +" a description to add it to the Maya Menu: ")       
        width = self.menuNameForScript_lbl.sizeHint().width()
        height = self.menuNameForScript_lbl.sizeHint().height()

        self.scriptMenuDescription_le = qg.QLineEdit("")
        self.scriptMenuDescription_le.setFixedSize(width, height)

        self.scriptMenuDescription_le.setStyleSheet("QLineEdit { background-color: rgb%s; color: rgb%s; border: none;}" % (self.scrollWidgetColor, self.fontColor,  ))
        
        scriptMenuName_layout.addWidget(self.menuNameForScript_lbl)
        scriptMenuName_layout.addWidget(self.scriptMenuDescription_le)

        self.NameOfFunctions_lbl = qg.QLabel("Function to Call:")

        self.functions_comboBox = qg.QComboBox()

        self.layout().addLayout(scriptMenuName_layout)        
        self.layout().addWidget(scriptName_Seperator)
        self.layout().addWidget(self.NameOfScript_checkBox)
        #self.layout().addWidget(self.NameOfFunctions_lbl)
        #self.layout().addWidget(self.functions_comboBox)

        self.scriptMenuDescription_le.editingFinished.connect(lambda: self.lineEditValue())
        self.NameOfScript_checkBox.stateChanged.connect(lambda: self.buttonClicked(self.NameOfScript_checkBox.text()))

    def lineEditValue(self):
        if self.scriptMenuDescription_le.text() == "":
            self.NameOfScript_checkBox.setChecked(False)
            
        else:
            self.NameOfScript_checkBox.setChecked(True)

            

    #function called when button is clicked
    def buttonClicked(self, text):
        if self.NameOfScript_checkBox.isChecked():
            self.addScriptToDict(str(text))
            self.setButtonColor()
        else:
            self.removeScriptFromDict(str(text))
            self.resetButtonColor()

    #add text of button to list in Main class
    def addScriptToDict(self, script):
        
        global dictOfMenuScripts
        #print str(self.parent().objectName())
        tempDict = collections.OrderedDict()
        tempDict["Menu Description"] = self.scriptMenuDescription_le.text()

        dictOfMenuScripts[script] = tempDict

        print dictOfMenuScripts

    def removeScriptFromDict(self, script):
        
        global dictOfMenuScripts
        del dictOfMenuScripts[script]

    #sets button color on click
    def setButtonColor(self):
        self.fontColor = (200, 200, 200)
        self.buttonPressedColor = (82,133,166)
        self.setStyleSheet(" background-color: green; color: rgb%s;" % (self.fontColor,))         
            

    def resetButtonColor(self):
        self.setStyleSheet("")

"""
#button class
class LoadScripts(qg.QPushButton):
    def __init__( self, scriptName = '', parent=None, ):
      super(LoadScripts, self).__init__(scriptName, parent )

      self.setCheckable(True)

      #sets button text as name of script
      self.setText(scriptName)
      #neat feature to delete button
      #self.clicked.connect(self.deleteLater)

      #calls function on click to change button color and add script name to list in Main class
      self.clicked.connect(lambda: self.buttonClicked(self.text()))

    #function called when button is clicked
    def buttonClicked(self, text):
        if self.isChecked():
            self.addScriptToList(str(text))
            self.setself.ButtonColor()
        else:
            self.removeScriptFromList(str(text))
            self.resetself.ButtonColor()

    #add text of button to list in Main class
    def addScriptToList(self, script):
        
        global listOfScripts
        listOfScripts.append(script)

    def removeScriptFromList(self, script):
        
        global listOfScripts
        listOfScripts.remove(script)

    #sets button color on click
    def setself.ButtonColor(self):
        self.setStyleSheet("QPushButton { background-color: green }" )        
            

    def resetself.ButtonColor(self):
        self.setStyleSheet("")
"""




app = qg.QApplication(sys.argv)
myWidget = Main()
myWidget.show()
app.exec_()



