import sqlite3
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QWidget
from mainUI import Ui_MainWindow
from addEditCoffeeForm import Ui_Form


class AddEdit(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.update_result)
        self.saveButton.clicked.connect(self.save_results)
        self.set_row.clicked.connect(self.new)

    def update_result(self):
        self.con = sqlite3.connect("data/coffee.sqlite")
        cur = self.con.cursor()
        result = cur.execute(f"SELECT * FROM info WHERE {self.textEdit.toPlainText()}").fetchall()
        self.con.close()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))


    def save_results(self):
        msg = QMessageBox(self)
        msg.setIcon(msg.icon().Question)
        msg.setStandardButtons(msg.StandardButton.Yes | msg.StandardButton.No)
        row = self.tableWidget.currentRow()
        msg.setInformativeText(f'Действительно изменить элементы с индексом {self.tableWidget.item(row, 0).text()}?')
        msg.show()
        res = msg.exec()
        if res == msg.StandardButton.Yes:
            self.con = sqlite3.connect("data/coffee.sqlite")
            cur = self.con.cursor()
            cur.execute(f"DELETE FROM info WHERE id = {self.tableWidget.item(row, 0).text()}")

            values = [self.tableWidget.item(row, i).text() for i in range(self.tableWidget.columnCount())]
            cur.execute("""INSERT INTO info VALUES (?, ?, ?, ?, ?, ?, ?)""", values)
            self.con.commit()
            self.con.close()

    def new(self):
        self.con = sqlite3.connect("data/coffee.sqlite")
        cur = self.con.cursor()
        cur.execute("""INSERT INTO info ('Название_сорта', 'Степень_обжарки', 'Молотый_или_в_зернах', 'Описание_вкуса', 'Цена', 'Объем_упаковки') VALUES (?, ?, ?, ?, ?, ?)""", (self.lineEdit.text(),
                                                                          self.lineEdit_2.text(), self.lineEdit_3.text(),
                                                                          self.lineEdit_4.text(), self.lineEdit_5.text(),
                                                                          self.lineEdit_6.text()))
        self.con.commit()
        self.con.close()



class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.create1.clicked.connect(self.click)
        self.refactor.clicked.connect(self.click)
        self.update.clicked.connect(self.update_result)
        self.update_result()

    def update_result(self):
        self.con = sqlite3.connect("data/coffee.sqlite")
        cur = self.con.cursor()
        result = cur.execute(f"SELECT * FROM info").fetchall()
        self.con.close()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def click(self):
        self.form = AddEdit()
        self.form.show()



    def except_hook(cls, exception, traceback):
        sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    sys.excepthook = ex.except_hook
    ex.show()
    sys.exit(app.exec())