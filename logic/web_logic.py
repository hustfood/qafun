# -*- coding: utf-8 -*-
import os
import random
from db_op import user as db
import id_generate

def vote(user_vote):
    Userdb = db()
    if not is_valid_time() or not is_valid_id(user_vote['nianhuiid']):
        return False
    if user_vote.get('vote1') not in [1,2,3,4,5] or user_vote.get('vote2') not in [1,2,3,4,5]:
        return False
    if user_vote.get('vote1') == user_vote.get('vote2'):
        return False
    Userdb.save_vote(user_vote)
    return True


def is_valid_id(_id):
    Userdb = db()
    valid_id_list = Userdb.find_id()
    if _id in valid_id_list:
        return True
    else:
        return False

def is_valid_time():
    Userdb = db()
    valid_time = Userdb.get_valid_time()
    return eval(valid_time)

def set_valid_time(valid_time):
    Userdb = db()
    Userdb.set_valid_time(valid_time)

def get_result_now():
    Userdb = db()
    result = {'1':0,'2':0,'3':0,'4':0,'5':0,'0':0}
    userlist = Userdb.find()
    for user in userlist:
        if user['name'] == 'system':
            continue
        result[str(user.get('vote1',0))]+=1
        result[str(user.get('vote2',0))]+=1
    return result

def get_win():
    Userdb = db()
    win_id = Userdb.get_win()
    return win_id

def set_win(winid):
    Userdb = db()
    Userdb.set_win(winid)

def random_for_C():
    Userdb = db()
    win_id = get_win()
    if not win_id or win_id == 0:
        return
    luck_userc = list(Userdb.find({'group':int(win_id)}))
    luck_num = random.randint(0,len(luck_userc))
    luck_userc[luck_num]['lucktag'] = 1
    Userdb.save(luck_userc[luck_num])
    return luck_userc[luck_num]

def random_for_vote_C():
    Userdb = db()
    win_id = get_win()
    if not win_id:
        return
    luck_voteuserc = set()
    userlist = list(Userdb.find())
    print len(userlist)
    for user in userlist:
        if (user.get('vote1') == win_id or user.get('vote2') == win_id ) and user.get('lucktag') != 1:
            luck_voteuserc.add(user.get('nianhuiid'))
    luck_voteuserc = list(luck_voteuserc)
    print len(luck_voteuserc)
    luckvote = random.randint(0,len(luck_voteuserc))
    print luckvote
    luckuser = Userdb.find_one({'nianhuiid':luck_voteuserc[luckvote]})
    luckuser['lucktag'] = 1
    Userdb.save(luckuser)
    return luck_voteuserc[luckvote]

if __name__ == "__main__":
    Userdb = db()
    user_list = Userdb.find()
    for i in user_list:
        if i.get('name') == 'system':
            continue
        i['vote1'] = random.randint(1,6)
        i['vote2'] = random.randint(1,6)
        vote(i)
    print get_result_now()
    set_win(3)
    print random_for_C()
    print random_for_vote_C()
    print random_for_vote_C()
    print random_for_vote_C()





