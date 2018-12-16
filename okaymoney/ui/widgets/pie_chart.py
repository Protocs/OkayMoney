from decimal import Decimal
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5.QtWidgets import QVBoxLayout

from ...util import INCOME, SPEND, THEMES

# Цвет фона окна
BACKGROUND_GRAY = str(55 / 255)
# Максимальная ширина разреза между секторами диараммы
MAX_EXPLODE = 0.03
# Текст обучения, который отображается, если доходов или расходов нет.
NO_TRANSACTIONS = 'Нет {} за этот месяц'
# Текст обучения, который отображается, если нет счетов.
NO_ACCOUNTS = 'Нет счетов\n\nДобавьте первый счет с помощью кнопки "Добавить счёт"'
# Шрифт, установленный на диаграмме
FONT = fm.FontProperties(family="Calibri", size=10, style="normal")

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
        self.set_transaction_type(INCOME)

    # noinspection PyMethodMayBeStatic
    def set_title(self, text):
        title = plt.title(text)
        plt.setp(title, color='w', fontfamily="Calibri", fontsize=18)

    @property
    def transaction_type(self):
        return self._transaction_type

    def set_transaction_type(self, tp, month=None, year=None):
        self._transaction_type = tp
        self.upd(month, year)

    @property
    def checked_accounts(self):
        """Возвращает список счетов, статистику которых нужно показать."""
        return [account for account in self.user.accounts if account.checked]

    # noinspection PyMethodMayBeStatic
    def calculate_explodes(self, data):
        """Вычисляет ширину разрезов между секторами диаграмм, чтобы разрезы были примерно равны."""
        sum_ = float(sum(data))
        return [MAX_EXPLODE - MAX_EXPLODE * float(d) / sum_ for d in data]

    def show_tutorial(self, transaction_type, month, year):
        self.axes.pie(())
        now_month, now_year, now_day = datetime.now().month, datetime.now().year, datetime.now().day
        text = NO_ACCOUNTS if not self.user.accounts else \
            (NO_TRANSACTIONS.format('расходов' if transaction_type == SPEND else 'доходов')
             + ('\n\nДобавьте первую транзакцию с помощью кнопки "Новая транзакция".'
             if datetime(now_year, now_month, now_day) <= datetime(year, month, now_day) else ''))
        self.axes.text(0, 0, text, horizontalalignment='center', verticalalignment='center',
                    fontfamily="Calibri",fontsize=14, color='w')
        self.canvas.draw()

    def update_chart(self, data, month, year):
        """Создает или обновляет диаграмму."""
        self.axes.clear()
        self.set_title(self.titles[self.transaction_type])

        if not data:
            self.show_tutorial(self.transaction_type, month, year)
            return

        labels = [d[0] + '\n' + str(d[1]) + ' ₽' for d in data]
        values = [d[1] for d in data]
        explode = self.calculate_explodes(values)

        colors = THEMES[self.user.theme]
        patches, texts = self.axes.pie(values, explode=explode, startangle=90,
                                       colors=colors)

        self.axes.legend(patches, labels, loc='best', prop=FONT)
        self.canvas.draw()

    def upd(self, month=None, year=None):
        """Вызывает :meth:`update_chart` с подготовленными данными пользователя."""
        now = datetime.now()
        if month is None:
            month = now.month
        if year is None:
            year = now.year

        all_transactions = sum((a.transactions for a in self.checked_accounts), [])
        # Только доходы или расходы
        transactions_of_type = (t for t in all_transactions if t.type == self.transaction_type)
        # Транзакции указанного месяца
        transactions_of_month = (t for t in transactions_of_type
                                 if t.date.date().month() == month and t.date.date().year() == year)
        # Данные транзакций для диаграммы
        pie_data = (t.to_pie_data() for t in transactions_of_month)

        # Слитие транзакций по категориям в большие, по одной на категорию
        merged_pie_data = {}
        for category, delta in pie_data:
            merged_pie_data[category] = merged_pie_data.get(category, Decimal()) + delta

        self.update_chart(merged_pie_data.items(), month, year)
