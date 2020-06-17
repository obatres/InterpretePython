from PyQt5.QtWidgets import  QInputDialog
def getInteger(self):
    i, okPressed = QInputDialog.getInt(self, "Get integer","Percentage:", 28, 0, 100, 1)
    if okPressed:
        print(i)
