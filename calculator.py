import csv
import settings

user_data_heading = ["id_user", "first_name", "last_name", "f_status",
                     "age_users", "data_old", "city", "education_flag",
                     "education", "language", "family_flag", "contact_flag",
                     "contact", "books", "works_flag", "military_int",
                     "interes", "life_main", "people_main", "smoking",
                     "alcohol", "last_seen", "open_flag", "age_pages", 
                     "data_pages", "friend", "has_photo", "subscriptions",
                     "sex"]

calculated_user_data_heading = ["id_user", "first_name", "last_name", "sex",
                                "first_name_mark", "last_name_mark", "f_status_mark",
                                "age_users_mark", "city_mark", "education_mark", "language_mark", 
                                "family_flag_mark", "contact_flag_mark", "books_mark", "interes_mark",
                                "works_flag_mark", "military_int_mark", "life_main_mark", "people_main_mark",
                                "smoking_mark", "alcohol_mark", "age_pages_mark", "has_photo_mark",
                                "subscriptions_mark",
                                "total_mark"]

applicable_cities = ['Санкт-Петербург',
                     'Лен. Область', 'Мурино', 'Приозерск', 'Гатчина', 
                     'Кириши', 'Сестрорецк', 
                     'Москва', 
                     'Новосибирск',
                     'Калининград',
                     'Краснодар',
                     'Ростов-на-Дону', 'Ленинградская область']

applicable_interests = ['бизнес', 'инвестиции', 'предпринимательство',
                        'коммерция', 'промышленность', 'хозяйство', 
                        'экономика', 'финансы', 'маркетинг',
                        'путешествия', 'спорт', 'здоровье']

def isInGroup(user_data, keyWords):
    for key in keyWords:
        if (user_data['subscriptions'].lower()).find(key) != -1:
            return True
    return False


