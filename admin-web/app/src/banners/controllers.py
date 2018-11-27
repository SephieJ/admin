# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import login_required
import services
from forms import BannersForm, ImagesForm
from app.src.utils import helpers

BannerBP = Blueprint('BannerBP', __name__)


# Banners Page
@BannerBP.route('/banners', methods=['GET'])
@login_required
def banner_page():
    banners = services.get_banners()
    return render_template("banners/index.html", banners=banners)


# Add Banners
@BannerBP.route('/banners/add', methods=['GET', 'POST'])
@login_required
def add_banner_page():
    banners_form = BannersForm()
    if request.method == 'GET':
        return render_template("banners/add.html", banners_form=banners_form)
    elif request.method == 'POST':
        if banners_form.validate_on_submit():
            sanitized_inputs = helpers.sanitize(request.form)
            name = sanitized_inputs['name']
            description = sanitized_inputs['description']
            banners = {
                'name': name,
                'description': description
            }
            add_banner = services.add_banners(banners)
            if add_banner.status_code == 201:
                flash(add_banner.text, 'success')
                return redirect(url_for('.banner_page'))
            else:
                flash('Error in Banner', 'danger')
                return render_template('banners/add.html', banners_form=banners_form)
        else:
            return render_template('banners/add.html', banners_form=banners_form)


# View Banner Detail
@BannerBP.route('/banners/<int:banner_id>', methods=['GET'])
@login_required
def view_banner_page(banner_id):
    if request.method == 'GET':
        banner = services.view_banner(banner_id)
        images = services.get_images(banner_id)
        banner = services.view_banner(banner_id)
        return render_template("banners/show.html", images=images, banner=banner)


# Update Banner
@BannerBP.route('/banners/<int:banner_id>/edit', methods=['GET','POST'])
@login_required
def update_banner_page(banner_id):
    banners_form = BannersForm()
    banner = services.view_banner(banner_id)
    if request.method == 'GET':
        banners_form.description.data = banner['description']
        return render_template('banners/edit.html', banner=banner, banners_form=banners_form)
    elif request.method == 'POST':
        if banners_form.validate_on_submit():
            sanitized_inputs = helpers.sanitize(request.form)
            name = sanitized_inputs['name']
            description = sanitized_inputs['description']
            banners = {
                'name': name,
                'description': description
            }
            update_banner = services.edit_banner(banner_id, banners)
            if update_banner.status_code == 202:
                flash(update_banner.text, 'success')
                return redirect(url_for('.banner_page'))
            else:
                flash('Error in Banner', 'danger')
                return render_template('banners/edit.html', banner=banner, banners_form=banners_form)
        else:
            return render_template('banners/edit.html', banner=banner, banners_form=banners_form)


# Delete Banners
@BannerBP.route('/banners/<int:banner_id>/delete', methods=['GET'])
@login_required
def delete_banner(banner_id):
    if request.method == 'GET':
        delete_banner = services.delete_banner(banner_id)
        if delete_banner.status_code == 202:
            flash(delete_banner.text, 'success')
            return redirect(url_for('.banner_page'))
        else:
            flash(delete_banner.text, 'danger')
        return redirect(url_for('.banner_page'))


# Archived Banners Page
@BannerBP.route('/banners/archived', methods=['GET'])
@login_required
def archived_banner_page():
    banners = services.get_archived_banners()
    return render_template("banners/archived.html", banners=banners)


# Restore Banners
@BannerBP.route('/banners/<int:banner_id>/restore', methods=['GET', 'POST'])
@login_required
def restore_banner(banner_id):
    if request.method == 'GET':
        restore_banner = services.restore_banners(banner_id)
        if restore_banner.status_code == 202:
            flash('Successfully restored.', 'success')
        else:
            flash(restore_banner.text, 'danger')
        return redirect(url_for('.archived_banner_page'))


# Images Page
@BannerBP.route('/banners/<int:banner_id>/images', methods=['GET'])
def image_page(banner_id):
    if request.method == 'GET':
        images = services.get_images(banner_id)
        banner = services.view_banner(banner_id)
        return render_template("banners/show.html", images=images, banner=banner)


