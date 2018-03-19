from threading import Thread
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

class BackupGUI(object):

    def __init__(self, model):

        self.Model = model

        self.Window = Tk()
        self.Window.wm_title("Backup Utility")
        self.Window.wm_geometry("600x600")

        Grid.rowconfigure(self.Window, 0, weight=1)
        Grid.columnconfigure(self.Window, 0, weight=1)

        self.GUIFrame = Frame(self.Window)
        self.GUIFrame.grid(row=0, column=0, sticky=N + S + E + W, padx=3)

        self.FileList = Listbox(self.GUIFrame)
        self.FileList.grid(row=0, column=0, columnspan=2, sticky=N + S + E + W)

        self.AddFile = Button(self.GUIFrame, text="Add File", command=self.addFilePressed)
        self.AddFile.grid(row=1, column=0, sticky=N + S + E + W, padx=3, pady=3)

        self.RemoveFile = Button(self.GUIFrame, text="Remove File", command=self.removeFilePressed)
        self.RemoveFile.grid(row=1, column=1, sticky=N + S + E + W, padx=3, pady=3)

        self.StartBackup = Button(self.GUIFrame, text="Start Backup", command=self.startBackupPressed)
        self.StartBackup.grid(row=2, column=0, columnspan=2, sticky=N + S+ E + W, padx=3, pady=3)

        Grid.rowconfigure(self.GUIFrame, 0, weight=20)
        Grid.rowconfigure(self.GUIFrame, 1, weight=1)
        Grid.rowconfigure(self.GUIFrame, 2, weight=1)

        Grid.columnconfigure(self.GUIFrame, 0, weight=1)
        Grid.columnconfigure(self.GUIFrame, 1, weight=1)

        self.progressBarWindow = None;
        self.progressBar = None;

    def addFilePressed(self):

        self.Model.GUIInteraction("addfile")

    def removeFilePressed(self):

        self.Model.GUIInteraction("removefile")

    def startBackupPressed(self):

        self.Model.GUIInteraction("startbackup")

    def updateFiles(self, files):

        self.FileList.delete(0, END)

        self.FileList.insert(END, *files)

    def getSelectedFileIndex(self):

        return self.FileList.curselection()[0]

    def chooseFile(self):

        return filedialog.askdirectory()

    def selectOption(self, text="", options=[]):

        return DropdownSelectionDialog(self.Window, options, text).getSelected()

    def alert(self, text=""):

        return messagebox.showerror(title="Backup Util Warning", message=text)

    def displayProgressBar(self, max_value):

        self.progressBarWindow = Toplevel(self.Window, takefocus=True)

        self.progressBar = ttk.Progressbar(self.progressBarWindow, mode="determinate", orient=HORIZONTAL, length=200, maximum=max_value)
        self.progressBar.pack()
        self.progressBarWindow.update()

    def updateProgressBar(self, delta):

        assert(self.progressBar is not None)

        self.progressBar.step(delta)
        self.progressBarWindow.update()

    def closeProgressBar(self):

        self.progressBarWindow.destroy()
        self.progressBar = None
        self.progressBarWindow = None

class DropdownSelectionDialog(object):

    def __init__(self, parent, optionslist, text=""):

        self.Top = Toplevel(parent, takefocus=True)
        self.Top.protocol("WM_DELETE_WINDOW", self.windowExited)

        self.UserMessage = Label(self.Top, text=text)
        self.UserMessage.grid(row=0, column=0, columnspan=2, sticky=N + S + E +W)

        self.selection = StringVar(self.Top)
        self.selection.set(optionslist[0])

        self.OptionDropdown = OptionMenu(self.Top, self.selection, *optionslist)
        self.OptionDropdown.grid(row=1, column=0, columnspan=2, sticky=N + S + E + W)

        self.CancelButton = Button(self.Top, text="Cancel", command=self.cancelPressed)
        self.CancelButton.grid(row=2, column=0, sticky=N + S + E +W)

        self.OkButton = Button(self.Top, text="Ok", command=self.okPressed)
        self.OkButton.grid(row=2, column=1, sticky=N + S + E + W)

        self.OkButtonClose = False

        self.Top.mainloop()

    def getSelected(self):

        if self.OkButtonClose:

            return self.selection.get()

        else:

            return "";

    def okPressed(self):

        self.OkButtonClose = True;

        self.Top.quit()
        self.Top.destroy()

    def cancelPressed(self):

        self.Top.quit()
        self.Top.destroy()

    def windowExited(self):

        self.Top.quit()
        self.Top.destroy()