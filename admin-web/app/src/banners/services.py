# -*- coding: utf-8 -*-

import dateutil.parser
from app.src.utils import api_manager
from app.src.utils import constants


def get_banners(mode='unarchived'):
    params = {'mode': mode}
    url = constants.BANNER_ALL
    req = api_manager.get_request(url, params)
    banners = req.json()
    for banner in banners:
        banner['created_date'] = dateutil.parser.parse(banner['created_date'])
    return banners


def add_banners(banners):
    url = constants.BANNER_ALL
    req = api_manager.post_request(url, banners)
    return req


def view_banner(banner_id):
    url = constants.BANNER_ONE.format(banner_id=banner_id)
    req = api_manager.get_request(url)
    banner = req.json()
    banner['created_date'] = dateutil.parser.parse(banner['created_date'])
    return banner


def edit_banner(banner_id, banners):
    url = constants.BANNER_ONE.format(banner_id=banner_id)
    req = api_manager.put_request(url, banners)
    return req


def delete_banner(banner_id):
    url = constants.BANNER_ONE.format(banner_id=banner_id)
    req = api_manager.delete_request(url)
    return req


def get_archived_banners(mode='archived'):
    params = {'mode': mode}
    url = constants.BANNER_ALL
    req = api_manager.get_request(url, params)
    banners = req.json()
    for banner in banners:
        banner['created_date'] = dateutil.parser.parse(banner['created_date'])
    return banners


def restore_banners(banner_id):
    url = constants.BANNER_RESTORE.format(banner_id=banner_id)
    req = api_manager.post_request(url)
    return req


def get_images(banner_id, mode='unarchived'):
    params = {'mode': mode}
    url = constants.BANNER_IMAGE_ALL.format(banner_id=banner_id)
    req = api_manager.get_request(url, params)
    images = req.json()
    for image in images:
        image['created_date'] = dateutil.parser.parse(image['created_date'])
    return images


def add_images(banner_id, images):
    url = constants.BANNER_IMAGE_ALL.format(banner_id=banner_id)
    req = api_manager.post_request(url, images)
    print req
    return req


def view_images(banner_id, image_id):
    url = constants.BANNER_IMAGE_ONE.format(banner_id=banner_id, image_id=image_id)
    req = api_manager.get_request(url)
    image = req.json()
    image['created_date'] = dateutil.parser.parse(image['created_date'])
    return image
    

def update_images(banner_id, image_id, images):
    url = constants.BANNER_IMAGE_ONE.format(banner_id=banner_id, image_id=image_id)
    req = api_manager.put_request(url, images)
    return req


def delete_images(banner_id, image_id):
    url = constants.BANNER_IMAGE_ONE.format(banner_id=banner_id, image_id=image_id)
    req = api_manager.delete_request(url)
    return req


def get_archived_images(banner_id, mode='archived'):
    params = {'mode': mode}
    url = constants.BANNER_IMAGE_ALL.format(banner_id=banner_id)
    req = api_manager.get_request(url, params)
    images = req.json()
    for image in images:
        image['created_date'] = dateutil.parser.parse(image['created_date'])
    return images


def restore_images(banner_id, image_id):
    url = constants.BANNER_IMAGE_RESTORE.format(banner_id=banner_id, image_id=image_id)
    req = api_manager.post_request(url)
    return req