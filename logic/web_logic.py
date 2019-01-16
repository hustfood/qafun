# -*- coding: utf-8 -*-
import os
import random
from db_op import user as db
import id_generate

###############投票#################################
def vote(user_vote):
    Userdb = db()
    if not is_valid_time():
        return 1#非法时间
    if not is_valid_id(user_vote['nianhuiid']):
        return 2#非法id
    if user_vote.get('vote1') not in [1,2,3,4,5] or user_vote.get('vote2') not in [1,2,3,4,5]:
        return 3#投票内容不合法
    if user_vote.get('vote1') == user_vote.get('vote2'):
        return 4#重复投票
    Userdb.save_vote(user_vote)
    return 0

#判断是不是合法id
def is_valid_id(_id):
    Userdb = db()
    valid_id_list = Userdb.find_id()
    if _id in valid_id_list:
        return True
    else:
        return False

#判断当前是不是合法时间
def is_valid_time():
    Userdb = db()
    valid_time = Userdb.get_valid_time()
    return eval(valid_time)

#设定是否为投票合法时间
def set_valid_time(valid_time):
    Userdb = db()
    Userdb.set_valid_time(valid_time)

##############获取当前投票结果#########
def get_result_now():
    Userdb = db()
    result = {'1':0,'2':0,'3':0,'4':0,'5':0,'0':0}
    userlist = Userdb.find()
    for user in userlist:
        if user['name'] == 'system':
            continue
        result[str(user.get('vote1',0))]+=1
        result[str(user.get('vote2',0))]+=1
    game1,game2 = Userdb.get_gamewin()
    if game1:
        for key in result.keys():
            result[key] += game1.get(str(key),0)
    if game2:
        for key in result.keys():
            result[key] += game2.get(str(key),0)

    return result


######获得当前胜利组########
def get_win():
    Userdb = db()
    win_id = Userdb.get_win()
    return win_id

##############设置胜利组#######################
def set_win(winid):
    Userdb = db()
    Userdb.set_win(winid)

def set_game_score(game_id,rank):
    Userdb = db()
    if game_id == 1:
        rank1_store = 20
        rank_store = rank1_store
    else:
        rank1_store = 16
        rank_store = rank1_store
    game_score = {}
    for i in rank:
        game_score[i] = rank_store
        rank_store -= rank1_store/4
    Userdb.set_gamewin(game_id,game_score)


######胜利组抽奖#######
def random_for_C():
    Userdb = db()
    win_id = get_win()
    if not win_id or win_id == 0:
        return
    luck_userc = list(Userdb.find({'group':int(win_id)}))
    luck_num = random.randint(0,len(luck_userc))
    while luck_userc[luck_num].get('lucktag',0) == 1:
        luck_num = random.randint(0,len(luck_userc))
    luck_userc[luck_num]['lucktag'] = 1
    Userdb.save(luck_userc[luck_num])
    return luck_userc[luck_num]

#########胜利组投票抽奖#########
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
    return luckuser

def init_all():
    Userdb = db()
    user_list = Userdb.find()
    for i in user_list:
        if i.get('name') == 'system':
            i['valid_time'] = "True"
            i['win_id'] = 0
            i['game1'] = None
            i['game2'] = None
        else:
            i['vote1'] = 0
            i['vote2'] = 0
            i['lucktag'] = 0
        Userdb.save(i)

if __name__ == "__main__":
    Userdb = db()
    user_list = Userdb.find()
    for i in user_list:
        if i.get('name') == 'system':
            continue
        i['vote1'] = random.randint(1,6)
        i['vote2'] = random.randint(1,6)
        vote(i)
    # print get_result_now()
    # set_win(3)
    # print random_for_C()
    # print random_for_vote_C()
    # print random_for_vote_C()
    # print random_for_vote_C()
    # set_game_score(1,['5','3','2','4','1'])
    # print get_result_now()
    # init_all()
    # print get_result_now()




