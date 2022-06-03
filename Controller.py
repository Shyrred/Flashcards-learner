import xlrd3
from random import *

document = xlrd3.open_workbook("Flashcards.xlsx")
feuille_1 = document.sheet_by_index(0)  #search in first page
#feuille_1 = document.sheet_by_name('feuille_1') #search in file by name

print("Nombre de feuilles: " + str(document.nsheets))
print("Noms des feuilles: " + str(document.sheet_names()))

print("Nombre de lignes: " + str(feuille_1.nrows))
print("Nombre de colonnes: " + str(feuille_1.ncols))

cols = feuille_1.ncols
rows = feuille_1.nrows

class returnList():
    def __init__(self, title, date, area, category, details):
        self.title = title
        self.date = date
        self.area = area
        self.category = category
        self.details = details

        print(title, "\n\n", date, "\n\n", area, "\n\n", category, "\n\n", details, "\n\n")         #print in console

def filterCategory(category, area):
    fcTitleSessionList, fcDateSessionList, fcAreaSessionList, fcCatSessionList, fcDetailSessionList = [], [], [], [], []
    index = 0

    while index < 10:
        flashcardId = randint(1, rows-1)
        areaCellValue = (feuille_1.cell_value(rowx=flashcardId, colx=2))
        catCellValue = (feuille_1.cell_value(rowx=flashcardId, colx=3))

        if (category == str(catCellValue) and area == str(areaCellValue)):
            fcTitleSessionList += [feuille_1.cell_value(rowx=flashcardId, colx=0)]
            fcDateSessionList += [feuille_1.cell_value(rowx=flashcardId, colx=1)]
            fcAreaSessionList += [feuille_1.cell_value(rowx=flashcardId, colx=2)]
            fcCatSessionList += [feuille_1.cell_value(rowx=flashcardId, colx=3)]
            fcDetailSessionList += [feuille_1.cell_value(rowx=flashcardId, colx=4)]
            index += 1

        elif (category == 'Toutes les catégories' or area == 'Toutes les aires géographiques') and (category == str(catCellValue) or area == str(areaCellValue)):
            fcTitleSessionList += [feuille_1.cell_value(rowx=flashcardId, colx=0)]
            fcDateSessionList += [feuille_1.cell_value(rowx=flashcardId, colx=1)]
            fcAreaSessionList += [feuille_1.cell_value(rowx=flashcardId, colx=2)]
            fcCatSessionList += [feuille_1.cell_value(rowx=flashcardId, colx=3)]
            fcDetailSessionList += [feuille_1.cell_value(rowx=flashcardId, colx=4)]
            index += 1

        elif (category == 'Toutes les catégories' and area == 'Toutes les aires géographiques'):
            fcTitleSessionList += [feuille_1.cell_value(rowx=flashcardId, colx=0)]
            fcDateSessionList += [feuille_1.cell_value(rowx=flashcardId, colx=1)]
            fcAreaSessionList += [feuille_1.cell_value(rowx=flashcardId, colx=2)]
            fcCatSessionList += [feuille_1.cell_value(rowx=flashcardId, colx=3)]
            fcDetailSessionList += [feuille_1.cell_value(rowx=flashcardId, colx=4)]
            index += 1

        else:
            #print(category, [feuille_1.cell_value(rowx=flashcardId, colx=3)])
            print('Unable to sort such a list, please select a valid category, or check the file .xlsx for spelling errors')
            pass

    response = returnList(fcTitleSessionList, fcDateSessionList, fcAreaSessionList, fcCatSessionList, fcDetailSessionList)
    return response

