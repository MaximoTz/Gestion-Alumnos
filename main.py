import sys
from PyQt5 import QtWidgets
from Vista.login import Login

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Login()
    app.exec()

# Ya no se toca este programa
# ahi queda su programación