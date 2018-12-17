import sys

from PyQt5.QtWidgets import QApplication, QStyleFactory

from okaymoney.ui.login import LoginWindow
from okaymoney.util import find_data_file

# Класс окна, появляющегося при запуске программы.
FIRST_WINDOW = LoginWindow

# Стиль приложения
STYLE = 'Fusion'

app = QApplication(sys.argv)

st = QStyleFactory.create(STYLE)
app.setStyle(st)

# Установка листа стилей (Style Sheet)
with open(find_data_file('ui/app.qss')) as ss:
    app.setStyleSheet(ss.read())

w = FIRST_WINDOW()
w.show()
sys.exit(app.exec())
