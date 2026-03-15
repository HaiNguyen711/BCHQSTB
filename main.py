import os
import sys

from PySide6.QtWidgets import QApplication

from config.settings import APP_NAME, STYLESHEET_PATH
from ui.auth.login_window import LoginWindow


def load_stylesheet(app):
    if not os.path.exists(STYLESHEET_PATH):
        return

    with open(STYLESHEET_PATH, 'r', encoding='utf-8') as file:
        app.setStyleSheet(file.read())


def main():
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)

    load_stylesheet(app)

    window = LoginWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
