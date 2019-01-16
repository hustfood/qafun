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
from logic import web_logic

blueprint = Blueprint("barrage", __name__)


@socketio.on('send barrage', namespace='/barrage')
def handle_send_barrage(param):
	try:
		say = param.get('say', '').strip()
		emit('sync barrage', say, broadcast=True, namespace='/barrage')
		return "ok"
	except Exception:
		return "error"


@socketio.on('send vote', namespace='/barrage')
def handle_send_vote(param):
	try:
		return web_logic.vote(param)
	except Exception, e:
		return "error"


@socketio.on('set win group', namespace='/barrage')
def handle_set_win_group(param):
	try:
		web_logic.set_win(param)
		emit('sync win group', param, broadcast=True, namespace='/barrage')
		return "ok"
	except Exception:
		return "error"


@socketio.on('set game sort', namespace='/barrage')
def handle_set_game_sort(param):
	try:
		web_logic.set_game_score(param['game'], param['sort'])
		return "ok"
	except Exception:
		return "error"


@socketio.on('ask win group', namespace='/barrage')
def handle_ask_win_group():
	try:
		win_group = web_logic.get_win()
		return win_group
	except Exception:
		return "error"


@socketio.on('ask win lucky', namespace='/barrage')
def handle_ask_win_lucky():
	try:
		lucky = web_logic.random_for_C()
		if not lucky:
			return {}
		return {'name': lucky['name'], 'nianhuiid': lucky['nianhuiid']}
	except Exception:
		return "error"


@socketio.on('ask vote lucky', namespace='/barrage')
def handle_ask_vote_luck():
	try:
		lucky = web_logic.random_for_vote_C()
		if not lucky:
			return {}
		return {'name': lucky['name'], 'nianhuiid': lucky['nianhuiid']}
	except Exception:
		return "error"


@socketio.on('get vote stat', namespace='/barrage')
def handle_get_vote_stat():
	try:
		return web_logic.get_result_now()
	except Exception:
		return []


@socketio.on('reset all', namespace='/barrage')
def handle_reset_all():
	try:
		web_logic.init_all()
		return "ok"
	except Exception:
		return "error"


@socketio.on('ask valid time', namespace='/barrage')
def handle_ask_valid_time():
	try:
		return web_logic.is_valid_time()
	except Exception:
		return "error"


@socketio.on('set valid time', namespace='/barrage')
def handle_set_valid_time(param):
	try:
		web_logic.set_valid_time(param)
		return "ok"
	except Exception:
		return "error"
