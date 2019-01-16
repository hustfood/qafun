# -*- coding: utf-8 -*-
import os
import random
from db_op import user as db

FILEPATH = u"2019年会.csv"
GROUPDICT = {'gaia':1,
             'titan':2,
             'moco':3,
             'eros':4,
             'Flamemission':5
}

def get_in_db(path):
    f = open(path,'r')
    namelist =  f.readlines()
    f.close()
    last4_id = []
    for nameline in namelist[1:]:
        user_info = nameline.split(',')
        user = {}
        user['workid'] = user_info[0]
        try:
            user['name'] = user_info[1].decode('gb2312')
        except:
            #print user
            user['name'] = user_info[1].decode('gbk')
        user['group'] = GROUPDICT.get(user_info[-2],5)
        last4 = random.randint(0,10000)
        while(last4 not in last4_id):
            last4 = random.randint(0,10000)
            last4_id.append(last4)
        user['nianhuiid'] = user['workid'][1:]+('%04d'%last4)
        print user
        save_txt(user)


    #db.save(user)

def insert_db_from_txt():
    f= open('nianhuiid.txt','r')
    content = f.readlines()
    f.close()

    f = open(FILEPATH,'r')
    namelist =  f.readlines()
    f.close()
    name_dic = {}
    for nameline in namelist[1:]:
        user_info = nameline.split(',')
        try:
            name = user_info[1].decode('gb2312')
        except:
            #print user
            name = user_info[1].decode('gbk')
        group = GROUPDICT.get(user_info[-1].strip(),5)
        name_dic[name] = group

    print name_dic

    Userdb = db()
    for i in content:
        user = {}
        ct = i.split(' ')
        user['nianhuiid'] = ct[0]
        if len(ct)>2:
            user['name'] = ' '.join([ct[1],ct[2],ct[3],ct[4]]).replace('\n','').replace('\r', '')
        else:
            user['name'] = i.split(' ')[1].replace('\n','').replace('\r', '')
        user['group'] = name_dic.get(user['name'].decode('utf8'),0)
        Userdb.insert_user(user)
    user = {'name':'system','valid_time':'True'}
    Userdb.insert_user(user)

def save_txt(user):
    f = open('nianhuiid.txt','a')
    f.write(' '.join([user['nianhuiid'],user['name'].encode('utf8')])+'\n')
    f.close()


if __name__ == "__main__":
    #get_in_db(FILEPATH)
    insert_db_from_txt()
