import vk
import time
from datetime import datetime
import csv
import settings

session = vk.Session(
    access_token=settings.ACCESS_TOKEN)
vk_api = vk.API(session=session, v=5.92)


FLAG_FRIEND = False
FLAG_SUBS = False
OUTPUT_CSV_FILE = settings.USER_DATA_FILE_PATH

class User:
    def __init__(self, id, date):
        self.id = id

        self.create_date = date
        self.age_wall = 2021 - int(self.create_date.split('-')[0]) # c погрешностью на декабрь

        self.first_name = ''
        self.last_name = ''
        self.f_status = -1
        self.age_user = -1
        self.birhtay_date = ''
        self.city = ''

        self.education_flag = False
        self.education = []

        self.language = []
        self.family_flag = False #проверить
        self.contact_flag= False
        self.contact = []
        self.books = ''
        self.works_flag = False

        self.military_int = -1
        self.int_user = '' # проверить
        self.life_main = -1
        self.people_main = -1
        self.smoking = -1
        self.alcohol = -1
        self.last_seen = ''
        self.open_flag = False
        self.friend = []
        self.has_photo = -1
        self.subscriptions = []
        self.sex = -1

    def set_age(self, birt_date):
        self.birhtay_date = birt_date
        if (birt_date==''):
            self.age_user = -1
        else:
            if(len(birt_date.split('.')) == 2): # d.m
                self.age_user = -1
            else:
                year = int(birt_date.split('.')[2])
                self.age_user = 2021 - year # сейчас декабрь, родившееся в декабре 2003 - погрешность
        # birt_date can be d.m.yyyy / d.m / ''
        # self.age = 0

    def set_cintact_flag(self):
        for cont in self.contact:
            if cont!= '':
                self.contact_flag = True

    def set_work_flag(self, arr):
        if len(arr) > 0:
            self.works_flag = True

    def set_education_flag(self):
        if len(self.education) > 0:
            self.education_flag = True



    def set_relation(self, rel):
        self.f_status = rel




def get_wall_information(owner_id, count, offset=0):
    info = vk_api.wall.get(owner_id=owner_id, offset=offset, count=count, extended=1)
    return info


def get_user_info(owner_id):
    # info = vk_api.users.get(owner_id=owner_id)
    time.sleep(0.4)
    try:
        info_temp = vk_api.users.get(user_ids=owner_id, fields='first_name,last_name,is_closed,about,'
                                                        'activities,bdate,books,career,city,connections,'
                                                        'contacts,country,education,has_mobile,has_photo,'
                                                        'home_townhome_town,interests,last_seen,military,nickname,'
                                                        'occupation,personal,relatives,relation,schools,'
                                                        'sex,status,universities,relation,last_seen')
    except BaseException as err:
        print(err)
        time.sleep(1)
        info_temp = vk_api.users.get(user_ids=owner_id, fields='first_name,last_name,is_closed,about,'
                                                        'activities,bdate,books,career,city,connections,'
                                                        'contacts,country,education,has_mobile,has_photo,'
                                                        'home_townhome_town,interests,last_seen,military,nickname,'
                                                        'occupation,personal,relatives,relation,schools,'
                                                        'sex,status,universities,relation,last_seen')
    friends = {'items' : []}
    if (FLAG_FRIEND):
        time.sleep(0.4)
        try:
            friends = vk_api.friends.get(user_id=owner_id)
            
        except BaseException as err:
            print(err)
            friends = {'items' : []} # This profile is private
    else:
        friends = {'items' : []}

    if (FLAG_SUBS):
        time.sleep(0.4)
        subs = []
        try:
            subs = vk_api.groups.get(user_id = owner_id, count=1000, extended=1)
            
        except BaseException as err:
            print(err)
            subs = []
    else:
        subs = []

    return info_temp, friends, subs


