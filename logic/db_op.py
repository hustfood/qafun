# -*- coding: utf-8 -*-
import os
import sys
reload(sys)

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from pymongo import MongoClient
DB_CONF = {
    'ip':'',
    'port':'',
    'user':'',
    'password':'',
}

def open_db(dbname, db_conf = DB_CONF):
    import urllib
    if db_conf["user"] and db_conf["password"]:
        uri = "mongodb://%s:%s@%s:%s"%(urllib.quote(db_conf['user']),urllib.quote(db_conf['password']),db_conf['ip'],db_conf['port'])
    else:
        uri = "mongodb://%s:%s"%(db_conf['ip'],db_conf['port'])
    return MongoClient(uri)[dbname]

class MongoDB(object):
    """
    mongodb数据库操作基类
    """
    def __init__(self,db, collection):
        super(MongoDB, self).__init__()
        self.__collection = open_db(db)[collection]

    def __getattr__(self,name):
        return object.__getattribute__(self.__collection,name)

class user(MongoDB):
    def __init__(self):
        MongoDB.__init__(self,"nianhui19","user")

    def insert_user(self,user):
        self.save(user)

    def get_valid_time(self):
        system = self.find_one({'name':'system'})
        return system.get('valid_time')

    def set_valid_time(self,valid_time):
        system = self.find_one({'name':'system'})
        system['valid_time'] = valid_time
        self.save(system)

    def save_vote(self,vote_info):
        user = self.find_one({'nianhuiid':vote_info['nianhuiid']})
        user['vote1'] = vote_info['vote1']
        user['vote2'] = vote_info['vote2']
        self.save(user)

    def find_id(self):
        user_list = self.find()
        return [i['nianhuiid'] for i in user_list if i['name'] != 'system']

    def get_win(self):
        system = self.find_one({'name':'system'})
        return system.get('win_id',0)

    def set_win(self,winid):
        system = self.find_one({'name':'system'})
        system['win_id'] = winid
        self.save(system)

    def set_gamewin(self,game_id,game_score):
        system = self.find_one({'name':'system'})
        if game_id ==1:
            system['game1'] = game_score
        else:
            system['game2'] = game_score
        self.save(system)

    def get_gamewin(self):
        system = self.find_one({'name':'system'})
        return system.get('game1',None),system.get('game2',None)

    def set_temp_result(self,temp_result):
        system = self.find_one({'name':'system'})
        system['temp_result'] = temp_result
        self.save(system)

    def get_temp_result(self):
        system = self.find_one({'name':'system'})
        return system.get('temp_result',None)
#test mongodb
if __name__ == "__main__":
    a = MongoDB("nianhui19","user")
    print a
    for x in a.find():
        print x
    pass
