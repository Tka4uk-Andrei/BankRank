import csv
import subprocess as sb
import settings

from flask import render_template
from flask import Flask

file_calc = settings.RANKED_USER_FILE_PATH
file_user = settings.USER_DATA_FILE_PATH

count_0_5 = 0
arr_0_5 = []
count_5_10 = 0
arr_5_10 = []
count_10_15 = 0
arr_10_15 = []
count_15_20 = 0
arr_15_20 = []
count_20_25 = 0
arr_20_25 = []

str_1 = ''
str_2 = ''
str_3 = ''
str_4 = ''
str_5 = ''

count_0_5 = 0
arr_0_5 = []
count_5_10 = 0
arr_5_10 = []
count_10_15 = 0
arr_10_15 = []
count_15_20 = 0
arr_15_20 = []
count_20_25 = 0
arr_20_25 = []



def get_balls():
    res_arr = []
    with open(file_calc) as File:
        reader = csv.DictReader(File, delimiter=',')
        for row in reader:
            res_arr.append(row)
    return res_arr
    
def get_users(str_1, str_2, str_3, str_4, str_5):
    res_arr = []
    with open(file_user) as File:
        reader = csv.DictReader(File, delimiter='|')
        for row in reader:
            print(row['id_user'])
            if(row['id_user'] in arr_0_5):
                str_1 += row['id_user'] + ' ' + row['first_name'] + ' ' + row['last_name'] + '\n'
            if(row['id_user'] in arr_5_10):
                str_2 += row['id_user'] + ' ' + row['first_name'] + ' ' + row['last_name'] + '\n'
            if(row['id_user'] in arr_10_15):
                str_3 += row['id_user'] + ' ' + row['first_name'] + ' ' + row['last_name'] + '\n'
            if(row['id_user'] in arr_15_20):
                str_4 += row['id_user'] + ' ' + row['first_name'] + ' ' + row['last_name'] + '\n'
            if(row['id_user'] in arr_20_25):
                str_5 += row['id_user'] + ' ' + row['first_name'] + ' ' + row['last_name'] + '\n'


            # res_arr.append(row)
    return str_1, str_2, str_3, str_4, str_5


bols = get_balls()





def create_table(count_0_5,arr_0_5,count_5_10 ,arr_5_10 ,count_10_15,arr_10_15 ,count_15_20,arr_15_20 ,count_20_25,arr_20_25 , str_1, str_2, str_3, str_4, str_5):

    for row in bols:
        mark = int(row['total_mark'])
        s = 'id - '+ row['id_user'] + ', total mark - ' + str(mark) + '.   '
        if(mark<6):
            
            count_0_5 = count_0_5+1
            arr_0_5.append(row['id_user'])
            str_1 += s
        if(mark<11) and (mark>=6):
            count_5_10 = count_5_10+1
            str_2 += s
            arr_5_10.append(row['id_user'])
        if(mark<16) and (mark>=11):
            count_10_15 = count_10_15+1
            str_3 += s
            arr_10_15.append(row['id_user'])
        if(mark<21) and (mark>=16):
            count_15_20 = count_15_20+1
            arr_15_20.append(row['id_user'])
            str_4 += s
        if (mark>=21):
            count_20_25 = count_20_25+1
            arr_20_25.append(row['id_user'])
            str_5 += s
    return count_0_5,arr_0_5,count_5_10 ,arr_5_10 ,count_10_15,arr_10_15 ,count_15_20,arr_15_20 ,count_20_25,arr_20_25 ,str_1, str_2, str_3, str_4, str_5
    
    
count_0_5,arr_0_5,count_5_10 ,arr_5_10 ,count_10_15,arr_10_15 ,count_15_20,arr_15_20 ,count_20_25,arr_20_25 ,str_1, str_2, str_3, str_4, str_5 = create_table(count_0_5,arr_0_5,count_5_10 ,arr_5_10 ,count_10_15,arr_10_15 ,count_15_20,arr_15_20 ,count_20_25,arr_20_25,str_1, str_2, str_3, str_4, str_5 )

# str_1, str_2, str_3, str_4, str_5 = get_users(str_1, str_2, str_3, str_4, str_5)

# import http.server
# import socketserver

# PORT = 8083
# Handler = http.server.SimpleHTTPRequestHandler

# with socketserver.TCPServer(("", PORT), Handler) as httpd:
#     print("serving at port", PORT)
#     httpd.serve_forever()



app = Flask(__name__) 

@app.route('/')
def index():
    return render_template('./page.html',c_1=count_0_5,c_2=count_5_10,c_3=count_10_15,c_4=count_15_20,c_5=count_20_25)






@app.route('/h_0_5/')
def h_0_5():
    return render_template('./0_5.html', id=str_1)

@app.route('/h_5_10/')
def h_5_10():
    return render_template('./5_10.html', id_=str_2)

@app.route('/h_10_15/')
def h_10_15():
    return render_template('./10_15.html', id_=str_3)

@app.route('/h_15_20/')
def h_15_20():
    return render_template('./15_20.html', id_=str_4)

@app.route('/h_20_25/')
def h_20_25():
    return render_template('./20_25.html', id_=str_5)

app.run(host='0.0.0.0', port=5000,debug=True)


if __name__ == '__main__':
    ...