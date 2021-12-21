import vk
import time
from datetime import datetime
import csv
import settings

session = vk.Session(access_token=settings.ACCESS_TOKEN)
vk_api = vk.API(session=session, v=5.92)
FLAG_FRIEND = False

applicable_cities = ['Санкт-Петербург',
                     'Лен. Область', 'Мурино', 'Приозерск', 'Гатчина', 
                     'Кириши', 'Сестрорецк', 
                     'Москва', 
                     'Новосибирск',
                     'Калининград',
                     'Краснодар',
                     'Ростов-на-Дону', 'Ленинградская область']


def get_id_sber():
    page = 0
    limit = 1000
    info = vk_api.groups.getMembers(group_id=settings.VK_GROUP_ID, offset=0)
    count_ = info['count']
    res_arr = []

    
    while(count_ > (page-1) * limit):
        offset_ = page * limit
        print(offset_, ' of ', count_)
        time.sleep(0.35)
        members = vk_api.groups.getMembers(group_id=settings.VK_GROUP_ID, offset=offset_, count=limit, fields='city')
        items = members['items']
        for item in items:
            if 'city' in item:
                if (item['city']['title'] in applicable_cities):
                    if ('is_closed' in item):
                        if (item['is_closed'] == False):
                            if('deactevated' in item):
                                if(item['deactevated'] == 'deleted' or item['deactevated'] == 'banned'):
                                    continue
                            res_arr.append(item['id'])

        page = page+1

    str_ = ''
    for it in res_arr:
        str_ += str(it) + '\n'


    with open(settings.ID_DATA_PATH, 'w') as f:
        f.write(str_)


if __name__ == '__main__':
    get_id_sber()