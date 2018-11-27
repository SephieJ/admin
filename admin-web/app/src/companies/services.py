# -*- coding: utf-8 -*-

import dateutil.parser
from app.src.utils import api_manager
from app.src.utils import constants


def get_companies(mode='unarchived'):
    params = {'mode': mode}
    url = constants.COMPANIES_ALL
    req = api_manager.get_request_no_auth(url, params)
    companies = req.json()
    for company in companies:
        company['created_date'] = dateutil.parser.parse(company['created_date'])
    return companies


def add_companies(companies):
    url = constants.COMPANIES_ALL
    req = api_manager.post_request(url, companies)
    print req
    return req


def view_companies(company_id):
    url = constants.COMPANIES_ONE.format(company_id=company_id)
    req = api_manager.get_request_no_auth(url)
    company = req.json()
    company['created_date'] = dateutil.parser.parse(company['created_date'])
    return company


def edit_companies(company_id, companies):
    url = constants.COMPANIES_ONE.format(company_id=company_id)
    req = api_manager.put_request(url, companies)
    return req


def delete_companies(company_id):
    url = constants.COMPANIES_ONE.format(company_id=company_id)
    req = api_manager.delete_request(url)
    return req


def get_archived_companies(mode='archived'):
    params = {'mode': mode}
    url = constants.COMPANIES_ALL
    req = api_manager.get_request(url, params)
    companies = req.json()
    for company in companies:
        company['created_date'] = dateutil.parser.parse(company['created_date'])
    return companies


def restore_companies(company_id):
    url = constants.COMPANIES_RESTORE.format(company_id=company_id)
    req = api_manager.post_request(url)
    return req


def update_company(company_id, name, company_info, office_number,
                   website, facebook, linkedin,
                   block_street, postal_code, company_industry,
                   company_size, company_revenue,
                   years_of_incorporation, iso, bizsafe,
                   bca,
                    image_url):
    company = {
        'name': name,
        'company_info': company_info,
        'office_number': office_number,
        'website': website,
        'facebook': facebook,
        'linkedin': linkedin,
        'address': [
            {
                'block_street': block_street,
                'postal_code': postal_code,
            }
        ],
        'primary_industry': company_industry,
        'company_size': company_size,
        'company_revenue': company_revenue,
        'years_of_incorporation': years_of_incorporation,
        'iso': iso,
        'bizsafe': bizsafe,
        'bca': bca,
        'image_url': image_url
    }
    url = constants.COMPANIES_ONE.format(company_id=company_id)
    req = api_manager.put_request(url, company)
    return req
    

# def upload_image(image_base64):
#     params = {
#         'image': image_base64
#     }
#     req = api_manager.post_request(constants.IMAGE_UPLOAD, params)
#     return req
