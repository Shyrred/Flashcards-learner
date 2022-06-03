import sys
import time  # in seconds
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import importlib
import Controller as c

#######################################################################################

class homePage(QWidget):
    def __init__(self):
        super(homePage, self).__init__()
        loadUi('Ui/homepagestyle.ui', self)

        self.learnBtn.clicked.connect(self.learnAction)
        self.testBtn.clicked.connect(self.testAction)
        self.filterBtn.clicked.connect(self.filterAction)

    def delay(self):
        time.sleep(1.0)

    def learnAction(self):
        learnpage = learnPage()
        widget.addWidget(learnpage)
        widget.setCurrentWidget(learnpage)

    def testAction(self):
        testpage = testPage()
        widget.addWidget(testpage)
        widget.setCurrentWidget(testpage)

    def filterAction(self):
        filterpage = filterPage()
        widget.addWidget(filterpage)
        widget.setCurrentWidget(filterpage)

#######################################################################################

class learnPage(QWidget):
    def __init__(self):
        super(learnPage, self).__init__()
        loadUi('Ui/learnpage.ui', self)

        self.titleCard = self.findChild(QLabel, "titleCard")
        self.userInput = self.findChild(QTextEdit, "userInput")

        self.previousBtn.clicked.connect(self.previousAction)
        self.nextBtn.clicked.connect(self.nextAction)

        self.__listIndex = 0
        self.lenList = 10
        self.display_quest()

    def display_quest(self):
        if self.__listIndex < self.lenList:
            self.titleCard.setText(str(c.fcTitleSessionList[self.__listIndex]))
            self.descriptionCard.setText("")

    @staticmethod
    def previousAction():
        widget.setCurrentIndex(widget.currentIndex() - 1)
        #widget.setCurrentIndex(0)

    def nextAction(self):
        while self.__listIndex < self.lenList:

            if self.userInput.toPlainText() == "":  # Gestion d'exception
                self.titleCard.setText("Entrez une réponse svp")
                break

            elif self.userInput.toPlainText() == str(c.fcDateSessionList[self.__listIndex]):
                self.titleCard.setText("CORRECT !")
                self.__listIndex += 1
                self.display_quest()
                print('bonne réponse')
                break

            else:
                self.titleCard.setText("INCORRECT")
                self.__listIndex += 1
                self.display_quest()
                break
        print(self.__listIndex)

        if self.__listIndex >= self.lenList:
            print('retour à l\'accueil')
            importlib.reload(c)  # To get a new serie of 10 questions (random)
            homepage = homePage()
            widget.addWidget(homepage)
            widget.setCurrentWidget(homepage)


#######################################################################################

class testPage(QWidget):

    score = 0                   #class attribute to be used in other classes (scorePage)

    def __init__(self):
        super(testPage, self).__init__()
        loadUi('Ui/testpage.ui', self)

        self.titleCard = self.findChild(QLabel, "titleCard")
        self.userInput = self.findChild(QTextEdit, "userInput")

        self.previousBtn.clicked.connect(self.previousAction)
        self.nextBtn.clicked.connect(self.nextAction)

        self.__listIndex = 0
        self.lenList = 10
        self.display_quest()

    def display_quest(self):
        if self.__listIndex < self.lenList:
            self.titleCard.setText(str(c.fcTitleSessionList[self.__listIndex]))
            self.descriptionCard.setText("")

    @staticmethod
    def previousAction():
        widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.setCurrentIndex(0)

    def nextAction(self):
        while self.__listIndex < self.lenList:

            if self.userInput.toPlainText() == "":                  #Exception
                self.titleCard.setText("Entrez une réponse svp")
                break

            elif self.userInput.toPlainText() == str(c.fcDateSessionList[self.__listIndex]):
                self.titleCard.setText("CORRECT !")

                self.__listIndex += 1
                testPage.score = testPage.score+1

                self.display_quest()
                print('bonne réponse')
                break

            else:
                self.titleCard.setText("INCORRECT")
                self.__listIndex += 1
                self.display_quest()
                print('mauvaise réponse')
                break

        print(self.__listIndex)

        if self.__listIndex >= self.lenList:  # return to homePage when serie end
            print('retour à l\'accueil')
            print(str(testPage.score))
            importlib.reload(c)  # To get a new serie of 10 questions (random)
            scorepage = scorePage()
            widget.addWidget(scorepage)
            widget.setCurrentWidget(scorepage)

#######################################################################################

class scorePage(QWidget):
    def __init__(self):
        super(scorePage, self).__init__()
        loadUi('Ui/scorepage.ui', self)

        self.scoreLabel = self.findChild(QLabel, "scoreLabel")
        self.homeBtn.clicked.connect(self.homeAction)

        self.display_score()

    def homeAction(self):
        importlib.reload(c)
        homepage = homePage()
        widget.addWidget(homepage)
        widget.setCurrentWidget(homepage)

    def display_score(self):
        print(testPage.score)
        self.scoreLabel.setText(str(testPage.score))

#######################################################################################

class filterPage(QWidget):
    int(index)
    def __init__(self):
        super(filterPage, self).__init__()
        loadUi("Ui/filterpage.ui", self)

        self.validateBtn.clicked.connect(self.readFilter)

    def validateAction(self):
        homepage = homePage()
        widget.addWidget(homepage)
        widget.setCurrentWidget(homepage)

    def readFilter(self):
        index = self.filtersList.findIndex()
        self.validateAction()


#######################################################################################

app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()

Home = homePage()
widget.addWidget(Home)

widget.setFixedWidth(1100)
widget.setFixedHeight(600)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting...")






import xlrd3
from random import *

document = xlrd3.open_workbook("Flashcards.xlsx")
feuille_1 = document.sheet_by_index(0) #va chercher la premiere feuille
#feuille_1 = document.sheet_by_name('feuille_1') #recherche par nom

print("Nombre de feuilles: "+str(document.nsheets))
print("Noms des feuilles: "+str(document.sheet_names()))

print("Nombre de lignes: "+str(feuille_1.nrows))
print("Nombre de colonnes: "+str(feuille_1.ncols))

cols = feuille_1.ncols
rows = feuille_1.nrows

i = 0
fcTitleSessionList = []
fcDateSessionList = []
fcCatSessionList = []

while i < 10:
    flashcardId = randint(1,rows)
    fcTitleSessionList += [feuille_1.cell_value(rowx=flashcardId, colx=0)]
    fcDateSessionList += [feuille_1.cell_value(rowx=flashcardId, colx=1)]
    fcCatSessionList += [feuille_1.cell_value(rowx=flashcardId, colx=2)]
    i += 1

#if category === "Evenement":


print(fcTitleSessionList,"\n")
print(fcDateSessionList,"\n")
print(fcCatSessionList,"\n")
