"""Утилиты для быстрого создания окон сообщений."""

from PyQt5.QtWidgets import QMessageBox

STYLESHEET = "* { color: white; background-color: rgb(55, 55, 55); }"


def error(msg, parent=None):
    """Показывает окно с сообщением об ошибке ``msg`` над окном/виджетом ``parent``."""
    box = QMessageBox(parent)
    box.setText(msg)
    box.setWindowTitle('Ошибка')
    box.setIcon(QMessageBox.Critical)
    box.setStyleSheet(STYLESHEET)
    box.exec()


def warning(msg, parent=None):
    """Показывает окно с предупреждением ``msg`` над окном/виджетом ``parent``."""
    box = QMessageBox(parent)
    box.setText(msg)
    box.setWindowTitle('Внимание')
    box.setIcon(QMessageBox.Warning)
    box.setStyleSheet(STYLESHEET)
    box.exec()


def information(msg, parent=None):
    """Показывает окно с информацией ``msg`` над окном/виджетом ``parent``."""
    box = QMessageBox(parent)
    box.setText(msg)
    box.setWindowTitle('Внимание!')
    box.setIcon(QMessageBox.Information)
    box.setStyleSheet(STYLESHEET)
    box.exec()
