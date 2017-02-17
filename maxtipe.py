DebugMode = False
#DebugMode = True
#### IMPORTS ####
from sys import *
import os
import datetime
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, SimpleDocTemplate

#### CLASSES ####
class TextStyle:
    EndC       = '\033[0m'
    Black      = '\033[30m'
    Red        = '\033[31m'
    Green      = '\033[32m'
    Brown      = '\033[33m'
    Blue       = '\033[34m'
    Purple     = '\033[35m'
    Cyan       = '\033[36m'
    LightGrey  = '\033[37m'
    Grey       = '\033[90m'
    LightRed   = '\033[91m'
    LightGreen = '\033[92m'
    Yellow     = '\033[93m'
    LightBlue  = '\033[94m'
    Pink       = '\033[95m'
    LightCyan  = '\033[96m'

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
global LogLocation
global UseLog
global TxtOutput
global TxtOutLocation
global TxtOutData
DocumentStarted = False
BoldOpened      = False
ItalicsOpened   = False
LogLocation     = ""
UseLog          = True
TxtOutput       = False
TxtOutLocation  = ""
TxtOutData      = []

#### LISTS ####
StopChars = [" ", "{", "}", "\n"]

#### FUNCTIONS ####
def Log(msg, **kwargs):
    if "LogType" in kwargs:
        lType = kwargs["LogType"]
    else:
        lType = "Default"
    Time = str(datetime.datetime.now())
    FullMsg = "[" + Time + "] " + "[" + lType + "] " + msg + "\n"
    if UseLog:
        file = open(LogLocation, "a+")
        file.write(FullMsg)

def RaiseNegativeMessage(msg):
    print(msg)
    Log(msg, LogType="Error")
    exit()

def RaiseLearningMessage(msg):
    print(msg)
    Log(msg, LogType="Error")
    exit()

def RaiseOKMessage(msg):
    print(msg)
    Log(msg)

def OpenFile(filename):
    global LogLocation
    LogLocation = filename.replace(os.path.basename(filename), "")+"log.txt"
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
    xFile = []      # I know it's a bad name, but I don't care enough to change it
    global DocumentStarted
    global UseLog
    global TxtOutput
    global TxtOutLocation
    global TxtOutData
    while i < len(tokens):
        if(DocumentStarted == False):
            while tokens[i] != "{":
                i+=1
            if tokens[i] == "{":
                if(tokens[i+1] != "START" and tokens[i+1].upper() == "START"):
                    RaiseLearningMessage("Can not accept command \"" + tokens[i+1] + ".\" Command must be capitalized as \"START\"")
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
                                if(tokens[i+1] == "\n"):
                                    i+=1
                            else:
                                RaiseNegativeMessage("Curly bracket decleration must be terminated immediately after declaring start of document.")
                        else:
                            RaiseNegativeMessage("Curly bracket decleration must be terminated immediately after declaring start of document.")
        elif(DocumentStarted == True):
            if tokens[i] == "{":
                if(tokens[i+1] != "OUTPUT" and tokens[i+1].upper() == "OUTPUT"):
                    RaiseLearningMessage("Can not accept command \"" + tokens[i+1] + ".\" Command must be capitalized as \"OUTPUT\"")
                elif(tokens[i+1] == "OUTPUT"):
                    i+=2
                    TxtOutput = True
                    while(tokens[i] != "}"):
                          xFile.append(tokens[i])
                          i+=1
                    if(tokens[i] == "}"):
                        if(len(xFile) > 0): 
                            for item in xFile:
                                TxtOutLocation+=str(item)
                            if(len(xFile) > 1):
                                RaiseOKMessage("File location can not have spaces or other non alphanumeric characters. File has been saved as \"" + TxtOutLocation +"\" instead")
                        i+=1
                    if(tokens[i] == "\n"):
                        i+=1
                elif(tokens[i+1] != "END" and tokens[i+1].upper() == "END"):
                    RaiseLearningMessage("Can not accept command \"" + tokens[i+1] + ".\" Command must be capitalized as \"START\"")
                elif(tokens[i+1] == "END"):
                    if(tokens[i+2].upper() == "DOCUMENT"):
                        if(tokens[i+3] == "}"):
                            DocumentStarted = False
                            i+=4
                        else:
                            RaiseNegativeMessage("Curly bracket decleration must be terminated immediately after declaring end of document.")
            elif tokens[i] == "\n":
                TxtOutData.append(tokens[i])
                i+=1
            elif tokens[i] != "{" and tokens[i] != "}":
                TxtOutData.append(tokens[i])
                i+=1
    Log("Successfuly ran program!", LogType="Success")

def OutputData():
    global TxtOutput
    global TxtOutData
    global TxtOutLocation
    style = getSampleStyleSheet()['Normal']
    style.wordWrap = 'LTR'
    txt = ""
    punctuation = [".", "!"]
    tok = ""
    words = []
    Story = []
    paras = []
    styles=getSampleStyleSheet()
    if(TxtOutput == True):
        if(TxtOutData[0] == "\n"):
            TxtOutData.pop(0)
        if(TxtOutData[-1] == "\n"):
            TxtOutData.pop()

        for item in TxtOutData:
            txt += str(item)
            if item != "\n" and item[-1:] not in punctuation :
                txt+=" "
        if TxtOutLocation[-4:] != ".pdf":
            try:
                FileLocation = open(TxtOutLocation, "w+")
            except Exception:
                RaiseNegativeMessage("Could not create file in directory. Please check if directory exists and if program has sufficient permissions")
            FileLocation.write(txt)
            FileLocation.close()
        else:
            doc = SimpleDocTemplate(TxtOutLocation, pagesize=letter,rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
            for item in TxtOutData:
                if item == " \n" or item == ".\n" or item == "\n":
                    paras.append(txt)
                    txt = ""
                    item = ""
                else:
                    txt += str(item)
                    if item != "\n" and item[-1:] not in punctuation :
                        txt+=" "
                
            txt = txt.replace("\n", "<br/>")
            print(paras)
            for item in paras:
                print(item)
                Story.append(Paragraph(item, styles["Normal"]))
            doc.build(Story)
            #print(txt)
            """c = canvas.Canvas(TxtOutLocation, pagesize=letter)
            t = c.beginText(50, 782-35)
            #t.setFont("Times", 14)
            width, height =letter
            txt+="\n"
            for char in txt:
                if char != "\n":
                    tok+=char
                else:
                    words.append(tok)
                    tok = ""
            for thing in words:
                t.textLine(thing)

            #c.drawString(100, height - 100, textobject)
            #c.drawText(t)
            #print(TxtOutData)
            c.drawText(t)
            c.showPage()
            c.save()"""
def Run():
    data = OpenFile(argv[1])
    toParse = Lex(data)
    Parse(toParse)
    OutputData()

#### MAIN ####
Run()
