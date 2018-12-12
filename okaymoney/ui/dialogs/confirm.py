from .ui_dialog import UIDialog


class ConfirmActionDialog(UIDialog):
    """Диалог подтверждения совершения какой-либо операции.

    *Файл интерфейса:* ``ui/dialogs/confirm_dialog.ui``
    """

    ui_path = 'ui/dialogs/confirm_dialog.ui'

    def __init__(self, msg):
        super().__init__()

        self.information.setText(msg)
        self.ok_btn.clicked.connect(self.confirm_action)
        self.cancel_btn.clicked.connect(self.close)

        self.confirm = False

    def confirm_action(self):
        self.confirm = True
        self.close()

    def exec(self):
        super().exec()
        return self.confirm