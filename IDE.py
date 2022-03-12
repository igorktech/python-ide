import tkinter
import os
from tkinter import *
from tkinter import colorchooser
from tkinter.messagebox import *
from tkinter.filedialog import *
from turtle import fillcolor, width
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter.scrolledtext import ScrolledText
import subprocess
import json
import sys

class Notepad:
    __root = Tk()
    __thisWidth = 300
    __thisHeight = 300
    __thisTextArea = Text(__root, font=("haveltica 10 bold"), wrap=None)
    __thisTextArea.pack(fill=BOTH, expand=1)
    __thisTextArea.focus()
    __thisMenuBar = Menu(__root)
    __thisFileMenu = Menu(__thisMenuBar, tearoff = 0)
    __thisEditMenu = Menu(__thisMenuBar, tearoff = 0)
    __thisRunMenu = Menu(__thisMenuBar,tearoff = 0)
    __thisViewMenu = Menu(__thisMenuBar,tearoff = 0)
    __thisThemeMenu = Menu(__thisMenuBar, tearoff = 0)
    __thisHelpMenu = Menu(__thisMenuBar, tearoff = 0)
    # create output window to display output of written code
    __thisOutputWindow = Text(__root, height=30)
    __thisOutputWindow.pack(fill=BOTH, expand=1)
    # scrollbar
    __thisScrollBar = Scrollbar(__thisTextArea)
    __thisOutputScrollBar = Scrollbar(__thisOutputWindow)
    # status bar
    __thisStatusBars = ttk.Label(__root,text = "github.com/igorkkkk/PythonIDE \t\t\t\t\t\t characters: 0 words: 0")
    __thisStatusBars.pack(side = BOTTOM)
    __show_status_bar = BooleanVar()
    __show_status_bar.set(True)

    __text_change = BooleanVar()
    __text_change.set(False) 

    __file = None
    __color_theme = None
    __local_path = "Themes//theme1.json"

    def __init__(self, **kwargs):
        # icon
        try:
            self.__root.wm_iconbitmap("Python.ico")
        except:
            pass
        # window size
        try:
            self.__thisWidth = kwargs['width']
        except KeyError:
            pass
        try:
            self.__thisHeight = kwargs['height']
        except KeyError:
            pass

        #load color theme
        try:
            self.__my_theme()
        except:
            pass

        # text
        self.__root.title("Untitled - PyNotepad")
        # center the window
        screenWidth = self.__root.winfo_screenwidth()
        screenHeight = self.__root.winfo_screenheight()

        left = (screenWidth / 2) - (self.__thisWidth / 2)

        top = (screenHeight / 2) - (self.__thisHeight / 2)

        self.__root.geometry('%dx%d+%d+%d' % (self.__thisWidth, self.__thisHeight,left,top))
        # autoresize
        self.__root.grid_rowconfigure(0,weight = 1)
        self.__root.grid_columnconfigure(0,weight = 1)
        # controls
       # self.__thisTextArea.grid(sticky=N + E + S + W)
        # open new file
        self.__thisFileMenu.add_command(label = "New", command = self.__newFile)
        # open existing
        self.__thisFileMenu.add_command(label = "Open", command = self.__openFile)
        # save current
        self.__thisFileMenu.add_command(label = "Save", command = self.__saveFile)
        # create line in the dialog
        self.__thisFileMenu.add_separator()
        self.__thisFileMenu.add_command(label = "Exit", command = self.__quitApplication)
        self.__thisMenuBar.add_cascade(label = "File", menu = self.__thisFileMenu)
        # cut
        self.__thisEditMenu.add_command(label = "Cut", command = self.__cut)
        # copy
        self.__thisEditMenu.add_command(label = "Copy", command = self.__copy)
        # paste
        self.__thisEditMenu.add_command(label = "Paste", command = self.__paste)
        # editing
        self.__thisMenuBar.add_cascade(label = "Edit", menu = self.__thisEditMenu)
        # run
        self.__thisMenuBar.add_cascade(label="Run", menu = self.__thisRunMenu)
        self.__thisRunMenu.add_command(label="Run", accelerator="F5", command=self.__run)
        # view
        self.__thisMenuBar.add_cascade(label ="View", menu = self.__thisViewMenu)
        self.__thisViewMenu.add_checkbutton(label = "Status Bar" , onvalue = True, offvalue = 0,variable = self.__show_status_bar , command = self.__hide_statusbar)
        # create a label for status bar
        # self.__thisStatusBars = ttk.Label(window,text = "www.codershubb.com \t\t\t\t\t\t characters: 0 words: 0")
        # status_bars.pack(side = BOTTOM) TODO
        # theme
        self.__thisMenuBar.add_cascade(label ="Theme", menu = self.__thisThemeMenu)
        self.__thisThemeMenu.add_command(label = "light", command = self.__light)
        self.__thisThemeMenu.add_command(label = "dark", command = self.__dark)
        self.__thisThemeMenu.add_command(label = "my theme", command = self.__my_theme)
        self.__thisThemeMenu.add_command(label = "import color theme", command = self.__import_color_theme)
        # description
        self.__thisHelpMenu.add_command(label = "About Notepad", command = self.__showAbout)
        self.__thisMenuBar.add_cascade(label = "Help", menu = self.__thisHelpMenu)
        self.__root.config(menu = self.__thisMenuBar)
        

        self.__thisScrollBar.pack(side = RIGHT, fill = Y)
        # scrollbar adjust with content
        self.__thisScrollBar.config(command  = self.__thisTextArea.yview)
        self.__thisTextArea.config(yscrollcommand = self.__thisScrollBar.set)


        self.__thisOutputScrollBar.pack(side = RIGHT, fill = Y)
        # scrollbar adjust with content
        self.__thisOutputScrollBar.config(command  = self.__thisOutputWindow.yview)
        self.__thisOutputWindow.config(yscrollcommand = self.__thisOutputScrollBar.set)
        # function to display and hide status bar

    
    def __hide_statusbar(self):
        if self.__show_status_bar:
            self.__thisStatusBars.pack_forget()
            self.__show_status_bar = False 
        else :
            self.__thisStatusBars.pack(side=BOTTOM)
            self.__show_status_bar = True

    
    def __change_word(self):
        
        if self.__thisTextArea.edit_modified():
            self.__text_change = True
            word = len(self.__thisTextArea.get(1.0, "end-1c").split())
            chararcter = len(self.__thisTextArea.get(1.0, "end-1c").replace(" ",""))
            self.__thisStatusBars.config(text = f"github.com/igorkkkk/PythonIDE \t\t\t\t\t\t characters: {chararcter} words: {word}")
        self.__thisTextArea.edit_modified(False)
    __root.bind("<<Modified>>",__change_word)

    def __run(self):
        if self.__file == None:
            self.__saveFile()
        '''global code, __file
        
        code = editor.get(1.0, END)
        exec(code)
        '''    
        cmd = f"python {self.__file}"
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, shell=True)
        output, error =  process.communicate()
        # delete the previous text from
        # output_windows
        self.__thisOutputWindow.delete(1.0, END)
        # insert the new output text in
        # output_windows
        self.__thisOutputWindow.insert(1.0, output)
        # insert the error text in output_windows
        # if there is error
        self.__thisOutputWindow.insert(1.0, error)
    __root.bind("<F5>", __run)

    def __quitApplication(self):
        self.__root.destroy()
    __root.bind("<Control-q>", __quitApplication)
    

    def __showAbout(self):
        showinfo("PyNotepad","My notepad for run Python")

    def __openFile(self):
        self.__file = askopenfilename(defaultextension = ".py", filetypes = [("All Files","*.*"),
                                                                    ("Python Documents", "*.py")])
        if self.__file == "":
            # no file to open
            self.__file = None
        else:
            # try to open
            self.__root.title(os.path.basename(self.__file) + " - PyNotepad")
            self.__thisTextArea.delete(1.0,END)
            file  = open(self.__file, "r")
            self.__thisTextArea.insert(1.0,file.read())
            file.close()
    __root.bind("<Control-o>", __openFile)

    def __newFile(self):
        self.__root.title("Untitled - PyNotepad")
        self.__file = None
        self.__thisTextArea(1.0, END)

    def __saveFile(self):
        if self.__file == None:
            # save as new
            self.__file = asksaveasfilename(initialfile = 'Untitled.py', defaultextension= ".py", filetypes=
                                                         [("All Files","*.*"), ("Python Documents", "*.py")])
            if self.__file == "":
                self.__file = None
            else:
                # try to save
                file = open(self.__file,"w")
                file.write(self.__thisTextArea.get(1.0,END))
                file.close()
                # change window title
                self.__root.title(os.path.basename(self.__file) + " - PyNotepad")
        else:
            file = open(self.__file, "w")
            file.write(self.__thisTextArea.get(1.0,END))
            file.close()
    __root.bind("<Control-S>", __saveFile)

        # function for light mode window
    def __light(self):
      self.__thisTextArea.config(fg = 'black', bg = "white")
      self.__thisOutputWindow.config(fg = 'black', bg = "white")
    # function for dark mode window
    def __dark(self):
        self.__thisTextArea.config(fg="white", bg = "black")
        self.__thisOutputWindow.config(fg="white", bg = "black")

    def __my_theme(self):
        file  = open(self.__local_path, "r")
        if file == "":
            # no file to open
            self.__color_theme = None
        else:
            # try to open
            file  = open(self.__local_path, "r")
            data = file.read()
            self.__color_theme = json.loads(data)
            file.close()
            self.__thisTextArea.config(fg = self.__color_theme["brightYellow"], bg = self.__color_theme["background"],
            insertbackground = self.__color_theme["brightRed"])
            self.__thisOutputWindow.config(fg = self.__color_theme["brightYellow"], bg = self.__color_theme["background"],
            insertbackground = self.__color_theme ["brightRed"])

    def __import_color_theme(self):
        self.__local_path = askopenfilename(defaultextension = ".json", filetypes = [("All Files","*.*"),
                                                                    ("Color Theme", "*.json")])
        if self.__local_path == "":
            # no file to open
            self.__file = None
        else:
            # try to open
            #self.__root.title(os.path.basename(self.__local_path) + " - PyNotepad")
            #self.__thisTextArea.delete(1.0,END)
            file  = open(self.__local_path, "r")
            data = file.read()
            self.__color_theme = json.loads(data)
            file.close()
            self.__thisTextArea.config(fg = self.__color_theme["brightYellow"],
            bg = self.__color_theme["background"],
            insertbackground = self.__color_theme["brightRed"])

            self.__thisOutputWindow.config(fg = self.__color_theme["brightYellow"],
            bg = self.__color_theme["background"],
            insertbackground = self.__color_theme ["brightRed"])


    def __cut(self):
        self.__thisTextArea.event_generate("<<Cut>>")

    def __copy(self):
        self.__thisTextArea.event_generate("<<Copy>>")
    
    def __paste(self):
        self.__thisTextArea.event_generate("<<Paste>>")

    def runApp(self):
        self.__root.mainloop()

# run app

notepad = Notepad(width = 600, height = 400)
notepad.runApp()

