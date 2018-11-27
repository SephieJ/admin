# -*- coding: utf-8 -*-

import dateutil.parser
from app.src.utils import api_manager
from app.src.utils import constants


def send_newsletter(email_category, emails):

    newsletter = {
        'message_type': email_category,
        'emails': emails
    }
    url = constants.INVITE_USERS
    req = api_manager.post_request(url,newsletter)
    print req
    return req
