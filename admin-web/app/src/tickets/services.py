# -*- coding: utf-8 -*-

import dateutil.parser
from app.src.utils import api_manager
from app.src.utils import constants


# Get Support Requests
def get_tickets(mode='all'):
    params = {'mode': mode}
    url = constants.TICKET_ALL
    req = api_manager.get_request(url, params)
    tickets = req.json()
    for ticket in tickets:
        ticket['created_date'] = dateutil.parser.parse(ticket['created_date'])
    return tickets


# View Support Requests
def view_tickets(ticket_id):
    url = constants.TICKET_ONE.format(ticket_id=ticket_id)
    req = api_manager.get_request(url)
    ticket = req.json()
    ticket['created_date'] = dateutil.parser.parse(ticket['created_date'])
    return ticket


# Accept Support Requests
def accept_tickets(ticket_id, support):
    url = constants.TICKET_ACCEPT.format(ticket_id=ticket_id)
    req = api_manager.put_request(url, support)
    return req


# Close Support Requests
def close_tickets(ticket_id, support):
    url = constants.TICKET_CLOSE.format(ticket_id=ticket_id)
    req = api_manager.post_request(url, support)
    return req

# Get Support chat Messages
def support_chat_messages():
    url = constants.ADMIN_SUPPORT_REQUEST.format()
    print url
    req = api_manager.get_request(url)

    return req

# Create chat Messages
def admin_support_request_create(tickets):
    url = constants.ADMIN_SUPPORT_REQUEST_CREATE
    req = api_manager.post_request(url, tickets)
    return req

# Update support chat status
def admin_support_request_update(tickets):
    url = constants.ADMIN_SUPPORT_CHAT_STATUS
    req = api_manager.put_request(url, tickets)
    return req

# Get Chat Messages Profile
def support_requests_profile(reference_code):
    url = constants.ADMIN_SUPPORT_REQUEST_PROFILE.format(reference_code=reference_code)
    req = api_manager.get_request(url)
    return req

# Get support chat convesations
def admin_support_conversations(conversations):
    url = constants.ADMIN_SUPPORT_CONVERSATION
    req = api_manager.post_request(url, conversations)
    return req