def criteria_calculation(user_data):
    calculated_user_data = {}
    total = 0
    calculated_user_data = {'id_user': user_data['id_user']}

    # 3.1
    # Nothing to do
    calculated_user_data['first_name_mark'] = 0
    calculated_user_data['last_name_mark'] = 0
    total += calculated_user_data['first_name_mark']
    total += calculated_user_data['last_name_mark']

    # 3.2
    calculated_user_data['f_status_mark'] = 0
    if (user_data['f_status'] == 3 or user_data['f_status'] == 4):
        calculated_user_data['f_status_mark'] = 2
    if (user_data['f_status'] == 8):
        calculated_user_data['f_status_mark'] = 1
    total += calculated_user_data['f_status_mark']

    # 3.3
    calculated_user_data['age_users_mark'] = 0
    user_data['age_users'] = int(user_data['age_users'])
    if (21 <= user_data['age_users'] < 24):
        calculated_user_data['age_users_mark'] = 0
    if (24 <= user_data['age_users'] < 30):
        calculated_user_data['age_users_mark'] = 1
    if (30 <= user_data['age_users'] < 50):
        calculated_user_data['age_users_mark'] = 2
    if (50 <= user_data['age_users'] < 65):
        calculated_user_data['age_users_mark'] = 1
    if (65 <= user_data['age_users'] < 72):
        calculated_user_data['age_users_mark'] = 0
    total += calculated_user_data['age_users_mark']

    # 3.4 - improve?
    calculated_user_data['city_mark'] = 0
    for city in applicable_cities:
        if (user_data['city'] == city):
            calculated_user_data['city_mark'] = 2
    total += calculated_user_data['city_mark']

    # 3.5
    calculated_user_data['education_mark'] = 0
    user_data['education'] = get_arr(user_data['education'])
    if (len(user_data['education']) == 1):
        calculated_user_data['education_mark'] = 1
    if (len(user_data['education']) >= 2):
        calculated_user_data['education_mark'] = 2
    total += calculated_user_data['education_mark']

    # 3.6
    calculated_user_data['language_mark'] = 0
    user_data['language'] = get_arr(user_data['language'])
    if (len(user_data['language']) >= 2):
        calculated_user_data['language_mark'] = 1
    total += calculated_user_data['language_mark']

    # 3.7
    calculated_user_data['family_flag_mark'] = 0
    if (user_data['family_flag'] == 'True'):
        calculated_user_data['family_flag_mark'] = 1
    total += calculated_user_data['family_flag_mark']

    # 3.8
    calculated_user_data['contact_flag_mark'] = 0
    if (user_data['contact_flag'] == 'True'):
        calculated_user_data['contact_flag_mark'] = 1
    total += calculated_user_data['contact_flag_mark']

    # 3.9
    calculated_user_data['books_mark'] = 0
    if (user_data['books'] != ''):
        calculated_user_data['books_mark'] = 1
    total += calculated_user_data['books_mark']

    # 3.10
    calculated_user_data['interes_mark'] = 0
    for interest in applicable_interests:
        if (user_data['interes'].lower()).find(interest) != -1:
            calculated_user_data['interes_mark'] = 1
    total += calculated_user_data['interes_mark']

    # 3.11
    calculated_user_data['works_flag_mark'] = 0
    if (user_data['works_flag'] == 'True'):
        calculated_user_data['works_flag_mark'] = 1
    total += calculated_user_data['works_flag_mark']

    # 3.12
    calculated_user_data['military_int_mark'] = int(user_data['military_int'])
    total += calculated_user_data['military_int_mark']


    # 3.13
    calculated_user_data['life_main_mark'] = 0
    user_data['life_main'] = int(user_data['life_main'])
    if (user_data['life_main'] == 1):
        calculated_user_data['life_main_mark'] = 2
    if (user_data['life_main'] == 2):
        calculated_user_data['life_main_mark'] = 2
    if (user_data['life_main'] == 3):
        calculated_user_data['life_main_mark'] = 1
    if (user_data['life_main'] == 4):
        calculated_user_data['life_main_mark'] = 1
    if (user_data['life_main'] == 7):
        calculated_user_data['life_main_mark'] = 2
    if (user_data['life_main'] == 8):
        calculated_user_data['life_main_mark'] = 1
    total += calculated_user_data['life_main_mark']


    # 3.14
    calculated_user_data['people_main_mark'] = 0
    user_data['people_main'] = int(user_data['people_main'])
    if (user_data['people_main'] > 0):
        calculated_user_data['people_main_mark'] = 2
    total += calculated_user_data['people_main_mark']


    # 3.15
    calculated_user_data['smoking_mark'] = 0
    user_data['smoking'] = int(user_data['smoking'])
    if (user_data['smoking'] == 1):
        calculated_user_data['smoking_mark'] = 2
    if (user_data['smoking'] == 2):
        calculated_user_data['smoking_mark'] = 1
    if (user_data['smoking'] == 3):
        calculated_user_data['smoking_mark'] = 0
    if (user_data['smoking'] == 4):
        calculated_user_data['smoking_mark'] = -1
    if (user_data['smoking'] == 5):
        calculated_user_data['smoking_mark'] = -2
    total += calculated_user_data['smoking_mark']


    # 3.16
    calculated_user_data['alcohol_mark'] = 0
    user_data['alcohol'] = int(user_data['alcohol'])
    if (user_data['alcohol'] == 1):
        calculated_user_data['alcohol_mark'] = 2
    if (user_data['alcohol'] == 2):
        calculated_user_data['alcohol_mark'] = 1
    if (user_data['alcohol'] == 3):
        calculated_user_data['alcohol_mark'] = 0
    if (user_data['alcohol'] == 4):
        calculated_user_data['alcohol_mark'] = -1
    if (user_data['alcohol'] == 5):
        calculated_user_data['alcohol_mark'] = -2
    total += calculated_user_data['alcohol_mark']


    # 3.17
    calculated_user_data['age_pages_mark'] = 0
    user_data['age_pages'] = int(user_data['age_pages'])
    if (user_data['age_pages'] <= 1):
        calculated_user_data['age_pages_mark'] = -2
    if (user_data['age_pages'] <= 2):
        calculated_user_data['age_pages_mark'] = -1
    if (user_data['age_pages'] <= 3):
        calculated_user_data['age_pages_mark'] = 0
    if (user_data['age_pages'] <= 4):
        calculated_user_data['age_pages_mark'] = 1
    if (user_data['age_pages'] > 4):
        calculated_user_data['age_pages_mark'] = 2
    total += calculated_user_data['age_pages_mark']


    # 3.18
    calculated_user_data['has_photo_mark'] = 0
    if (user_data['has_photo'] == 'True'):
        calculated_user_data['has_photo_mark'] = 1
    total += calculated_user_data['has_photo_mark']

    # 3.19 Отсутствует
    
    # 3.20 Невозможно из-за ограничений ВК

    # 3.21 Невозможно из-за ограничений ВК
    

    # Далее идёт анализ подписок
    calculated_user_data['subscriptions_mark'] = 0

    # 3.22
    keyWords322 = ['гостиница', 'отель', 'горячие путевки', 'travel', 'путешествия']
    if (isInGroup(user_data, keyWords322)):
        calculated_user_data['subscriptions_mark'] += 2

    # 3.23
    keyWords323 = ['сдам', 'сниму', 'аренда жилья']
    if (isInGroup(user_data, keyWords323)):
        calculated_user_data['subscriptions_mark'] += -1

    # 3.24
    keyWords324 = ['прогнозы на спорт', 'ставки', 'экспрессы', 'договорные матчи', 'bet']
    if (isInGroup(user_data, keyWords324)):
        calculated_user_data['subscriptions_mark'] += -3

    # 3.25
    keyWords325 = ['займы', 'кредиты', 'долги', 'коллектор', 'быстрые деньги']
    if (isInGroup(user_data, keyWords325)):
        calculated_user_data['subscriptions_mark'] += -5

    # 3.26
    keyWords326 = ['заработок в интернете', 'легкие деньги', 'халява', 'выжить за сотку']
    if (isInGroup(user_data, keyWords326)):
        calculated_user_data['subscriptions_mark'] += -3

    # 3.27
    keyWords327 = ['обучение', 'курсы']
    if (isInGroup(user_data, keyWords327)):
        calculated_user_data['subscriptions_mark'] += +3

    # 3.28 Невозможно из-за ограничений ВК

    # 3.29 Невозможно из-за ограничений ВК

    # 3.30
    keyWords330 = ['крипта', 'crypto', 'etf', 'bit', 'coin']
    if (isInGroup(user_data, keyWords330)):
        calculated_user_data['subscriptions_mark'] += -2

    # 3.31
    keyWords331 = ['здоровье', 'йога', 'фитнес', 'пилатес', 'диета', 'тренировки']
    if (isInGroup(user_data, keyWords331)):
        calculated_user_data['subscriptions_mark'] += +1

    # 3.32 @todo

    # 3.33
    keyWords333 = ['купить дешево', 'продать дешево', 'барахолка', 'блошиный рынок']
    if (isInGroup(user_data, keyWords333)):
        calculated_user_data['subscriptions_mark'] += -1

    total += calculated_user_data['subscriptions_mark']

    calculated_user_data['total_mark'] = total

    return calculated_user_data


def get_arr(string_):
    str_temp = string_.split('[')[1].split(']')[0]
    if str_temp == '':
        return []
    arr = str_temp.split("'")
    res_arr = []
    for i in range(1, len(arr), 2):
        res_arr.append(arr[i])
    return res_arr


if __name__ == '__main__':

    INPUT_FILE = settings.USER_DATA_FILE_PATH
    OUTPUT_FILE = settings.RANKED_USER_FILE_PATH

    reader = None
    results = []
    with open(INPUT_FILE) as File:
        reader = csv.DictReader(File, delimiter='|')
        for row in reader:
            if row['open_flag'] == False:
                continue
            res = criteria_calculation(row)
            results.append(res)


    myFile = open(OUTPUT_FILE, 'w')
    with myFile:
        writer = csv.DictWriter(myFile, fieldnames=calculated_user_data_heading)

        writer.writeheader()
        writer.writerows(results)



