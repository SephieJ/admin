# -*- coding: utf-8 -*-

import dateutil.parser
from app.src.utils import api_manager
from app.src.utils import constants


def get_all_admins():
    url = constants.ADMIN_ALL
    req = api_manager.get_request(url)
    admins = req.json()
    for admin in admins:
        admin['created_date'] = dateutil.parser.parse(admin['created_date'])
    return admins


def add_admin(admin):
    url = constants.ADMIN_ALL
    req = api_manager.post_request(url, admin)
    return reqview_faq


def get_admin_profile(username):
    url = constants.ADMIN_ONE.format(username=username)
    req = api_manager.get_request(url)
    admin = req.json()
    admin['created_date'] = dateutil.parser.parse(admin['created_date'])
    return admin


def edit_admin_user(username, admin):
    url = constants.ADMIN_ONE.format(username=username)
    req = api_manager.put_request(url, admin)
    return req


def delete_admin_user(username):
    url = constants.ADMIN_ONE.format(username=username)
    req = api_manager.delete_request(url)
    return req


def restore_admin_user(username):
    url = constants.ADMIN_RESTORE.format(username=username)
    req = api_manager.post_request(url)
    return req


def change_password(username, old_password, new_password, 
    confirm_password):
    
    password = {
        'old_password': old_password,
        'password': new_password,
        'confirm_password': confirm_password
    }
    url = constants.ADMIN_CHANGE.format(username=username)
    req = api_manager.put_request(url,password)
    return req
