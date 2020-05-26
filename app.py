import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets
import sys


# Add dish window - Window object name: Dialog
class Ui_Dialog(object):
    def setupDialog(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(793, 648)
        self.cancelAddDishButton = QtWidgets.QPushButton(Dialog)
        self.cancelAddDishButton.setGeometry(QtCore.QRect(620, 570, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.cancelAddDishButton.setFont(font)
        self.cancelAddDishButton.setObjectName("cancelAddDishButton")
        self.cancelAddDishButton.clicked.connect(Dialog.done)
        self.dishDescriptionTextview = QtWidgets.QLabel(Dialog)
        self.dishDescriptionTextview.setGeometry(QtCore.QRect(30, 180, 731, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.dishDescriptionTextview.setFont(font)
        self.dishDescriptionTextview.setObjectName("dishDescriptionTextview")
        self.dishTitleTextview = QtWidgets.QLabel(Dialog)
        self.dishTitleTextview.setGeometry(QtCore.QRect(30, 80, 731, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.dishTitleTextview.setFont(font)
        self.dishTitleTextview.setObjectName("dishTitleTextview")
        self.dishTitleTextedit = QtWidgets.QLineEdit(Dialog)
        self.dishTitleTextedit.setGeometry(QtCore.QRect(30, 120, 731, 31))
        self.dishTitleTextedit.setObjectName("dishTitleTextedit")
        self.saveAddDishButton = QtWidgets.QPushButton(Dialog)
        self.saveAddDishButton.setGeometry(QtCore.QRect(30, 570, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)

        self.saveAddDishButton.setFont(font)
        self.saveAddDishButton.setAutoFillBackground(False)
        self.saveAddDishButton.setStyleSheet("background-color:green;\n"
                                             "color:white")
        self.saveAddDishButton.setObjectName("saveAddDishButton")
        self.saveAddDishButton.clicked.connect(self.save_and_exit)
        self.saveAddDishButton.clicked.connect(Dialog.done)

        self.line = QtWidgets.QFrame(Dialog)
        self.line.setGeometry(QtCore.QRect(30, 160, 731, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.addNewDishWindowtitle = QtWidgets.QLabel(Dialog)
        self.addNewDishWindowtitle.setGeometry(QtCore.QRect(230, 30, 301, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.addNewDishWindowtitle.setFont(font)
        self.addNewDishWindowtitle.setAlignment(QtCore.Qt.AlignCenter)
        self.addNewDishWindowtitle.setObjectName("addNewDishWindowtitle")
        self.dishDescriptionTextedit = QtWidgets.QPlainTextEdit(Dialog)
        self.dishDescriptionTextedit.setGeometry(QtCore.QRect(30, 210, 731, 341))
        self.dishDescriptionTextedit.setObjectName("dishDescriptionTextedit")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Add Dish"))
        self.cancelAddDishButton.setText(_translate("Dialog", "Cancel"))
        self.dishDescriptionTextview.setText(_translate("Dialog", "Dish Description:"))
        self.dishTitleTextview.setText(_translate("Dialog", "Dish Title:"))
        self.saveAddDishButton.setText(_translate("Dialog", "Save"))
        self.addNewDishWindowtitle.setText(_translate("Dialog", "Add new dish"))

    def save_and_exit(self):
        dishname = self.dishTitleTextedit.text().title()
        dishdescription = self.dishDescriptionTextedit.toPlainText().title()

        # Insert new dish
        sqliteConn = sqlite3.connect('favourite_dishes.db')
        cursor = sqliteConn.cursor()
        query_select_dishes = "select * from dishes"
        cursor.execute(query_select_dishes)
        dishesRecords = cursor.fetchall()

        if (dishesRecords):
            values = '({}, {}, {})'.format((len(dishesRecords) + 1), dishname, dishdescription)
            query_insert_dish = "INSERT INTO dishes ('id','name','description') VALUES (?, ?, ?)"
            cursor.execute(query_insert_dish, [(len(dishesRecords) + 1), dishname, dishdescription])
        else:
            query_insert_dish = "INSERT INTO dishes ('id','name','description') VALUES (1,'"
            query_insert_dish += dishname
            query_insert_dish += "','"
            query_insert_dish += dishdescription
            query_insert_dish += "')"
            cursor.execute(query_insert_dish)

        sqliteConn.commit()
        print("New dish added")
        cursor.close()
        sqliteConn.close()
        #UiMainWindow.reload_mainWindow(self)


class UiMainWindow(object):
    sqliteConn = 0
    dishesRecords = 0
    dishesDisplayPostion = 0

    def load_data_database(self):
        self.sqliteConn = sqlite3.connect('favourite_dishes.db')
        cursor = self.sqliteConn.cursor()

        query_select_dishes = "select * from dishes"
        cursor.execute(query_select_dishes)
        self.dishesRecords = cursor.fetchall()

        cursor.close()
        self.sqliteConn.close()

        # Display first dish from loaded data
        if (self.dishesRecords):
            dishEntry = self.dishesRecords[0]
            self.dishTitleTextview.setText(str(dishEntry[1]))
            self.dishDescriptionTextview.setText(str(dishEntry[2]))
            self.dishesDisplayPostion = 1
            self.positionTextview.setText(str(self.dishesDisplayPostion) + "/" + str(len(self.dishesRecords)))

    # Displays the dish for the Number dishesDisplayPosition (Dishes index starting with 1)
    def show_dish_entry(self, dishId):
        if (self.dishesRecords):
            dishEntry = self.dishesRecords[dishId - 1]
            # dish titel
            self.dishTitleTextview.setText(dishEntry[1])
            # dish desc
            self.dishDescriptionTextview.setText(dishEntry[2])

            self.positionTextview.setText(str(dishEntry[0]) + " / " + str(len(self.dishesRecords)))

    def display_left_dish(self):
        if (self.dishesRecords):
            if (self.dishesDisplayPostion > 1):
                self.dishesDisplayPostion -= 1;
                UiMainWindow.show_dish_entry(self, self.dishesDisplayPostion)
            else:
                if(len(self.dishesRecords)!=0):
                    self.dishesDisplayPostion = len(self.dishesRecords)
                    UiMainWindow.show_dish_entry(self, self.dishesDisplayPostion)


    def display_right_dish(self):
        if (self.dishesRecords):
            if (self.dishesDisplayPostion < len(self.dishesRecords)):
                self.dishesDisplayPostion += 1;
                UiMainWindow.show_dish_entry(self, self.dishesDisplayPostion)
            else:
                if (len(self.dishesRecords) != 0):
                    self.dishesDisplayPostion = 1
                    UiMainWindow.show_dish_entry(self, self.dishesDisplayPostion)


    def setup_ui(self, MainWindow):
        # Load Main Window
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 682)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.programmTitle = QtWidgets.QLabel(self.centralwidget)
        self.programmTitle.setGeometry(QtCore.QRect(290, 10, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.programmTitle.setFont(font)
        self.programmTitle.setObjectName("programmTitle")
        self.addDishButton = QtWidgets.QPushButton(self.centralwidget)
        self.addDishButton.setGeometry(QtCore.QRect(20, 610, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.addDishButton.setFont(font)
        self.addDishButton.setObjectName("addDishButton")
        self.showRelatedDishesButton = QtWidgets.QPushButton(self.centralwidget)
        self.showRelatedDishesButton.setGeometry(QtCore.QRect(550, 610, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.showRelatedDishesButton.setFont(font)
        self.showRelatedDishesButton.setObjectName("showRelatedDishesButton")
        self.leftButton = QtWidgets.QPushButton(self.centralwidget)
        self.leftButton.setGeometry(QtCore.QRect(280, 530, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.leftButton.setFont(font)
        self.leftButton.setObjectName("leftButton")
        self.rightButton = QtWidgets.QPushButton(self.centralwidget)
        self.rightButton.setGeometry(QtCore.QRect(370, 530, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.rightButton.setFont(font)
        self.rightButton.setObjectName("rightButton")
        self.positionTextview = QtWidgets.QLabel(self.centralwidget)
        self.positionTextview.setGeometry(QtCore.QRect(270, 580, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.positionTextview.setFont(font)
        self.positionTextview.setAlignment(QtCore.Qt.AlignCenter)
        self.positionTextview.setObjectName("positionTextview")
        self.dishTitleTextview = QtWidgets.QLabel(self.centralwidget)
        self.dishTitleTextview.setGeometry(QtCore.QRect(30, 70, 731, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.dishTitleTextview.setFont(font)
        self.dishTitleTextview.setObjectName("dishTitleTextview")
        self.dishDescriptionTextview = QtWidgets.QLabel(self.centralwidget)
        self.dishDescriptionTextview.setGeometry(QtCore.QRect(30, 140, 731, 361))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.dishDescriptionTextview.setFont(font)
        self.dishDescriptionTextview.setObjectName("dishDescriptionTextview")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(30, 120, 731, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Functions
        self.addDishButton.clicked.connect(self.open_window_add_dishes)
        self.leftButton.clicked.connect(self.display_left_dish)
        self.rightButton.clicked.connect(self.display_right_dish)

        # Load database
        try:
            UiMainWindow.load_data_database(self)

        except sqlite3.Error as error:
            print("Error sqlite db: ", error)
            sqliteConn = self.sqliteConn
            # Create new database and tables
            query_create_table = ''' CREATE TABLE dishes (
                                id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL,
                                description TEXT
                                );
                                ''';

            cursor = sqliteConn.cursor();
            cursor.execute(query_create_table)
            sqliteConn.commit()
            print("New Database created")
            cursor.close()

        finally:
            if (self.sqliteConn):
                self.sqliteConn.close()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "My Favourite Dishes"))
        self.programmTitle.setText(_translate("MainWindow", "My Favourite Dishes"))
        self.addDishButton.setText(_translate("MainWindow", "Add Dish"))
        self.showRelatedDishesButton.setText(_translate("MainWindow", "Show Related Dishes"))
        self.leftButton.setText(_translate("MainWindow", "<"))
        self.rightButton.setText(_translate("MainWindow", ">"))
        self.positionTextview.setText(_translate("MainWindow", "X / X"))
        self.dishTitleTextview.setText(_translate("MainWindow", "No dish created"))
        self.dishDescriptionTextview.setText(
            _translate("MainWindow", "Please create a dish by clicking on the button \"Add Dish\""))

    def open_window_add_dishes(self):
        Dialog = QtWidgets.QDialog()
        ui2 = Ui_Dialog()
        ui2.setupDialog(Dialog)

        Dialog.exec_()
        UiMainWindow.load_data_database(self)
        UiMainWindow.show_dish_entry(self, 1)

        # sys.exit(app.exec_())



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UiMainWindow()
    ui.setup_ui(MainWindow)
    MainWindow.show()


    sys.exit(app.exec_())
