import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
IMAGES_DIR = os.path.join(ASSETS_DIR, 'images')
CITIZEN_IMAGES_DIR = os.path.join(IMAGES_DIR, 'citizens')
STYLESHEET_PATH = os.path.join(ASSETS_DIR, 'style.qss')

APP_NAME = 'BCHQS - Quản lý công dân'
LOGIN_WINDOW_WIDTH = 490
LOGIN_WINDOW_HEIGHT = 340
MAIN_WINDOW_WIDTH = 1400
MAIN_WINDOW_HEIGHT = 820

DB_HOST = '127.0.0.1'
DB_PORT = 3306
DB_USER = 'bch'
DB_PASSWORD = 'BCHQSPTB'
DB_NAME = 'military_citizen_db'
DB_AUTH_PLUGIN = 'mysql_native_password'
DB_USE_PURE = True
