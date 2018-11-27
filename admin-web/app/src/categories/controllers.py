# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, url_for, flash, redirect,jsonify
from flask_login import login_required
import services
from forms import CategoryForm, SubCategoryForm, SuggestedCategoryForm, SuggestedSubcategoryForm
from flask_login import current_user
from app.src.utils import helpers
from flask import jsonify
CategoryBP = Blueprint('CategoryBP', __name__)


# Categories Page
@CategoryBP.route('/categories', methods=['GET'])
@login_required
def category_page():
    # categories = services.get_categories()
    categories = filter(lambda category: category['status'] == 'ACTIVE', services.get_categories_no_mode())
    try:
        transactions = categories
        for transaction in transactions:
            count = 0
            for item in transaction['subcategories']:
                if item['status'] == 'PENDING':
                    count += 1
            transaction['count'] = count
    except ValueError:
        transactions = []
    return render_template("categories/index.html", categories=transactions)


# Add Category
@CategoryBP.route('/categories/add', methods=['GET', 'POST'])
@login_required
def add_category_page():
    category_form = CategoryForm()
    if request.method == 'GET':
        return render_template("categories/add.html", category_form=category_form)
    elif request.method == 'POST':
        if category_form.validate_on_submit():
            sanitized_inputs = helpers.sanitize(request.form)
            name = sanitized_inputs['name']
            description = sanitized_inputs['description']
            # image = request.files['image']
            # if image.filename is None:
            #     image_url = ''
            # else:
            #     image_url = helpers.upload(image)
            categories = {
                'name': name,
                'description': description,
                # 'image_url': image_url
            }

            ##return jsonify(categories);
            add_category = services.add_category(categories)
            if add_category.status_code == 201:
                flash(add_category.text, 'success')
                return redirect(url_for('.category_page'))
            else:
                flash(add_category.text, 'danger')
                return render_template('categories/add.html', category_form=category_form)
        else:
            return render_template('categories/add.html', category_form=category_form)


# View Category Detail
@CategoryBP.route('/categories/<int:category_id>', methods=['GET'])
@login_required
def view_category_page(category_id):
    if request.method == 'GET':
        category = services.view_category(category_id)
        # subcategories = services.get_subcategories(category_id)
        subcategories = services.get_subcategories_no_mode(category_id)
        subcategories = filter(lambda subcategory: subcategory['status'] == 'ACTIVE', subcategories)
        return render_template("categories/show.html", subcategories=subcategories, category=category)


