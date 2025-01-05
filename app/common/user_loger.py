import logging
import os

LOG_DIR: str = os.path.join(os.path.dirname(__file__), '..', '..', 'log')
LOG_FILE_PATH: str = os.path.join(LOG_DIR, 'users.log')
NOTIFICATION_LOG_FILE_PATH: str = os.path.join(LOG_DIR, 'notification.log')
os.makedirs(LOG_DIR, exist_ok=True)

user_loger = logging.getLogger('result_logger')
user_loger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(LOG_FILE_PATH, encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s __ %(levelname)s __ %(message)s')
file_handler.setFormatter(formatter)
user_loger.addHandler(file_handler)
