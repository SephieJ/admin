# -*- coding: utf-8 -*-

import dateutil.parser
from app.src.utils import api_manager
from app.src.utils import constants


# Get resources
def get_resources(**params):
    url = constants.RESOURCE_ALL
    if bool(params):
        params = { k:v for k, v in params.items() }
        req = api_manager.get_request(url, params)
    else:
        req = api_manager.get_request(url)
    resources = req.json()
    for resource in resources:
        if ('created_date' in resource) and (resource['created_date'] is not None):
            resource['created_date'] = dateutil.parser.parse(resource['created_date'])
        if ('deleted_date' in resource) and (resource['deleted_date'] is not None):
            resource['deleted_date'] = dateutil.parser.parse(resource['deleted_date'])
        if ('updated_date' in resource) and (resource['updated_date'] is not None):
            resource['updated_date'] = dateutil.parser.parse(resource['updated_date'])
    return resources


# View Resource
def view_resource(resource_id):
    url = constants.RESOURCE_ONE.format(resource_id=resource_id)
    req = api_manager.get_request(url)
    resource = req.json()
    resource['created_date'] = dateutil.parser.parse(resource['created_date'])
    return resource


# Delete Resource
def archive_resource(resource_id):
    url = constants.RESOURCE_ARCHIVE.format(resource_id=resource_id)
    req = api_manager.get_request(url)
    resource = req.json()
    resource['created_date'] = dateutil.parser.parse(resource['created_date'])
    return resource


# Ban Resources
def ban_resource(resource_id):
    url = constants.RESOURCE_BAN.format(resource_id=resource_id)
    req = api_manager.post_request(url)
    return req


# Accept Resources
def accept_resources(resource_id):
    url = constants.RESOURCE_ACCEPT.format(resource_id=resource_id)
    req = api_manager.post_request(url)
    print url
    return req


# Reject Resources
def reject_resources(resource_id):
    url = constants.RESOURCE_REJECT.format(resource_id=resource_id)
    req = api_manager.post_request(url)
    print url
    return req


# Restore Resource
def restore_resource(resource_id):
    url = constants.RESOURCE_RESTORE.format(resource_id=resource_id)
    req = api_manager.post_request(url)
    return req


# Delete Resource
def delete_resource(resource_id):
    url = constants.RESOURCE_BAN.format(resource_id=resource_id)
    req = api_manager.post_request(url)
    return req


# Get Wishlists
def get_wishlists_no_mode():
    url = constants.WISHLIST_ALL
    req = api_manager.get_request(url)
    wishlists = req.json()
    for wishlist in wishlists:
        wishlist['created_date'] = dateutil.parser.parse(wishlist['created_date'])
    return wishlists


def get_wishlists():
    url = constants.WISHLIST_ALL
    req = api_manager.get_request(url)
    wishlists = req.json()
    for wishlist in wishlists:
        wishlist['created_date'] = dateutil.parser.parse(wishlist['created_date'])
    return wishlists


# View Wishlists
def view_wishlists(wishlist_id):
    url = constants.WISHLIST_ONE.format(wishlist_id=wishlist_id)
    req = api_manager.get_request(url)
    wishlist = req.json()
    wishlist['created_date'] = dateutil.parser.parse(wishlist['created_date'])
    return wishlist


# Edit Wishlist
def edit_wishlist(wishlist_id, wishlists):
    url = constants.WISHLIST_ONE.format(wishlist_id=wishlist_id)
    req = api_manager.put_request(url, wishlists)
    print req
    print url
    return req


# Accept Wishlist
def accept_wishlists(wishlist_id):
    url = constants.WISHLIST_ACCEPT.format(wishlist_id=wishlist_id)
    req = api_manager.post_request(url)
    print url
    return req


# Reject Wishlist
def reject_wishlists(wishlist_id):
    url = constants.WISHLIST_REJECT.format(wishlist_id=wishlist_id)
    req = api_manager.post_request(url)
    print req
    return req



# Delete Wishlist
def delete_wishlist(wishlist_id):
    url = constants.WISHLIST_ONE.format(wishlist_id=wishlist_id)
    req = api_manager.delete_request(url)
    return req


# Archive WishList
def get_archived_wishlists(mode='archived'):
    params = {'mode': mode}
    url = constants.WISHLIST_ALL
    req = api_manager.get_request(url, params)
    wishlists = req.json()
    for wishlist in wishlists:
        wishlist['created_date'] = dateutil.parser.parse(wishlist['created_date'])
    return wishlist


# Restore WishList
def restore_wishlist(wishlist_id):
    url = constants.WISHLIST_RESTORE.format(wishlist_id=wishlist_id)
    req = api_manager.post_request(url)
    return req


# View Updated Resources
def view_updates(update_id):
    url = constants.UPDATED_ONE.format(update_id=update_id)
    req = api_manager.get_request(url)
    updates = req.json()
    for update in updates:
        update['created_date'] = dateutil.parser.parse(update['created_date'])
    return updates


# Accept Updated Resources
def accept_updates(update_id, snapshot_code):
    url = constants.UPDATED_ACCEPT.format(update_id=update_id, snapshot_code=snapshot_code)
    req = api_manager.put_request(url, update_id)
    return req


# Reject Updated Resources
def reject_updates(update_id, snapshot_code):
    url = constants.UPDATED_REJECT.format(update_id=update_id, snapshot_code=snapshot_code)
    req = api_manager.delete_request(url, update_id)
    print url
    return req


# Get Pending Wishlists
def get_pending_wishlist():
    url = constants.WISHLIST_ALL
    req = api_manager.get_request(url)
    wishlists = req.json()
    for wishlist in wishlists:
        wishlist['created_date'] = dateutil.parser.parse(wishlist['created_date'])
    return wishlists