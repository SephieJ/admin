# -*- coding: utf-8 -*-

import dateutil.parser
from app.src.utils import api_manager
from app.src.utils import constants


def get_faqs(mode='unarchived'):
    params = {'mode': mode}
    url = constants.FAQ_ALL
    req = api_manager.get_request(url, params)
    faqs = req.json()
    for faq in faqs:
        faq['created_date'] = dateutil.parser.parse(faq['created_date'])
    return faqs


def add_faqs(faqs):
    url = constants.FAQ_ALL
    req = api_manager.post_request(url, faqs)
    return req


def view_faq(faq_id):
    url = constants.FAQ_ONE.format(faq_id=faq_id)
    req = api_manager.get_request(url)
    faq = req.json()
    faq['created_date'] = dateutil.parser.parse(faq['created_date'])
    return faq


def edit_faq(faq_id, faqs):
    url = constants.FAQ_ONE.format(faq_id=faq_id)
    req = api_manager.put_request(url, faqs)
    return req


def delete_faq(faq_id):
    url = constants.FAQ_ONE.format(faq_id=faq_id)
    req = api_manager.delete_request(url)
    return req


def get_archived_faqs(mode='archived'):
    params = {'mode': mode}
    url = constants.FAQ_ALL
    req = api_manager.get_request(url, params)
    faqs = req.json()
    for faq in faqs:
        faq['created_date'] = dateutil.parser.parse(faq['created_date'])
    return faqs


def restore_faqs(faq_id):
    url = constants.FAQ_RESTORE.format(faq_id=faq_id)
    req = api_manager.post_request(url)
    return req


def get_questions(faq_id, mode='unarchived'):
    params = {'mode': mode}
    url = constants.FAQ_QUESTION_ALL.format(faq_id=faq_id)
    req = api_manager.get_request(url, params)
    questions = req.json()
    for question in questions:
        question['created_date'] = dateutil.parser.parse(question['created_date'])
    return questions


def add_questions(faq_id, questions):
    url = constants.FAQ_QUESTION_ALL.format(faq_id=faq_id)
    req = api_manager.post_request(url, questions)
    return req


def view_questions(faq_id, question_id):
    url = constants.FAQ_QUESTION_ONE.format(faq_id=faq_id, question_id=question_id)
    req = api_manager.get_request(url)
    question = req.json()
    question['created_date'] = dateutil.parser.parse(question['created_date'])
    return question


def update_questions(faq_id, question_id, questions):
    url = constants.FAQ_QUESTION_ONE.format(faq_id=faq_id, question_id=question_id)
    req = api_manager.put_request(url, questions)
    return req


def delete_questions(faq_id, question_id):
    url = constants.FAQ_QUESTION_ONE.format(faq_id=faq_id, question_id=question_id)
    req = api_manager.delete_request(url)
    return req


def get_archived_questions(faq_id, mode='archived'):
    params = {'mode': mode}
    url = constants.FAQ_QUESTION_ALL.format(faq_id=faq_id)
    req = api_manager.get_request(url, params)
    questions = req.json()
    for question in questions:
        question['created_date'] = dateutil.parser.parse(question['created_date'])
    return questions


def restore_questions(faq_id, question_id):
    url = constants.FAQ_QUESTION_RESTORE.format(faq_id=faq_id, question_id=question_id)
    req = api_manager.post_request(url)
    return req


def sort_faqs_or_questions(sorted_list, faq_id=0):
    if faq_id:
        url = constants.QUESTIONS_ARRANGE.format(faq_id=faq_id)
    else:
        url = constants.FAQ_ARRANGE
    req = api_manager.post_request(url, sorted_list)
    return req