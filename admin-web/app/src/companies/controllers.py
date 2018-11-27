# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import login_required
import services
from app.src.utils import constants
from forms import CompanyForm
from app.src.utils import helpers
from flask import jsonify

CompanyBP = Blueprint('CompanyBP', __name__)


# Companies Page
@CompanyBP.route('/companies', methods=['GET'])
def company_page():
    companies = services.get_companies()
    return render_template("companies/index.html", companies=companies, chat_url=constants.CHAT_SUPPORT_URL)


# Add Companies Page
@CompanyBP.route('/companies/add', methods=['GET', 'POST'])
@login_required
def add_company_page():
    company_form = CompanyForm()
    if request.method == 'GET':
        return render_template("companies/add.html", company_form=company_form)
    elif request.method == 'POST':
        return jsonify({'hi':"hello"});
        if company_form.is_submitted():
            print 'ehllo'
            sanitized_inputs = helpers.sanitize(request.form)
            name = sanitized_inputs['name']
            company_info = sanitized_inputs['company_info']
            business_reg_number = sanitized_inputs['business_reg_number']
            office_number = sanitized_inputs['office_number']
            mobile_number = sanitized_inputs['mobile_number']
            accreditations = sanitized_inputs['accreditations']
            latitude = sanitized_inputs['latitude']
            longitude = sanitized_inputs['longitude']
            block_street = sanitized_inputs['block_street']
            unit_number = sanitized_inputs['unit_number']
            postal_code = sanitized_inputs['postal_code']
            companies = {
                'name': name,
                'company_info': company_info,
                'business_reg_number': business_reg_number,
                'office_number': office_number,
                'mobile_number': mobile_number,
                'accreditations': accreditations,
                'address': {
                    'latitude': latitude,
                    'longitude': longitude,
                    'block_street': block_street,
                    'unit_number': unit_number,
                    'postal_code': postal_code,
                }
            }
            # return jsonify(companies);
            add_company = services.add_companies(companies)
            if add_company.status_code == 201:
                flash(add_company.text, 'success')
                return redirect(url_for('.company_page'))
            else:
                flash(add_company.text, 'danger')
                return render_template('companies/add.html', company_form=company_form)
        else:
            return render_template('companies/add.html', company_form=company_form)


# View Company DetailYear
@CompanyBP.route('/companies/<int:company_id>', methods=['GET'])
def view_company_page(company_id):
    if request.method == 'GET':
        company = services.view_companies(company_id)

        Year = {
            'LT2Y' : '< 2 years',
            'TTOFY' : '3 - 5 years',
            'STO10Y': '6 - 10 years',
            'GT10Y': '> 10 Years',
            'N.A.': 'N.A.'
        }
        Size = {
            'LT10': '< 10',
            'TTOF': '10 - 50',
            'F1TO1H': '51 to 100',
            'H1TO2H': '101 - 200',
            'GT2H': '> 200'
        }
        #return jsonify(Size);
        return render_template('companies/show.html', company=company , Year=Year,Size=Size)


# Update Company
@CompanyBP.route('/companies/<int:company_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_company_page(company_id):
    company_form = CompanyForm()
    company = services.view_companies(company_id)
    if request.method == 'GET':
        company_form.company_info.data = company['company_info']
        #return jsonify(company);
        return render_template('companies/edit.html', company_details=company, company_form=company_form)
    elif request.method == 'POST':

        if company_form.is_submitted():
            sanitized_inputs = helpers.sanitize(request.form)
            name = sanitized_inputs['name']
            company_info = sanitized_inputs['company_info']
            office_number = sanitized_inputs['office_number']
            website = sanitized_inputs['website']
            facebook = sanitized_inputs['facebook']
            linkedin = sanitized_inputs['linkedin']
            block_street = sanitized_inputs['block_street']
            postal_code = sanitized_inputs['postal_code']
            company_industry = company_form.industry.data
            company_size = company_form.company_size.data
            company_revenue = company_form.company_revenue.data
            years_of_incorporation = company_form.company_years.data
            bizsafe = company_form.bizsafe.data
            image = request.files['image_url']
            #return jsonify(sanitized_inputs['image']);
            # name = HTMLParser.HTMLParser().unescape(name)
            # company_info = HTMLParser.HTMLParser().unescape(company_info)

            iso_arr = request.form.getlist('iso')
            iso = []
            for iso_val in iso_arr:
                iso_dict = {
                    'title': iso_val
                }
                iso.append(iso_dict)

            bca_arr = request.form.getlist('bca')
            bca = []
            for bca_val in bca_arr:
                bca_dict = {
                    'title': bca_val
                }
                bca.append(bca_dict)

            if image.filename is None:
                image_url = ''
            else:
                image_url = helpers.upload(image)

            print image_url
            # company = {
            #     'name': name,
            #     'company_info': company_info,
            #     'office_number': office_number,
            #     'address': [
            #         {
            #             'block_street': block_street,
            #             'postal_code': postal_code,
            #         }
            #     ],
            #     'primaryIndustry': company_industry,
            #     'company_size': company_size,
            #     'company_revenue': company_revenue,
            #     'years_of_incorporation': years_of_incorporation,
            #     'image_url': image_url
            # }
            print bizsafe
            print iso
            print bca
            print company_revenue
            update_company = services.update_company(
                company_id, name, company_info, office_number,
                website, facebook, linkedin, block_street,
                postal_code, company_industry, company_size,
                company_revenue, years_of_incorporation,
                iso, bizsafe, bca, image_url)
            if update_company.status_code == 202:
                flash(update_company.text, 'success')
                return redirect(url_for('.edit_company_page',
                                        company_id=company_id))
            else:
                flash('Error in Company', 'danger')
                return render_template('companies/edit.html',
                                       company=company,
                                       company_form=company_form,
                                       company_id=company_id)
        else:
            return render_template('companies/edit.html',
                                   company=company,
                                   company_form=company_form,
                                   company_id=company_id)

@CompanyBP.route('/companies/upload/images', methods=['POST'])
def upload_image():
    json_data = request.get_json()
    image_base64 = json_data['image']
    #image_base64_full = json_data['image_full']

    # CSS purposes of image upload spinner
    # style_pic_id = json_data['pic_id']
    # style_pic_wrap = json_data['pic_wrap']

    result = services.upload_image(image_base64)
    json_result = result.json()
    #json_result.update({"pic_id": style_pic_id, "pic_wrap": style_pic_wrap})
    return jsonify(json_result)

# Delete Company
@CompanyBP.route('/companies/<company_id>/delete', methods=['GET'])
@login_required
def delete_company(company_id):
    if request.method == 'GET':
        delete_company = services.delete_companies(company_id)
        if delete_company.status_code == 202:
            flash('Successfully deleted.', 'success')
        else:
            flash(delete_company.text, 'danger')
        return redirect(url_for('.company_page'))


# Archived Companies Page
@CompanyBP.route('/companies/archived', methods=['GET'])
@login_required
def archived_company_page():
    companies = services.get_archived_companies()
    return render_template("companies/archived.html", companies=companies)


# Restore Companies
@CompanyBP.route('/companies/<company_id>/restore', methods=['GET', 'POST'])
@login_required
def restore_company(company_id):
    if request.method == 'GET':
        restore_company = services.restore_companies(company_id)
        if restore_company.status_code == 202:
            flash('Successfully restored.', 'success')
        else:
            flash(restore_company.text, 'danger')
        return redirect(url_for('.archived_company_page'))
