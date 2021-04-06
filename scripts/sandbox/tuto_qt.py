import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QFile
from ui_tuto import Ui_Form


class MyApp(QWidget):
    def __init__(self):
        super().__init__(parent=None)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle("My App")
        self.connectSignalsSlots()

    def connectSignalsSlots(self):
        self.ui.button.clicked.connect(self.hello)

    def hello(self):
        input_text = self.ui.input.toPlainText()
        self.ui.output.setText(f'Hello {input_text}')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_app = MyApp()
    my_app.show()

    sys.exit(app.exec_())
