import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import Controller

#######################################################################################

class homePage(QWidget):
    lenList = 10
    def __init__(self):
        super(homePage, self).__init__()
        loadUi('Ui/homepagestyle.ui', self)

        self.learnBtn.clicked.connect(self.learnAction)
        self.testBtn.clicked.connect(self.testAction)
        self.filterBtn.clicked.connect(self.filterAction)
        self.areaLabel = self.findChild(QLabel, "currentAreaLabel")
        self.catLabel = self.findChild(QLabel, "currentCategoryLabel")

##Initialisation des filtres
        filterPage().readFilter()
        filterPage().readAreaFilter()
        print('filters initialized')
        self.category = filterPage().readFilter()
        self.area = filterPage().readAreaFilter()
        print('filters have been read and stored')
        print(self.area)
        print(self.category)
        Controller.filterCategory(self.category, self.area)        # To get a new serie of 10 questions depending on category (random)
        print('New list created')

        self.areaLabel.setText(self.area)
        self.catLabel.setText(self.category)

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
        self.descriptionCard = self.findChild(QLabel, "descriptionCard")
        self.responseCard = self.findChild(QLabel, "responseCard")
        self.dateCard = self.findChild(QLabel, "dateLabel")
        self.userInput = self.findChild(QTextEdit, "userInput")

        self.previousBtn.clicked.connect(self.previousAction)
        self.nextBtn.clicked.connect(self.nextAction)

        self.__listIndex = 0
        self.lenList = 10

##Initialisation des filtres
        filterPage().readFilter()
        filterPage().readAreaFilter()
        self.category = filterPage().readFilter()
        self.area = filterPage().readAreaFilter()
        self.control = Controller.filterCategory(self.category, self.area)

        self.responseCard.clear()
        self.display_quest()

    def display_quest(self):
        if self.__listIndex < homePage.lenList:
            self.titleCard.setText(str(self.control.title[self.__listIndex]))
            self.dateCard.setText(str(self.control.date[self.__listIndex]))
            self.descriptionCard.setText(str(self.control.details[self.__listIndex]))

    @staticmethod
    def previousAction():
        #widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.setCurrentIndex(0)

    def nextAction(self):
        while self.__listIndex < homePage.lenList:

            if self.userInput.toPlainText() == "":  # Gestion d'exception
                self.responseCard.setText("Entrez une réponse svp")             ###Currently useless / TO FIX
                break

            elif self.userInput.toPlainText() == str(self.control.date[self.__listIndex]):
                self.responseCard.setText("CORRECT !")             ###Currently useless / TO FIX
                self.__listIndex += 1
                self.userInput.clear()
                self.display_quest()
                print('bonne réponse')
                break

            else:
                self.responseCard.setText("INCORRECT")             ###Currently useless / TO FIX
                self.userInput.clear()
                self.display_quest()
                break
        print(self.__listIndex)

        if self.__listIndex >= homePage.lenList:
            print('retour à l\'accueil')
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

##Initialisation des filtres
        filterPage().readFilter()
        filterPage().readAreaFilter()
        self.category = filterPage().readFilter()
        self.area = filterPage().readAreaFilter()
        self.control = Controller.filterCategory(self.category, self.area)

        self.display_quest()

    def display_quest(self):
        if self.__listIndex < homePage.lenList:
            self.titleCard.setText(str(self.control.title[self.__listIndex]))
            self.descriptionCard.setText("")

    @staticmethod
    def previousAction():
        #widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.setCurrentIndex(0)

    def nextAction(self):
        while self.__listIndex < homePage.lenList:

            if self.userInput.toPlainText() == "":                           #Exception
                self.titleCard.setText("Entrez une réponse svp")             ###Currently useless / TO FIX
                break

            elif self.userInput.toPlainText() == str(self.control.date[self.__listIndex]):
                self.titleCard.setText("CORRECT !")             ###Currently useless / TO FIX
                self.__listIndex += 1
                testPage.score += 1
                self.userInput.clear()
                self.display_quest()
                print('bonne réponse')
                break

            else:
                self.titleCard.setText("INCORRECT")             ###Currently useless / TO FIX
                self.__listIndex += 1
                self.userInput.clear()
                self.display_quest()
                print('mauvaise réponse')
                break

        print(self.__listIndex)

        if self.__listIndex >= homePage.lenList:  # return to homePage when serie end
            print('retour à l\'accueil')
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
        homepage = homePage()
        widget.addWidget(homepage)
        widget.setCurrentWidget(homepage)

    def display_score(self):
        print(testPage.score)
        self.scoreLabel.setText(str(testPage.score))

#######################################################################################

class filterPage(QWidget):
    currentFilter = ""
    currentAreaFilter = ""
    def __init__(self):
        super(filterPage, self).__init__()
        loadUi("Ui/filterpage.ui", self)

        self.validateBtn.clicked.connect(self.validateAction)

    def validateAction(self):
        filterPage.currentFilter = self.filtersList.currentText()
        filterPage.currentAreaFilter = self.areaFilter.currentText()

        homepage = homePage()
        widget.addWidget(homepage)
        widget.setCurrentWidget(homepage)

    def filterDefault(self):
        filterPage.currentFilter = "Toutes les catégories"
        filterPage.currentAreaFilter = "Toutes les aires géographiques"
        print('everything')

    def readFilter(self):             #avoid return of blank filter reading while calling method readFilter()
        if filterPage.currentFilter != "":
            print('returned')
            return filterPage.currentFilter
        elif filterPage.currentFilter == "":
            print('blank filter avoid')
            self.filterDefault()
        else:
            print('le filtre n\'a pas pu être chargé. type(currentFilter) is (None or Unknown)')

    def readAreaFilter(self):
        if filterPage.currentAreaFilter != "":
            print('area returned')
            return filterPage.currentAreaFilter
        elif filterPage.currentAreaFilter == "":
            print('blank area filter avoid')
            self.filterDefault()
        else:
            print('le filtre n\'a pas pu être chargé. type(currentAreaFilter) is (None or Unknown)')

#######################################################################################

app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()

Home = homePage()
widget.addWidget(Home)

widget.setMinimumWidth(1100)
widget.setMinimumHeight(600)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting...")
