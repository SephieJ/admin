# -*- coding: utf-8 -*-

import dateutil.parser
from app.src.utils import api_manager
from app.src.utils import constants


def send_invitation(email_category, emails):

    invitation = {
        'message_type': email_category,
        'emails': emails
    }
    url = constants.INVITE_USERS
    req = api_manager.post_request(url,invitation)
    print req
    return req

def send_emails(data_email):
    url = constants.INVITATION_ADD_EMAIL
    req = api_manager.post_request(url,data_email)
    return req

def remove_emails(email_category):
    url = constants.INVITATION_REMOVED_EMAIL.format(email_category=email_category)
    req = api_manager.get_request(url)
    return req
