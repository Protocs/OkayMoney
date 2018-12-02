import sys

from PyQt5.QtWidgets import QApplication, QStyleFactory

from okaymoney.ui.login import LoginWindow

# Класс окна, появляющегося при запуске программы.
FIRST_WINDOW = LoginWindow

# Стиль приложения
STYLE = 'Fusion'

app = QApplication(sys.argv)

st = QStyleFactory.create(STYLE)
app.setStyle(st)

w = FIRST_WINDOW()
w.show()
exit(app.exec())
