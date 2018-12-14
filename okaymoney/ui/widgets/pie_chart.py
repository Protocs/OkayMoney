from decimal import Decimal

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5.QtWidgets import QVBoxLayout

from ...util import INCOME, SPEND

# Цвет фона окна
BACKGROUND_GRAY = str(55 / 255)
# Цвета диграммы доходов
INCOME_COLORS = ['#EA005E', '#3498db', '#8e44ad', '#f39c12', '#16a085', '#2ecc71', '#2c3e50']
# Цвета диаграммы расходов
SPEND_COLORS = ['#EA005E', '#19B5FE', '#a0e300', '#ff5736', '#0078D7', '#f78fb3', '#db0dca']
# Максимальная ширина разреза между секторами диараммы
MAX_EXPLODE = 0.03


class PieChart:
    """Круговая диаграмма, отрисовывающаяся на выбранном виджете."""

    def __init__(self, widget, user):
        super().__init__()

        self.user = user

        # Заголовки, соответствующие режимам отображения
        self.titles = {INCOME: 'Доходы', SPEND: 'Расходы'}

        figure, self.axes = plt.subplots()
        self.axes.axis('equal')  # Фиксируем пропорции, чтобы рисовался круг, а не овал
        figure.set_facecolor(BACKGROUND_GRAY)

        # Холст для диаграммы, добавление его на виджет
        self.canvas = FigureCanvasQTAgg(figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        widget.setLayout(layout)

        # Что отображать - доходы или расходы
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
        """Возвращает список счетов, статистику которых нужно показать."""
        return [account for account in self.user.accounts if account.checked]

    # noinspection PyMethodMayBeStatic
    def calculate_explodes(self, data):
        """Вычисляет ширину разрезов между секторами диаграмм, чтобы разрезы были примерно равны."""
        sum_ = float(sum(data))
        return [MAX_EXPLODE - MAX_EXPLODE * float(d) / sum_ for d in data]

    def update_chart(self, data):
        """Создает или обновляет диаграмму."""
        labels = [d[0] + '\n' + str(d[1]) + ' ₽' for d in data]
        values = [d[1] for d in data]
        explode = self.calculate_explodes(values)

        self.axes.clear()
        self.set_title(self.titles[self.transaction_type])

        colors = INCOME_COLORS if self.transaction_type == INCOME else SPEND_COLORS
        patches, texts = self.axes.pie(values, explode=explode, startangle=90,
                                       colors=colors)

        self.axes.legend(patches, labels, loc='best', fontsize=8)
        self.canvas.draw()

    def upd(self):
        """Вызывает :meth:`update_chart` с подготовленными данными пользователя."""
        all_transactions = sum((a.transactions for a in self.checked_accounts), [])
        # Только доходы или расходы
        transactions_of_type = (t for t in all_transactions if t.type == self.transaction_type)
        # Данные транзакций для диаграммы
        pie_data = (t.to_pie_data() for t in transactions_of_type)

        # Слитие транзакций по категориям в большие, по одной на категорию
        merged_pie_data = {}
        for category, delta in pie_data:
            merged_pie_data[category] = merged_pie_data.get(category, Decimal()) + delta

        self.update_chart(merged_pie_data.items())
