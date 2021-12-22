VK_GROUP_ID = "bspb"
# VK_GROUP_ID = "sber"

DATA_FILE_PATH="data/"

ID_DATA_PATH = DATA_FILE_PATH + "users_id.txt"
DATE_DATA_PATH = DATA_FILE_PATH + "users_date.txt"
USERS_WITH_DELETED_PAGES_PATH = DATA_FILE_PATH + "users_with_delete_page.txt"
USER_DATA_FILE_PATH = DATA_FILE_PATH + "final.csv"
RANKED_USER_FILE_PATH = DATA_FILE_PATH + "calculated_user_data.csv"

# Значение ACCESS_TOKEN получаем по ссылке 
# https://oauth.vk.com/authorize?client_id=app_id&display=page&scope=friends&response_type=token&v=5.92&state=123456
# где app_id - ID приложения, зарегистрированного в ВК.
ACCESS_TOKEN = ""