# Update Category
@CategoryBP.route('/categories/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_category_page(category_id):
    category_form = CategoryForm()
    category = services.view_category(category_id)
    if request.method == 'GET':
        category_form.description.data = category['description']
        return render_template('categories/edit.html', category=category, category_form=category_form)
    elif request.method == 'POST':
        if category_form.validate_on_submit():
            sanitized_inputs = helpers.sanitize(request.form)
            name = sanitized_inputs['name']
            description = sanitized_inputs['description']
            # image = request.files['image']
            # if image.filename is None:
            #     image_url = ''
            # else:
            #     image_url = helpers.upload(image)

            categories = {
                'name': name,
                'description': description,
                # 'image_url': image_url
            }
            update_category = services.edit_category(category_id, categories)
            print update_category
            if update_category.status_code == 202:
                flash(update_category.text, 'success')
                return redirect(url_for('.category_page'))
            else:
                flash('Error in FAQ Category', 'danger')
                return render_template('categories/edit.html', category=category, category_form=category_form)
        else:
            return render_template('categories/edit.html', category=category, category_form=category_form)


# Delete Category
@CategoryBP.route('/categories/<int:category_id>/delete', methods=['GET'])
@login_required
def delete_category(category_id):
    if request.method == 'GET':
        delete_category = services.delete_category(category_id)
        if delete_category.status_code == 202:
            flash(delete_category.text, 'success')
            return redirect(url_for('.category_page'))
        else:
            flash(delete_category.text, 'danger')
        return redirect(url_for('.category_page'))


# Archived Category List
@CategoryBP.route('/archived/categories', methods=['GET'])
@login_required
def archived_category_page():
    # categories = services.get_archived_categories()
    categories = filter(lambda category: category['status'] == 'REJECTED' or \
                    category['status'] == 'ARCHIVED', services.get_categories_no_mode())
    return render_template("categories/archived.html", categories=categories)


# Restore Categories
@CategoryBP.route('/categories/<int:category_id>/restore', methods=['GET', 'POST'])
@login_required
def restore_category(category_id):
    if request.method == 'GET':
        restore_category = services.restore_category(category_id)
        if restore_category.status_code == 202:
            flash(restore_category.text, 'success')
            return redirect(url_for('.archived_category_page'))
        else:
            flash(restore_category.text, 'danger')
            return redirect(url_for('.archived_category_page'))


# Sub Category Page
@CategoryBP.route('/categories/<int:category_id>/subcategory', methods=['GET'])
def subcategory_page(category_id):
    if request.method == 'GET':
        subcategories = services.get_subcategories(category_id)
        category = services.view_category(category_id)
        return render_template("categories/show.html", subcategories=subcategories, category=category)


# Add Sub Category
@CategoryBP.route('/categories/<int:category_id>/add-subcategories', methods=['GET', 'POST'])
@login_required
def add_subcategory_page(category_id):
    subcategory_form = SubCategoryForm()
    category = services.view_category(category_id)
    if request.method == 'GET':
        return render_template("categories/add_subcategory.html", subcategory_form=subcategory_form, category=category)
    elif request.method == 'POST':
        if subcategory_form.validate_on_submit():
            sanitized_inputs = helpers.sanitize(request.form)
            name = sanitized_inputs['name']
            description = sanitized_inputs['description']
            subcategories = {
                'name': name,
                'description': description,
            }
            add_subcategory = services.add_subcategory(category_id, subcategories)
            print add_subcategory.status_code
            if add_subcategory.status_code == 201:
                flash(add_subcategory.text, 'success')
                return redirect(url_for('.subcategory_page', category_id=category_id, category=category))
            else:
                flash(add_subcategory.text, 'danger')
                return redirect(url_for('.add_subcategory_page', category_id=category_id, category=category))
        else:
            return render_template('categories/add_subcategory.html', subcategory_form=subcategory_form, category=category)


# View Sub Category by Category
@CategoryBP.route('/categories/<int:category_id>/view-subcategories/<int:subcategory_id>', methods=['GET'])
@login_required
def view_subcategory_page(category_id, subcategory_id):
    if request.method == 'GET':
        category = services.view_category(category_id)
        subcategory = services.view_subcategory(category_id, subcategory_id)
        return render_template("categories/show_subcategory.html", category=category, subcategory=subcategory)


# Edit SubCategory by Category
@CategoryBP.route('/categories/<int:category_id>/subcategory/<int:subcategory_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_subcategory_page(category_id, subcategory_id):
    subcategory_form = SubCategoryForm()
    subcategory = services.view_subcategory(category_id, subcategory_id)
    category = services.view_category(category_id)
    if request.method == 'GET':
        subcategory_form.description.data = subcategory['description']
        return render_template('categories/edit_subcategory.html', category=category, subcategory=subcategory, subcategory_form=subcategory_form)
    elif request.method == 'POST':
        if subcategory_form.validate_on_submit():
            sanitized_inputs = helpers.sanitize(request.form)
            name = sanitized_inputs['name']
            description = sanitized_inputs['description']
            subcategories = {
                'name': name,
                'description': description,
            }
            update_subcategory = services.update_subcategory(category_id, subcategory_id, subcategories)
            if update_subcategory.status_code == 202:
                flash(update_subcategory.text, 'success')
                return redirect(url_for('.subcategory_page', category_id=category_id))
            else:
                flash(update_subcategory.text, 'danger')
                return redirect(url_for('.edit_subcategory_page', category_id=category_id, subcategory_id=subcategory_id))
        else:
            return render_template('categories/edit_subcategory.html', category=category, subcategory_form=subcategory_form, subcategory=subcategory)


# Delete Sub Category by Category
@CategoryBP.route('/categories/<int:category_id>/subcategory/<int:subcategory_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_subcategory(category_id, subcategory_id):
    if request.method == 'GET':
        delete_subcategory = services.delete_subcategory(category_id, subcategory_id)
        if delete_subcategory.status_code == 202:
            flash(delete_subcategory.text, 'success')
        else:
            flash(delete_subcategory.text, 'danger')
        return redirect(url_for('.subcategory_page', category_id=category_id))


# Archived Sub Category
@CategoryBP.route('/categories/<int:category_id>/archived-subcategories', methods=['GET'])
@login_required
def archived_subcategory_page(category_id):
    if request.method == 'GET':
        category = services.view_category(category_id)
        # subcategories = services.get_archived_subcategory(category_id)
        # print subcategories
        subcategories = services.get_subcategories_no_mode(category_id)
        subcategories = filter(lambda subcategory: subcategory['status'] == 'ARCHIVED' or \
                            subcategory['status'] == 'REJECTED', subcategories)
        return render_template("categories/archived_subcategory.html", category=category, subcategories=subcategories)


# Restore Sub Category by Category
@CategoryBP.route('/categories/<int:category_id>/subcategory<int:subcategory_id>/restore', methods=['GET', 'POST'])
@login_required
def restore_subcategory(category_id, subcategory_id):
    if request.method == 'GET':
        restore_subcategory = services.restore_subcategory(category_id, subcategory_id)
        if restore_subcategory.status_code == 202:
            flash(restore_subcategory.text, 'success')
        else:
            flash(restore_subcategory.text, 'danger')
        return redirect(url_for('.subcategory_page', category_id=category_id))


# Suggested Category Page
@CategoryBP.route('/suggested-categories', methods=['GET'])
@login_required
def suggested_page():
    # suggested_categories = services.get_suggested()
    suggested_categories = services.get_suggested_no_mode()
    suggested_categories = filter(lambda suggested_category: suggested_category['status'] == 'PENDING' \
                            , suggested_categories)
    return render_template('categories/index_suggested.html', suggested_categories=suggested_categories)


# View Suggested Detail
@CategoryBP.route('/suggested-categories/<int:category_id>', methods=['GET'])
@login_required
def view_suggested_page(category_id):
    suggested_category_form = SuggestedCategoryForm()
    suggested_subcategory_form = SuggestedSubcategoryForm()
    if request.method == 'GET':
        suggested_category = services.view_suggested_category(category_id, mode='pending')
        suggested_subcategories = services.get_suggested_subcategories(category_id, mode='pending')
        return render_template("categories/show_suggested.html",
                               suggested_category=suggested_category,
                               suggested_subcategories=suggested_subcategories,
                               suggested_category_form=suggested_category_form,
                               suggested_subcategory_form=suggested_subcategory_form)


# Accept Suggested Category
@CategoryBP.route('/suggested-categories/<int:category_id>/accept', methods=['GET', 'POST'])
@login_required
def accept_suggested_category(category_id):
    suggested_category_form = SuggestedCategoryForm()
    suggested_category = services.view_suggested_category(category_id)
    if request.method == 'GET':
        return render_template('categories/show_suggested.html',
                               suggested_category_form=suggested_category_form,
                               suggested_category=suggested_category)
    elif request.method == 'POST':
        accept_suggested_cat = services.accept_suggested_cat(category_id)
        print accept_suggested_cat
        if accept_suggested_cat.status_code == 202:
            flash('Suggested Category successfully accepted', 'success')
            return redirect(url_for('.view_suggested_page', category_id=category_id))
        else:
            flash('Error in accepting suggested category', 'danger')
            return redirect(url_for('view_suggested_page', category_id=category_id))
    else:
        return render_template('categories/show_suggested.html',
                                suggested_category=suggested_category,
                                suggested_category_form=suggested_category_form)



# Accept Suggested Sub Category
@CategoryBP.route('/suggested-categories/<int:category_id>/subcategories/<int:subcategory_id>/accept', methods=['GET', 'POST'])
@login_required
def accept_suggested_subcategory(category_id, subcategory_id):
    suggested_subcategory_form = SuggestedSubcategoryForm()
    suggested_subcategory = services.get_suggested_subcategories(category_id, subcategory_id)
    if request.method == 'GET':
        return render_template('categories/show_suggested.html',
            suggested_subcategory_form=suggested_subcategory_form,
            suggested_subcategory=suggested_subcategory,
            suggested_category_form=suggested_category_form)
    elif request.method == 'POST':
        accept_suggested_subcat = services.accept_suggested_subcat(category_id, subcategory_id)
        print accept_suggested_subcat
        if accept_suggested_subcat.status_code == 202:
            flash('Suggested Sub Category successfully accepted', 'success')
            return redirect(url_for('.view_suggested_page',
                            category_id=category_id))
        else:
            flash('Error in accepting Sub Category', 'danger')
            return redirect(url_for('.view_suggested_page', category_id=category_id))
    else:
        return render_template('categories/show_suggested.html',
                            suggested_subcategory=suggested_subcategory,
                            suggested_subcategory_form=suggested_subcategory_form,
                            suggested_category_form=suggested_category_form)



# Reject Suggested Sub Category
@CategoryBP.route('/suggested-categories/<int:category_id>/subcategories/<int:subcategory_id>/reject', methods=['GET', 'POST'])
@login_required
def reject_suggested_subcategory(category_id, subcategory_id):
    suggested_subcategory_form = SuggestedSubcategoryForm()
    suggested_subcategory = services.get_suggested_subcategories(category_id, subcategory_id)
    if request.method == 'GET':
        return render_template('categories/show_suggested.html',
            suggested_subcategory_form=suggested_subcategory_form,
            suggested_subcategory=suggested_subcategory,
            suggested_category_form=suggested_category_form)
    elif request.method == 'POST':
        reject_suggested_subcat = services.reject_suggested_subcat(category_id, subcategory_id)
        print reject_suggested_subcat
        if reject_suggested_subcat.status_code == 202:
            flash('Suggested Sub Category successfully rejected', 'success')
            return redirect(url_for('.view_suggested_page',
                            category_id=category_id))
        else:
            flash('Error in rejecting Sub Category', 'danger')
            return redirect(url_for('.view_suggested_page', category_id=category_id))
    else:
        return render_template('categories/show_suggested.html',
                            suggested_subcategory=suggested_subcategory,
                            suggested_subcategory_form=suggested_subcategory_form,
                            suggested_category_form=suggested_category_form)



# Reject Suggested Category
@CategoryBP.route('/suggested-categories/<int:category_id>/reject', methods=['GET', 'POST'])
@login_required
def reject_suggested_category(category_id):
    suggested_category_form = SuggestedCategoryForm()
    suggested_category = services.view_suggested_category(category_id)
    if request.method == 'GET':
        return render_template('categories/show_suggested.html',
                                suggested_category=suggested_category,
                                suggested_category_form=suggested_category_form)
    elif request.method == 'POST':
        reject_suggested_cat = services.reject_suggested_cat(category_id)
        print reject_suggested_cat
        if reject_suggested_cat.status_code == 202:
            flash('Suggested Category successfully rejected.', 'success')
            return redirect(url_for('.view_suggested_page', category_id=category_id))
        else:
            flash('Error in rejecting suggested page', 'danger')
            return redirect(url_for('.view_suggested_page', category_id=category_id))
    else:
        return render_template('categories/show_suggested.html',
                                suggested_category=suggested_category,
                                suggested_category_form=suggested_category_form)



@CategoryBP.route('/categories/upload/images', methods=['POST'])
def upload_image():
    json_data = request.get_json()
    image_base64 = json_data['image']

    # CSS purposes of image upload spinner
    # style_pic_id = json_data['pic_id']
    # style_pic_wrap = json_data['pic_wrap']

    result = services.upload_image(image_base64)
    print result

    json_result = result.json()
    print json_result
    # json_result.update({"pic_id": style_pic_id, "pic_wrap": style_pic_wrap})
    return jsonify(json_result)
