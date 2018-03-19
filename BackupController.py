import os, simplejson as json
from datetime import *
from hurry import filesize
import shutil
import win32api


class BackupController(object):

    programDataDir = os.path.join(os.getenv("APPDATA"), "BackupUtility")
    programDataPath = os.path.join(programDataDir, "ProgramData.json")

    def __init__(self, model):

        self.Model = model

        self.programData = getProgramData()

        print(self.programData)

    def addFile(self):

        filePath = self.Model.GUIOperation("choosefile")

        if not filePath is None:

            self.programData["files"].append(filePath)

            saveProgramData(self.programData)

            self.updateGUI()

    def removeFile(self):

        fileIndex = self.Model.GUIOperation("selectedfileindex")

        if not fileIndex is None:

            del self.programData["files"][fileIndex]

            saveProgramData(self.programData)

            self.updateGUI()

    def getFiles(self):

        return self.programData["files"]

    def startbackuup(self):

        backupDrive = self.getBackupDrive();

        if not backupDrive is None:

            self.backup(backupDrive)

            self.updateGUI()

    def updateGUI(self):

        self.Model.GUIOperation("updatefiles", files=self.programData["files"])

    def getBackupDrive(self, spaceneeded=None):

        if spaceneeded is None:

            spaceneeded = self.getFilesTotalSize()

        alldrives = win32api.GetLogicalDriveStrings().split("\x00")
        alldrives = alldrives[0:len(alldrives) - 1]

        validdrives_withinfo = []

        for d in alldrives:

            try:

                TotalSpaceInBytes, FreeSpaceInBytes = self.getDriveSize(d)

                validdrives_withinfo.insert(len(validdrives_withinfo), d + " (Total=" + filesize.size(TotalSpaceInBytes) + " Free=" + filesize.size(FreeSpaceInBytes) + ")")

            except:
                pass

        selectedDrive = self.Model.GUIOperation("selectoption", text="Select which drive to backup to\n" + filesize.size(spaceneeded, filesize.verbose) + " needed to backup files", options=validdrives_withinfo)

        if not selectedDrive == "":

            selectedDrive = selectedDrive[0:4]

            if (self.getDriveSize(selectedDrive)[1] > spaceneeded):

                return selectedDrive

            else:

                self.Model.GUIOperation("alertuser", text="Drive selected has insufficient free space.\nPlease selected a different drive you idiot")
                self.getBackupDrive(spaceneeded=spaceneeded)

        else:

            return None;

    def getDriveSize(self, driveName):

        space, bytesPerSect, freeClusters, totalClusters = win32api.GetDiskFreeSpace(driveName);

        return [space * bytesPerSect * totalClusters, space * bytesPerSect * freeClusters]

    def backup(self, backupDrive):

        backupDir = self.getBackupLocation(backupDrive);

        totalfilessize = self.getFilesTotalSize()

        self.Model.GUIOperation("openprogressbar", max_value=totalfilessize)

        for file in self.getFilesToBackup():

            for entry in scantree(file):

                currentfilesize = os.path.getsize(entry.path)

                backupfilepath = os.path.join(backupDir, entry.path[len(file)+1:])

                if os.path.isdir(entry.path):
                    os.makedirs(backupfilepath)

                else:
                    shutil.copy2(entry.path, backupfilepath)

                self.Model.GUIOperation("updateprogressbar", delta=currentfilesize)

        self.Model.GUIOperation("closeprogressbar")
        self.Model.GUIOperation("alertuser", text="Backup finnished")

    def getBackupLocation(self, backupDrive):

        backup_time = datetime.now().strftime("%H-%M-%S %m-%d-%y")

        backup_dir = backupDrive + "Backup " + backup_time

        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        return backup_dir;

    def getFilesToBackup(self):

        return self.programData["files"]

    def getFilesTotalSize(self):

        totalSizeBytes = 0

        for file in self.getFilesToBackup():

            for entry in scantree(file):

                totalSizeBytes += os.path.getsize(entry.path)

        return totalSizeBytes

def scantree(path):
    """Recursively yield DirEntry objects for given directory."""
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            yield entry
            yield from scantree(entry.path)
        else:
            yield entry

def getProgramData():

    if os.path.isfile(BackupController.programDataPath):

        try:

            programdatafile = open(BackupController.programDataPath, "r", encoding="utf=8")

            return json.load(programdatafile)

        except Exception:

             return json.loads('{ "files" : [] }')

    else:

        return json.loads('{ "files" : [] }')

def saveProgramData(programdata):

    if not os.path.exists(BackupController.programDataDir):

        os.makedirs(BackupController.programDataDir)

    programdatafile = open(BackupController.programDataPath, "w", encoding="utf-8")

    programdatafile.write(json.dumps(programdata, indent=4))
