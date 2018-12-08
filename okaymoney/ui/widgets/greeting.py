from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsScene
from PyQt5.Qt import QByteArray

from ...util import shorten
from ...user_save_load import load
from ..main import MainWindow
from .ui_widget import UIWidget


class GreetingWidget(UIWidget):
    """Виджет, содержащий сообщение приветствия.

    *Файл интерфейса:* ``ui/widgets/greeting.ui``
    """

    ui_path = 'ui/widgets/greeting.ui'