def parse_user_info(info, friends, subs, user, i=0):
    info = info[i] # при передаче по одному id в get_user_info
    user.first_name = info['first_name']
    user.last_name = info['last_name']

    if('is_closed' not in info):
        user.open_flag = False
        # print(f'\n user with id = {user.id} not have is_closed variables')
        return user

    if(info['is_closed'] == False):
        user.open_flag = True
    else:
        user.open_flag = False
        return user

    if('deactevated' in info):
        if(info['deactevated'] == 'deleted' or info['deactevated'] == 'banned'):
            user.open_flag = False
            return user
    try:
        if (subs!=[]):
            items = subs['items']
            tem_res_arr = []
            for it in items:
                name = (it['name']).replace('|', '-')
                tem_res_arr.append(name)
            user.subscriptions = tem_res_arr
    except BaseException as err:
        print(err)

        

    if('has_photo' in info):
        user.has_photo = info['has_photo']

    if 'sex' in info:
        user.sex = info['sex']


    if ('city' in info):
        user.city = info['city']['title']
    temp = 0
    if('military' in info):
        if( info['military'] != []):
        # print('id usera - ', user.id)
        # print(info['military'])

            if ('unit' in info['military'][0] or 'unit_id' in info['military'][0] ):
                try:
                    if(info['military'][0]['unit'] != ''):
                        temp = temp + 1
                except:
                    if(info['military']['unit_id'] != 0):
                        temp = temp + 2          

            if ('from' in info['military'][0] and 'until' in info['military'][0] ):
                if(info['military'][0]['from'] != 0 and info['military'][0]['until'] != 0):
                    temp = temp + 1

    user.military_int = temp

    if('relatives' in info):
        if(len(info['relatives']) > 0):
            user.family_flag = True

    if('relation' in info):
        user.set_relation(info['relation'])

    if ('bdate' in info):
        user.set_age(info['bdate'])
    else:
        user.set_age('')

    if('universities' in info):
        un = info['universities']
        for u in un:
            user.education.append(u['name'])
        user.set_education_flag()

    if('books' in info):
        user.books = info['books']
    if ('career' in info):
        user.set_work_flag(info['career'])

    if ('interests' in info):
        user.int_user = info['interests']

    if('mobile_phone' in info):
        if(info['mobile_phone'] != ''):
            user.contact.append('mobile_phone:' + info['mobile_phone'])
    if('home_phone' in info):
        if(info['home_phone'] != ''):
            user.contact.append('home_phone:' + info['home_phone'])
    if('skype' in info):
        if(info['skype'] != ''):
            user.contact.append('skype:' + info['skype'])
    if('instagram' in info):
        if(info['instagram'] != ''):
            user.contact.append('instagram:' + info['instagram'])
    if('whatsapp' in info):
        if(info['whatsapp'] != ''):
            user.contact.append('whatsapp:' + info['whatsapp'])
    if('facebook' in info):
        if(info['facebook'] != ''):
            user.contact.append('facebook:' + info['facebook'])
    if('twitter' in info):
        if(info['twitter'] != ''):
            user.contact.append('twitter:' + info['twitter'])
    if('livejournal' in info):
        if(info['livejournal'] != ''):
            user.contact.append('livejournal:' + info['livejournal'])
    user.set_cintact_flag()

    if('last_seen' in info):
        user.last_seen = datetime.fromtimestamp(info['last_seen']['time']).date() # convert
    user.friend = friends['items']

    if('personal' not in info):
        return user

    if('langs' in info['personal']):
        user.language = info['personal']['langs']

    if('alcohol' in info['personal']):
        user.alcohol = info['personal']['alcohol']
    if('smoking' in info['personal']):
        user.smoking = info['personal']['smoking']
    if('people_main' in info['personal']):
        user.people_main = info['personal']['people_main']
    if('life_main' in info['personal']):
        user.life_main = info['personal']['life_main']
    return user



def get_user_id_date():
    """
    :return user array
    id - int
    date-str
    """
    with open(settings.DATE_DATA_PATH, 'r') as f:
        raws = f.read()

    row_arr = raws.split('\n')
    result_arr = []
    for i in range (0, len(row_arr)):
        try:
            id = row_arr[i].split(' ')[0] # там 2 слова - id date
            date = (row_arr[i].split(' ')[1])
        except:
            id = row_arr[i].split('\t')[0] # там 2 слова - id date
            date = (row_arr[i].split('\t')[1])

        user = User(id=id, date=date)
        result_arr.append(user)
    return result_arr 

