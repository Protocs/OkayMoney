import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from ...util import INCOME, SPEND

BACKGROUND_GRAY = str(55 / 255)


class PieChart:
    """Круговая диаграмма, отрисовывающаяся на выбранном виджете."""

    def __init__(self, widget, checked_accounts):
        super().__init__()

        self.titles = {INCOME: 'Доходы', SPEND: 'Расходы'}

        self.checked_accounts = checked_accounts

        figure, self.axes = plt.subplots()
        self.axes.axis('equal')  # Фиксируем пропорции, чтобы рисовался круг, а не овал
        figure.set_facecolor(BACKGROUND_GRAY)

        self.canvas = FigureCanvasQTAgg(figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        widget.setLayout(layout)

        self._transaction_type = None
        self.transaction_type = INCOME

    @property
    def transaction_type(self):
        return self._transaction_type

    @transaction_type.setter
    def transaction_type(self, tp):
        self._transaction_type = tp

        title = plt.title(self.titles[self.transaction_type])
        plt.setp(title, color='w')
        self.update_chart([t.to_pie_data() for t in sum((a.transactions for a in self.checked_accounts), [])
                           if t.type == self.transaction_type])

    def update_chart(self, data):
        """Создает или обновляет диаграмму."""
        labels = [d[0] + '\n' + str(d[1]) + ' ₽' for d in data]
        values = [d[1] for d in data]
        explode = [0.01 for _ in range(len(data))]

        self.axes.pie(values, labels=labels, explode=explode, startangle=90, labeldistance=0.5)
        self.canvas.draw()
