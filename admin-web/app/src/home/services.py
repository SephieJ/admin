# -*- coding: utf-8 -*-

from flask import session
from app.src.utils import api_manager
from app.src.utils import constants


def login(user_creds, basic_auth):
    req = api_manager.post_request_no_auth(constants.USER_LOGIN, user_creds)
    print req
    print req.text
    return req
    # if req.status_code == 200:
    #     user = User(req.json())
    #     session['user_basic'] = basic_auth
    #     login_user(user)
    # else:
    #     return req

    # if dao.get(user.id) is None:
    #     dao.add(user)
    # else:
    #     dao.update(user)
    # return req

def getAnalytics():
    return api_manager.get_request(constants.ANALYTICS_ALL)

def logout(user_id):
    # user = dao.get(user_id)
    # if user is None:
    #     dao.add(user)
    # else:
    #     dao.update(user)
    session.pop('user_basic', None)
    session.pop('current_url', None)
