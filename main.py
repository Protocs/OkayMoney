import sys

from PyQt5.QtWidgets import QApplication

from okaymoney.login import LoginWindow

# Класс окна, появляющегося при запуске программы.
FIRST_WINDOW = LoginWindow

app = QApplication(sys.argv)
w = FIRST_WINDOW()
w.show()
exit(app.exec())