# Add Images
@BannerBP.route('/banners/<int:banner_id>/add-images', methods=['GET', 'POST'])
@login_required
def add_image_page(banner_id):
    images_form = ImagesForm()
    banner = services.view_banner(banner_id)
    if request.method == 'GET':
        return render_template("banners/add_images.html", images_form=images_form, banner=banner)
    elif request.method == 'POST':
        if images_form.validate_on_submit():
            sanitized_inputs = helpers.sanitize(request.form)
            name = sanitized_inputs['name']
            image_link = sanitized_inputs['image_link']
            image = request.files['image']
            if image.filename is None:
                image_url = ''
            else:
                image_url = helpers.upload(image)
            images = {
                'name': name,
                'image_url': image_url,
                'image_link': image_link
            }
            add_image = services.add_images(banner_id, images)
            if add_image.status_code == 201:
                flash(add_image.text, 'success')
                return redirect(url_for('.image_page', banner_id=banner_id))
            else:
                flash(add_image.text, 'danger')
                return redirect(url_for('.add_image_page', banner_id=banner_id))
        else:
            return render_template('banners/add_images.html', images_form=images_form, banner=banner)


# View Images by Banner
@BannerBP.route('/banners/<int:banner_id>/view-images/<int:image_id>', methods=['GET'])
@login_required
def view_image_page(banner_id, image_id):
    if request.method == 'GET':
        image = services.view_images(banner_id, image_id)
        banner = services.view_banner(banner_id)
        return render_template("banners/show_images.html", image=image, banner=banner, banner_id=banner_id)


# Edit Images by Banner
@BannerBP.route('/banners/<int:banner_id>/image/<int:image_id>/edit', methods=['GET','POST'])
@login_required
def edit_image_page(banner_id, image_id):
    images_form = ImagesForm()
    image = services.view_images(banner_id, image_id)
    banner = services.view_banner(banner_id)
    if request.method == 'GET':
        return render_template('banners/edit_images.html', banner=banner, image=image, images_form=images_form)
    elif request.method == 'POST':
        if images_form.validate_on_submit():
            sanitized_inputs = helpers.sanitized(request.form)
            name = sanitized_inputs['name']
            image_link = sanitized_inputs['image_link']
            image = request.files['image']
            if image.filename is None:
                image_url = '' 
            else:
                image_url = helpers.upload(image)
            images = {
                'name': name,
                'image_url': image_url,
                'image_link': image_link
            }
            print update_image
            update_image = services.update_images(banner_id, image_id, images)
            if update_image.status_code == 202:
                flash(update_image.text, 'success')
                return redirect(url_for('.image_page', banner_id=banner_id))
            else:
                flash(update_image.text, 'danger')
                return redirect(url_for('.edit_image_page', banner_id=banner_id, image_id=image_id))
        else:
            return render_template('banners/edit_images.html', images_form=images_form, banner=banner, image=image)

# Delete Images by Banner
@BannerBP.route('/banners/<int:banner_id>/image/<int:image_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_images(banner_id, image_id):
    if request.method == 'GET':
        delete_image = services.delete_images(banner_id, image_id)
        if delete_image.status_code == 202:
            flash(delete_image.text, 'success')
        else:
            flash(delete_image.text, 'danger')
        return redirect(url_for('.image_page', banner_id=banner_id))

# Archived Images Page
@BannerBP.route('/banners/<int:banner_id>/archived-images', methods=['GET'])
@login_required
def archived_image_page(banner_id):
    if request.method == 'GET':
        images = services.get_archived_images(banner_id)
        banner = services.view_banner(banner_id)
        return render_template("banners/archived_images.html", images=images, banner=banner)

# Restore Images by Banners
@BannerBP.route('/banners/<int:banner_id>/image/<int:image_id>/restore', methods=['GET', 'POST'])
@login_required
def restore_image_page(banner_id, image_id):
    if request.method == 'GET':
        restore_image = services.restore_images(banner_id, image_id)
        if restore_image.status_code == 202:
            flash(restore_image.text, 'success')
        else:
            flash(restore_image.text, 'danger')
        return redirect(url_for('.image_page', banner_id=banner_id))
