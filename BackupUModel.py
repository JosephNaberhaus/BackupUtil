from BackupController import BackupController
from BackupGUI import BackupGUI


class BackupModel(object):
    def __init__(self):

        self.controller = BackupController(self)
        self.gui = BackupGUI(self)

        self.GUIInteraction("update")

        self.gui.Window.mainloop()

    def GUIInteraction(self, name):

        print(name)

        if name == "addfile":

            self.controller.addFile()

        elif name == "removefile":

            self.controller.removeFile()

        elif name == "startbackup":

            self.controller.startbackuup()

        elif name == "update":

            self.controller.updateGUI()

        else:

            print("Unkown GUI interaction: " + name)

    def GUIOperation(self, name, **req_attr):

        if name == "selectedfileindex":

            return self.gui.getSelectedFileIndex()

        elif name == "choosefile":

            return self.gui.chooseFile()

        elif name == "selectoption":

            return self.gui.selectOption(**req_attr)

        elif name == "alertuser":

            return self.gui.alert(**req_attr)

        elif name == "updatefiles":

            return self.gui.updateFiles(**req_attr)

        elif name == "openprogressbar":

            self.gui.displayProgressBar(req_attr["max_value"])

        elif name == "updateprogressbar":

            self.gui.updateProgressBar(req_attr["delta"])

        elif (name == "closeprogressbar"):

            self.gui.closeProgressBar()

        else:

            print("Unkown model GUI opertation: " + name)