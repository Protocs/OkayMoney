import matplotlib.pyplot as plt

from .ui_window import UIWindow
from .widgets.pie_chart import PieChart


class MainWindow(UIWindow):
    """Основное окно приложения.

    *Файл интерфейса:* ``ui/main.ui``
    """

    ui_path = 'ui/main.ui'

    def __init__(self, user):
        super().__init__()

        self.user = user

        pie_chart = PieChart(self.pie_place)
        title = plt.title('Test')
        plt.setp(title, color='w')
        pie_chart.update_chart([('Покупки', 100), ('Зарплата', 200)])
