# -*- coding: utf-8 -*-

# from flask import session
# from flask_login import login_user
import dateutil.parser
import dao
from app.src.utils import api_manager
from app.src.utils import constants
import json


def get(user_id):
    user = dao.get(user_id)
    return user


def get_all_users(**params):
    url = constants.USERT_ALL
    if bool(params):
        params = { k:v for k, v in params.items() }
        req = api_manager.get_request(url, params)
    else:
        req = api_manager.get_request(url)
    users = req.json()
    for user in users:
        user['created_date'] = dateutil.parser.parse(user['created_date'])
    return users


def get_search_or_paginate(**params):
    users = get_all_users(limit=-1, order=params.get('order'), column=params.get('column'))
    status_array = str(params.get('status')).split(',')
    filtered_users = []

    if len(status_array) > 1:
        for status in status_array:
            if params.get('has_search'):
                temp = [ 
                    user for user in users if \
                    (params.get('search_value') in "{} {}".format(user['first_name'], user['last_name']).lower() \
                    or params.get('search_value') in user['email'].lower() \
                    or params.get('search_value') in user['company']['name'].lower()) \
                    and user['status'] == status
                ]
            else:
                temp = [ user for user in users if user['status'] == status ]
            filtered_users.extend(temp)
        return filtered_users

    return filter(lambda user: user['status'] == params.get('status'), users)
    


def get_user_profile(user_id):
    url = constants.USERS_ONE.format(user_id=user_id)
    req = api_manager.get_request(url)
    user = req.json()
    user['created_date'] = dateutil.parser.parse(user['created_date'])
    if user['date_reminded']:
        user['date_reminded'] = dateutil.parser.parse(user['date_reminded'])
    
    if user.has_key('email_reminder_send_date'):
        user['email_reminder_send_date'] = dateutil.parser.parse(user['email_reminder_send_date'])
    return user


def restore_user_account(user_id):
    url = constants.USER_RESTORE.format(user_id=user_id)
    req = api_manager.post_request(url)
    return req


def ban_user_account(user_id):
    url = constants.USER_BAN.format(user_id=user_id)
    req = api_manager.post_request(url)
    return req


def deactivate_user_account(user_id):
    url = constants.USER_DEACTIVATE.format(user_id=user_id)
    req = api_manager.delete_request(url)
    return req


def resend_emails(user_email):
    # url = constants.USER_RESEND.format(user_id=user_id)
    url = constants.USER_RESEND
    req = api_manager.post_request(url, data=dict(email=user_email))
    return req
