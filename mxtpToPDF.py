DebugMode = False
#### IMPORTS ####
from sys import *
from PyPDF2 import PdfFileWriter
op = PdfFileWriter()

#### CLASSES ####
class PageSize:
    class Default:
        class Portrait:
            Width  = 612
            Height = 792
        class Landscape:
            Width  = 792
            height = 612

#### VARIABLES ####
global DocumentStarted
global ForPDF
global OutputLocation
DocumentStarted = False
OutputLocation = ""
ForPDF = []

#### LISTS ####
StopChars = [" ", "{", "}", "\n"]

#### FUNCTIONS ####
def RaiseNegativeMessage(msg):
    print(TextStyle.LightRed + msg + TextStyle.EndC)
    Log(msg, LogType="Error")
    exit()

def RaiseLearningMessage(msg):
    print(TextStyle.Yellow + msg + TextStyle.EndC)
    Log(msg, LogType="Error")
    exit()


def OpenFile(filename):
    if filename[-5:] != ".mxtp":
       RaiseNegativeMessage("Can not open file. Can only open \".mxtp\" files")
       exit()
    else:
        data = open(filename, "r",).read()
        return(data)

def Lex(filecontents):
    toks = []
    tokens = []
    for char in filecontents:
        if char in StopChars:
            if len(toks) > 0:
                tokens.append(toks)
            if char != " ":
                tokens.append(char)
            toks = ""
        else:
            toks+=char
    if(DebugMode):
        print(tokens)
        return(["","","","",""])
    else:
        return(tokens)

def Parse(tokens):
    i = 0
    global DocumentStarted
    while i < len(tokens):
        if(DocumentStarted == False):
            if tokens[i] == "{":
                if(tokens[i+1] != "START" and tokens[i+1].upper() == "START"):
                    RaiseLearningMessage("Can not accept command \"" + tokens[i+1] + "\"\nCommand must be capitalized as \"START\"")
                elif(tokens[i+1] == "START"):
                    if(tokens[i+2].upper() == "DOCUMENT"):
                        if(tokens[i+3] == "}"):
                            DocumentStarted = True
                            i+=4
                        elif(tokens[i+3].upper() == "NOLOG"):
                            if(tokens[i+4] == "}"):
                                DocumentStarted = True
                                UseLog = False
                                i+=5
                            else:
                                RaiseNegativeMessage("Curly bracket decleration must be terminated immediately after declaring start of document.")
                        else:
                            RaiseNegativeMessage("Curly bracket decleration must be terminated immediately after declaring start of document.")
        elif(DocumentStarted == True):
            if tokens[i] == "{":
                if(tokens[i+1] != "END" and tokens[i+1].upper() == "END"):
                    RaiseLearningMessage("Can not accept command \"" + tokens[i+1] + "\"\nCommand must be capitalized as \"START\"")
                elif(tokens[i+1] == "END"):
                    if(tokens[i+2].upper() == "DOCUMENT"):
                        if(tokens[i+3] == "}"):
                            DocumentStarted = False
                            i+=4
                        else:
                            RaiseNegativeMessage("Curly bracket decleration must be terminated immediately after declaring end of document.")
            elif tokens[i] == "\n":
                ForPDF.append(tokens[i])
                i+=1
            else:
                ForPDF.append(tokens[i])
                i+=1

def AddToPDF(OutputLocation, Data):
    op.addBlankPage(612, 792)
    file = open(OutputLocation, "wb")
    op.write(file)
    file.close()
    
def Run():
    global OutputLocation
    OutputLocation = input("PDF Output Location:  ")
    data = OpenFile(argv[1])
    toParse = Lex(data)
    Parse(toParse)
    AddToPDF(OutputLocation, ForPDF)
    print(OutputLocation)
    print(ForPDF)

#### MAIN ####
Run()
    
