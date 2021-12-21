import time

from bs4 import BeautifulSoup
import requests
from datetime import datetime
import settings


str_ = 'https://vk.com/foaf.php?id='


def read_file(file):
    with open(file, 'r') as f:
        raws = f.read()
    return raws

def get_date(id):
    response = requests.get('https://vk.com/foaf.php?id='+id)
    xml = response.text
    soup = BeautifulSoup(xml,  "html.parser")
    # soup = BeautifulSoup(xml, 'lxml')
    created = soup.find('ya:created').get('dc:date')
    date = str(created).split('T')[0]
    return created, date

if __name__ == '__main__':
    new_str = ''
    rows = read_file(settings.ID_DATA_PATH)
    rows_arr = rows.split('\n')
    now = datetime.now()

    deleted_id = ''
    for i in range (0, len(rows_arr)):
        id = rows_arr[i]
        try:
            created, data_created = get_date(id)
            # age = (curent_data_in_datatime - datetime.strptime(data_created, format))
            print(i, ' of ', len(rows_arr))
            new_str +=id + ' ' + data_created + '\n'

        except:
            deleted_id +=id + '\n'
            print(id + '---------')

    with open(settings.DATE_DATA_PATH, mode='w') as f:
        f.write(new_str)

    with open(settings.USERS_WITH_DELETED_PAGES_PATH, mode='w') as f:
        f.write(deleted_id)


