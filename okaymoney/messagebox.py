"""Утилиты для быстрого создания окон сообщений."""

from PyQt5.QtWidgets import QMessageBox


def error(msg, parent=None):
    """Показывает окно с сообщением об ошибке ``msg`` над окном/виджетом ``parent``."""
    box = QMessageBox(parent)
    box.setText(msg)
    box.setIcon(QMessageBox.Critical)
    box.exec()
