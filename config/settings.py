import os
import sys


def get_app_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_resource_dir():
    if getattr(sys, 'frozen', False):
        return getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


APP_DIR = get_app_dir()
BASE_DIR = APP_DIR
RESOURCE_DIR = get_resource_dir()
ASSETS_DIR = os.path.join(RESOURCE_DIR, 'assets')
DATA_ASSETS_DIR = os.path.join(APP_DIR, 'assets')
IMAGES_DIR = os.path.join(DATA_ASSETS_DIR, 'images')
CITIZEN_IMAGES_DIR = os.path.join(IMAGES_DIR, 'citizens')
STYLESHEET_PATH = os.path.join(ASSETS_DIR, 'style.qss')

APP_NAME = 'BCHQS - Quản lý công dân'
LOGIN_WINDOW_WIDTH = 580
LOGIN_WINDOW_HEIGHT = 430
MAIN_WINDOW_WIDTH = 1400
MAIN_WINDOW_HEIGHT = 820

DB_HOST = '127.0.0.1'
DB_PORT = 3306
DB_USER = 'bch'
DB_PASSWORD = 'BCHQSPTB'
DB_NAME = 'military_citizen_db'
DB_AUTH_PLUGIN = 'mysql_native_password'
DB_USE_PURE = True
