import sys
from PySide6.QtWidgets import QApplication, QWidget, QDialog, QVBoxLayout, QLabel, QPushButton, QComboBox
from googletrans import Translator
import json
import os

from ui_form import Ui_Widget

class InfoWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Info")

        layout = QVBoxLayout()

        info_text = """
        Verba Translate - Fast translation!
        This program uses the free MIT license and the PySide6 and googletrans libraries.
        Github: https://github.com/blbjn/verbatranslate
        """

        label = QLabel(info_text)
        layout.addWidget(label)

        close_button = QPushButton("Ok")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.translate_text)
        self.ui.pushButton_2.clicked.connect(self.show_info)

        self.translator = Translator()

        self.language_history = self.load_language_history()

        self.populate_languages()

    def load_language_history(self):
        history_file = "language_history.json"
        if os.path.exists(history_file):
            with open(history_file, "r") as f:
                return json.load(f)
        return {}

    def save_language_history(self):
        with open("language_history.json", "w") as f:
            json.dump(self.language_history, f)

    def populate_languages(self):
        languages = ['en', 'ru', 'es', 'de', 'fr', 'it', 'pt', 'zh-cn', 'ja', 'ko', 'ar', 'pl', 'nl', 'sv', 'tr']
        language_names = ['English', 'Russian', 'Spanish', 'German', 'French', 'Italian', 'Portuguese', 'Chinese', 'Japanese', 'Korean', 'Arabic', 'Polish', 'Dutch', 'Swedish', 'Turkish']

        sorted_languages = sorted(zip(language_names, languages), key=lambda x: self.language_history.get(x[1], 0), reverse=True)

        for name, lang in sorted_languages:
            self.ui.comboBox.addItem(name, lang)
            self.ui.comboBox_2.addItem(name, lang)

    def translate_text(self):
        source_text = self.ui.textEdit.toPlainText()

        if not source_text.strip():
            self.ui.textEdit_2.setPlainText("Error: Please enter text for translation.")
            return

        source_lang = self.ui.comboBox.currentData()
        target_lang = self.ui.comboBox_2.currentData()

        self.update_language_history(source_lang)
        self.update_language_history(target_lang)

        try:
            translation = self.translator.translate(source_text, src=source_lang, dest=target_lang)
            self.ui.textEdit_2.setPlainText(translation.text)
        except Exception as e:
            self.ui.textEdit_2.setPlainText(f"Error: {e}")

        self.save_language_history()

    def update_language_history(self, lang):
        if lang in self.language_history:
            self.language_history[lang] += 1
        else:
            self.language_history[lang] = 1

    def show_info(self):
        self.info_window = InfoWindow(self)
        self.info_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
