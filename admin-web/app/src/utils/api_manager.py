# -*- coding: utf-8 -*-

import requests
from flask import session


def get_request(url, data=None):
    basic_auth = session['user_basic']
    headers = {
        'Authorization': basic_auth
    }
    if data is None:
        req = requests.get(url, headers=headers)
    else:
        req = requests.get(url, params=data, headers=headers)
    return req


def post_request(url, data=None):
    basic_auth = session['user_basic']
    headers = {
        'Authorization': basic_auth
    }
    if data is None:
        req = requests.post(url, headers=headers)
    else:
        req = requests.post(url, json=data, headers=headers)
    return req


def put_request(url, data):
    basic_auth = session['user_basic']
    headers = {
        'Authorization': basic_auth
    }
    req = requests.put(url, json=data, headers=headers)
    return req


def delete_request(url, data=None):
    basic_auth = session['user_basic']
    headers = {
        'Authorization': basic_auth
    }
    if data is None:
        req = requests.delete(url, headers=headers)
    else:
        req = requests.delete(url, json=data, headers=headers)
    return req


def get_request_no_auth(url, data=None):
    if data is None:
        req = requests.get(url)
    else:
        req = requests.get(url, params=data)
    return req


def post_request_no_auth(url, data):
    req = requests.post(url, json=data)
    return req


def put_request_no_auth(url, data):
    req = requests.put(url, json=data)
    return req


def delete_request_no_auth(url):
    req = requests.delete(url)
    return req
