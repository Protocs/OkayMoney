import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5.QtWidgets import QVBoxLayout

from ...util import INCOME, SPEND

BACKGROUND_GRAY = str(55 / 255)


class PieChart:
    """Круговая диаграмма, отрисовывающаяся на выбранном виджете."""

    COLORS = ['#eb3b5a', '#4b7bec', '#a55eea', '#fed330', '#20bf6b', '#fa8231', '#0fb9b1']

    def __init__(self, widget, user):
        super().__init__()

        self.user = user

        self.titles = {INCOME: 'Доходы', SPEND: 'Расходы'}

        figure, self.axes = plt.subplots()
        self.axes.axis('equal')  # Фиксируем пропорции, чтобы рисовался круг, а не овал
        figure.set_facecolor(BACKGROUND_GRAY)

        self.canvas = FigureCanvasQTAgg(figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        widget.setLayout(layout)

        self._transaction_type = None
        self.transaction_type = INCOME

    # noinspection PyMethodMayBeStatic
    def set_title(self, text):
        title = plt.title(text)
        plt.setp(title, color='w')

    @property
    def transaction_type(self):
        return self._transaction_type

    @transaction_type.setter
    def transaction_type(self, tp):
        self._transaction_type = tp
        self.upd()

    @property
    def checked_accounts(self):
        return [account for account in self.user.accounts if account.checked]

    def update_chart(self, data):
        """Создает или обновляет диаграмму."""
        labels = [d[0] + '\n' + str(d[1]) + ' ₽' for d in data]
        values = [d[1] for d in data]
        explode = [0.01 for _ in range(len(data))]

        self.axes.clear()
        self.set_title(self.titles[self.transaction_type])
        patches, texts = self.axes.pie(values, explode=explode, startangle=90, colors=self.COLORS)
        self.axes.legend(patches, labels, loc='best', fontsize=8)
        self.canvas.draw()

    def upd(self):
        self.update_chart([t.to_pie_data() for t in sum((a.transactions for a in self.checked_accounts), [])
                           if t.type == self.transaction_type])
