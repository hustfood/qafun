# -*- coding: utf8 -*-

"""--------------------------------------------------------------
Author:
food
gzfujianfeng@corp.netease.com

Date:
2018/12/19

Description:

History:
2017/09/14, create file.
--------------------------------------------------------------"""

from flask import Blueprint
from flask_socketio import emit
from utils import socketio

blueprint = Blueprint("barrage", __name__)


@socketio.on('send barrage', namespace='/barrage')
def handle_set_const(param):
	try:
		say = param.get('say', '')
		emit('sync barrage', say, broadcast=True, namespace='/barrage')
		return "ok"
	except Exception:
		return "error"