def dozapis_csv(res_arr):
    heading = []

    for res in res_arr:
        data = []
        data.append(res.id)
        data.append(res.first_name)
        data.append(res.last_name)
        data.append(res.f_status)

        data.append(res.age_user)
        data.append(res.birhtay_date)
        data.append(res.city)
        data.append(res.education_flag)
        
        data.append(res.education)
        data.append(res.language)
        data.append(res.family_flag)
        data.append(res.contact_flag)
        
        data.append(res.contact)
        data.append(res.books)
        data.append(res.works_flag)
        data.append(res.military_int)
        
        data.append(res.int_user)
        data.append(res.life_main)
        data.append(res.people_main)
        data.append(res.smoking)
        
        data.append(res.alcohol)
        data.append(res.last_seen)
        data.append(res.open_flag)
        data.append(res.age_wall)

        data.append(res.create_date)
        data.append(res.friend)
        data.append(res.has_photo)
        data.append(res.subscriptions)
        data.append(res.sex)

        heading.append(data)

    with open(OUTPUT_CSV_FILE, 'a') as myFile:
        writer = csv.writer(myFile,delimiter='|')
        writer.writerows(heading)


if __name__ == '__main__':
    # id_kate = 'ekaterina_novoselova'
    # id_d = 'vovanchic'
    # str_u = 'ekaterina_novoselova,vovanchic'

    # FLAG_FRIEND = False
    # user = User(id_kate, '2006-11-29')
    # user2 = User(id_d, '2006-11-29')
    # info, friends = get_user_info(str_u)
    # user = parse_user_info(info, friends, user, 0)
    # user2 = parse_user_info(info, friends, user2, 1)
    # e =2
    # heading = [["id_user", "first_name", "last_name", "f_status",
    #            "age_users", "data_old", "city", "education_flag",
    #            "education", "language", "family_flag", "contact_flag",
    #            "contact", "books", "works_flag", "military_int",
    #            "interes", "life_main", "people_main", "smoking",
    #            "alcohol", "last_seen", "open_flag", "age_pages", 
    #            "data_pages", "friend", 'has_photo', 'subscriptions', 'sex']]

    # with open('final.csv', 'w') as myFile:
    #     writer = csv.writer(myFile, delimiter= "|")
    #     writer.writerows(heading)


    # при использовании этого файла все в try str ='12,13,14,'

    users_arr =get_user_id_date()
    res_arr = []
    FLAG_FRIEND = False
    FLAG_SUBS = False
    users_arr_len = len(users_arr)
    delta = 1
    shetchik = 1
    step = 500

    format = '%m/%d/%y %H:%M:%S'
    start_time = datetime.strptime(datetime.now().strftime(format), format)

    for i in range(0, users_arr_len, delta):
        str_ = ''
        for j in range(i, min((i+delta), users_arr_len)):
            str_ += users_arr[j].id + ','
        print("Process {:10} of {:10} || i-th id is {:30}\r".format(i, users_arr_len, users_arr[i].id), end="", flush=True)
        info, friends, subs = get_user_info(str_)
        for j in range(i, min((i+delta), users_arr_len)):
            try:
                parse_info_user = parse_user_info(info=info, friends=friends, subs=subs, user=users_arr[j], i=j-i)
                res_arr.append(parse_info_user)
            except BaseException as err:
                print(err)
                print(f'\nfailed with id = {users_arr[j].id}\n')
        if(shetchik > step):
            shetchik = 0
            dozapis_csv(res_arr)
            print()
            print("Save done to ", OUTPUT_CSV_FILE)
            res_arr = []
        shetchik = shetchik + 1

    dozapis_csv(res_arr)
    end_time = datetime.strptime(datetime.now().strftime(format), format)

    delta_time = end_time - start_time
    print()
    print("Download DONE. Time spent ", delta_time)
