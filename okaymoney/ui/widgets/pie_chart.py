import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5.QtWidgets import QWidget, QVBoxLayout


class PieChart:
    """Круговая диаграмма, отрисовывающаяся на выбранном виджете."""

    def __init__(self, widget):
        super().__init__()

        figure, self.axes = plt.subplots()
        self.axes.axis('equal')  # Фиксируем пропорции, чтобы рисовался круг, а не овал

        self.canvas = FigureCanvasQTAgg(figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        widget.setLayout(layout)

    def update_chart(self, data):
        """Создает или обновляет диаграмму."""
        labels = [d[0] + '\n' + str(d[1]) + ' ₽' for d in data]
        values = [d[1] for d in data]
        explode = [0.01 for _ in range(len(data))]

        self.axes.pie(values, labels=labels, explode=explode, startangle=90, labeldistance=0.5)
        self.canvas.draw()


if __name__ == '__main__':
    # Пример использования

    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = QWidget()
    pc = PieChart(w)
    plt.title('Test')
    pc.update_chart([('Покупки', 100), ('Зарплата', 200)])
    w.show()
    exit(app.exec())
