import requests
import json
import datetime
import mysql.connector

def get_next_weekday(startdate, weekday):
    """
    @startdate: given datetime
    @weekday: week day as a integer, between 0 (Monday) to 6 (Sunday)
    """
    #d = datetime.datetime.strftime(startdate, '%Y-%m-%d')
    t = datetime.timedelta((7 + weekday - startdate.weekday()) % 7)
    return (startdate + t)

db = mysql.connector.connect(host="127.0.0.1",    # your host, usually localhost
                              user="root",         # your username
                              password="abc123",  # your password
                              auth_plugin="mysql_native_password",
                              database="cal")        # name of the data base


cur = db.cursor()
j=0
# get date from kv table
sql='select v from kv where k="last_checked"'
cur.execute(sql)
date_str=cur.fetchone()
print(date_str)
#db.commit()
# convert string to datetime
dt=datetime.datetime.strptime(date_str[0],"%Y/%m/%d")
#dt=get_next_weekday(datetime.datetime.now(),6)
url='https://orono.api.nutrislice.com/menu/api/weeks/school/orono-intermediate-school/menu-type/lunch/'+dt.strftime("%Y/%m/%d")+'/?format=json'
#print(url)
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
response = requests.get(url, headers=headers,verify=False)
json_response=json.loads(response.content)
while(len(response.content)>650):
    dt_prev=dt
    #print(response.content)
    d=json_response.get('days')
    for i in range(0,len(d)):
        menu_items=d[i].get('menu_items')
        date=d[i].get('date')
        if (len(menu_items)>0):
            menu_str=''
            for j in range(0,len(menu_items)):
                if menu_items[j].get('is_section_title'):
                    menu_str+='&nbsp;&nbsp;&nbsp;<b>'+menu_items[j].get('text')+'</b><br>'
                    #print('&nbsp;&nbsp;&nbsp;<b>'+menu_items[j].get('text')+'</b><br>')
                elif menu_items[j].get('text')!='': # not empty
                    menu_str+='&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+menu_items[j].get('text')+'<br>'
                    #print('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+menu_items[j].get('text')+'<br>')
                if menu_items[j].get('food') is not None: # not null
                    menu_str+='&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+menu_items[j].get('food').get('name')+'<br>'
                    #print('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+menu_items[j].get('food').get('name')+'<br>')

            sql='insert into menu(menu_date,menu) values (%s,%s)'
            val=(date,menu_str)
            #print(date+" xxx "+menu_str)
            cur.execute(sql,val)
            db.commit()
    j+=1
    dt=dt_prev+datetime.timedelta(days=7)
    url='http://orono.api.nutrislice.com/menu/api/weeks/school/orono-intermediate-school/menu-type/lunch/'+dt.strftime("%Y/%m/%d")+'/?format=json'
    #print(url)
    response = requests.get(url, headers=headers,verify=False)
    json_response=json.loads(response.content)

# insert last sunday into kv
sql='update kv set v=%s where k="last_checked"'
val=(dt.strftime("%Y/%m/%d"),)
cur.execute(sql,val)
db.commit()