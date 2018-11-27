# -*- coding: utf-8 -*-

import dateutil.parser
from app.src.utils import api_manager
from app.src.utils import constants


# Categories Module
def get_categories_no_mode():
    url = constants.CATEGORIES_ALL
    req = api_manager.get_request(url)
    categories = req.json()
    for category in categories:
        category['created_date'] = dateutil.parser.parse(category['created_date'])
    return categories

def get_categories(mode='unarchived'):
    params = {'mode': mode}
    url = constants.CATEGORIES_ALL
    req = api_manager.get_request(url, params)
    categories = req.json()
    for category in categories:
        category['created_date'] = dateutil.parser.parse(category['created_date'])
    return categories


def add_category(categories):
    url = constants.CATEGORIES_ALL
    req = api_manager.post_request(url, categories)
    return req


def view_category(category_id):
    url = constants.CATEGORIES_ONE.format(category_id=category_id)
    req = api_manager.get_request(url)
    category = req.json()
    category['created_date'] = dateutil.parser.parse(category['created_date'])
    return category


def edit_category(category_id, categories):
    url = constants.CATEGORIES_ONE.format(category_id=category_id)
    req = api_manager.put_request(url, categories)
    return req


def delete_category(category_id):
    url = constants.CATEGORIES_ONE.format(category_id=category_id)
    req = api_manager.delete_request(url)
    return req


def get_archived_categories(mode='archived'):
    params = {'mode': mode}
    url = constants.CATEGORIES_ALL
    req = api_manager.get_request(url, params)
    categories = req.json()
    for category in categories:
        category['created_date'] = dateutil.parser.parse(category['created_date'])
    return categories


def restore_category(category_id):
    url = constants.CATEGORIES_RESTORE.format(category_id=category_id)
    req = api_manager.post_request(url)
    return req


# Subcategories Module
def get_subcategories_no_mode(category_id):
    url = constants.SUBCATEGORIES_ALL.format(category_id=category_id)
    req = api_manager.get_request(url)
    subcategories = req.json()
    for subcategory in subcategories:
        subcategory['created_date'] = dateutil.parser.parse(subcategory['created_date'])
    return subcategories

def get_subcategories(category_id, mode='unarchived'):
    params = {'mode': mode}
    url = constants.SUBCATEGORIES_ALL.format(category_id=category_id)
    req = api_manager.get_request(url, params)
    subcategories = req.json()
    for subcategory in subcategories:
        subcategory['created_date'] = dateutil.parser.parse(subcategory['created_date'])
    return subcategories


def add_subcategory(category_id, subcategories):
    url = constants.SUBCATEGORIES_ALL.format(category_id=category_id)
    req = api_manager.post_request(url, subcategories)
    return req


def view_subcategory(category_id, subcategory_id):
    url = constants.SUBCATEGORIES_ONE.format(category_id=category_id, subcategory_id=subcategory_id)
    req = api_manager.get_request(url)
    subcategory = req.json()
    subcategory['created_date'] = dateutil.parser.parse(subcategory['created_date'])
    return subcategory


def update_subcategory(category_id, subcategory_id, subcategories):
    url = constants.SUBCATEGORIES_ONE.format(category_id=category_id, subcategory_id=subcategory_id)
    req = api_manager.put_request(url, subcategories)
    return req


def delete_subcategory(category_id, subcategory_id):
    url = constants.SUBCATEGORIES_ONE.format(category_id=category_id, subcategory_id=subcategory_id)
    req = api_manager.delete_request(url)
    return req


def get_archived_subcategory(category_id, mode='archived'):
    params = {'mode': mode}
    url = constants.SUBCATEGORIES_ALL.format(category_id=category_id)
    req = api_manager.get_request(url, params)
    subcategories = req.json()
    for subcategory in subcategories:
        subcategory['created_date'] = dateutil.parser.parse(subcategory['created_date'])
    return subcategories


def restore_subcategory(category_id, subcategory_id):
    url = constants.SUBCATEGORIES_RESTORE.format(category_id=category_id, subcategory_id=subcategory_id)
    req = api_manager.post_request(url)
    return req


# Suggested Categories
def get_suggested_no_mode():
    url = constants.CATEGORIES_ALL
    req = api_manager.get_request(url)
    suggested_categories = req.json()
    for suggested_category in suggested_categories:
        suggested_category['created_date'] = dateutil.parser.parse(suggested_category['created_date'])
    return suggested_categories

def get_suggested(mode='pending'):
    params = {'mode': mode}
    url = constants.CATEGORIES_ALL
    req = api_manager.get_request(url, params)
    suggested_categories = req.json()
    for suggested_category in suggested_categories:
        suggested_category['created_date'] = dateutil.parser.parse(suggested_category['created_date'])
    return suggested_categories


def view_suggested_category(category_id, mode='pending'):
    params = {'mode': mode}
    url = constants.CATEGORIES_ONE.format(category_id=category_id)
    req = api_manager.get_request(url, params)
    suggested_category = req.json()
    suggested_category['created_date'] = dateutil.parser.parse(suggested_category['created_date'])
    return suggested_category


def get_suggested_subcategories(category_id, mode='pending'):
    params = {'mode': mode}
    url = constants.SUBCATEGORIES_ALL.format(category_id=category_id)
    req = api_manager.get_request(url, params)
    suggested_subcategories = req.json()
    for suggested_subcategory in suggested_subcategories:
        suggested_subcategory['created_date'] = dateutil.parser.parse(suggested_subcategory['created_date'])
    return suggested_subcategories


# Accept Suggest Category
def accept_suggested_cat(category_id):
    url = constants.CATEGORIES_ACCEPT.format(category_id=category_id)
    req = api_manager.post_request(url)
    return req


# Accept Suggested Subcategory
def accept_suggested_subcat(category_id, subcategory_id):
    url = constants.SUBCATEGORIES_ACCEPT.format(category_id=category_id, subcategory_id=subcategory_id)
    req = api_manager.post_request(url)
    return req


# Reject Suggested Category
def reject_suggested_cat(category_id):
    url = constants.CATEGORIES_REJECT.format(category_id=category_id)
    req = api_manager.post_request(url)
    return req


# Reject Suggested Subcategory
def reject_suggested_subcat(category_id, subcategory_id):
    url = constants.SUBCATEGORIES_REJECT.format(category_id=category_id, subcategory_id=subcategory_id)
    req = api_manager.post_request(url)
    return req



def upload_image(image_base64):
    params = {
        'image': image_base64,
    }
    req = api_manager.post_request(constants.IMAGE_UPLOAD, params)
    return req



