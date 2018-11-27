    # -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, url_for, flash, redirect , jsonify
from flask_login import login_required
import services
from forms import ResourceForm, WishlistForm, UpdateForm
from app.src.utils import helpers
from flask import jsonify
import time
import traceback



ResourceBP = Blueprint('ResourceBP', __name__)


# Resources Page
@ResourceBP.route('/resources', methods=['GET'])
@login_required
def resource_page():
    resources = services.get_resources(mode='unarchived')
    return render_template("resources/index.html", resources=resources)


# View Resource Detail
@ResourceBP.route('/resource/<int:resource_id>', methods=['GET'])
@login_required
def view_resource_page(resource_id):
    resource_form = ResourceForm()
    if request.method == 'GET':
        resource = services.view_resource(resource_id)
        return render_template('resources/show.html',
                               resource=resource,
                               resource_form=resource_form)

# Ban Resource
@ResourceBP.route('/resource/<int:resource_id>/ban', methods=['POST'])
@login_required
def ban_resource(resource_id):
    resource_form = ResourceForm()
    resource = services.view_resource(resource_id)
    if request.method == 'GET':
        return render_template('resources/show.html',
                               resource=resource,
                               resource_form=resource_form)
    elif request.method == 'POST':
        if resource_form.validate():
            ban_resource = services.ban_resource(resource_id)
            if ban_resource.status_code == 202:
                # flash('Successfully banned.', 'success')
                return redirect(url_for('.view_resource_page',
                                        resource_id=resource_id))
            else:
                # flash('Error in banning resource', 'danger')
                return redirect(url_for('.view_resource_page',
                                        resource_id=resource_id))
        else:
            return render_template('resources/show.html',
                                   resource=resource,
                                   resource_form=resource_form)

# Accept Resource
@ResourceBP.route('/resource/<int:resource_id>/accept', methods=['GET','POST'])
@login_required
def accept_resource(resource_id):
    resource_form = ResourceForm()
    resource = services.view_resource(resource_id)
    if request.method == 'GET':
        return render_template('resources/show.html',resource_form=resource_form, resource=resource)
    elif request.method == 'POST':
        #return jsonify(resource)
        accept_resource = services.accept_resources(resource_id)
        print accept_resource.status_code
        if accept_resource.status_code == 202:
            flash('Resource successfully accepted', 'success')
            return redirect(url_for('.resource_page'))
        else:
            flash('Error in accepting resource', 'danger')
            return redirect(url_for('.resource_page'))
    else:
        return render_template('resources/show.html',
                               resource_form=resource_form, resource=resource)


# Reject Resource
@ResourceBP.route('/resource/<int:resource_id>/reject', methods=['POST'])
@login_required
def reject_resource(resource_id):
    resource_form = ResourceForm()
    resource = services.view_resource(resource_id)
    if request.method == 'GET':
        return render_template('resources/show.html',resource_form=resource_form, resource=resource)
    elif request.method == 'POST':
        reject_resource = services.reject_resources(resource_id)
        print reject_resource.status_code
        if reject_resource.status_code == 202:
            flash('Resource successfully rejected', 'success')
            return redirect(url_for('.resource_page'))
        else:
            flash('Error in accepting resource', 'danger')
            return redirect(url_for('.resource_page'))
    else:
        return render_template('resources/show.html',
                               resource_form=resource_form, resource=resource)

# Delete Resource
@ResourceBP.route('/resource/<int:resource_id>/delete', methods=['GET','POST'])
@login_required
def delete_resource(resource_id):
    #return jsonify(resource_id)
    if request.method == 'POST':
        delete_resource = services.delete_resource(resource_id)
        if delete_resource.status_code == 202:
            flash(delete_resource.text, 'success')
            return redirect(url_for('.resource_page'))
        else:
            flash(delete_resource.text, 'danger')
        return redirect(url_for('.resource_page'))


# Archived Resource List
@ResourceBP.route('/archived/resources', methods=['GET'])
@login_required
def archived_resource_page():
    resources = services.get_resources(mode='rejected')
    resources.extend(services.get_resources(mode='archived'))
    return render_template("resources/archived.html", resources=resources)


# Restore Resource
@ResourceBP.route('/resource/<int:resource_id>/restore', methods=['GET', 'POST'])
@login_required
def restore_resource(resource_id):
    if request.method == 'GET':
        restore_resource = services.restore_resource(resource_id)
        if restore_resource.status_code == 202:
            flash(restore_resource.text, 'success')
            return redirect(url_for('.archived_resource_page'))
        else:
            flash(restore_resource.text, 'danger')
            return redirect(url_for('.archived_resource_page'))


# Wishlists Page
@ResourceBP.route('/wishlists', methods=['GET'])
@login_required
def wishlist_page():
    #wishlists = services.get_wishlists()
    wishlists = filter(lambda wishlist: wishlist['status'] == 'ACTIVE', services.get_wishlists_no_mode())
    return render_template("resources/indexwl.html", wishlists=wishlists)


# View Wishlists Detail
@ResourceBP.route('/wishlist/<int:wishlist_id>', methods=['GET'])
@login_required
def view_wishlist_page(wishlist_id):
    wishlist_form = WishlistForm()
    if request.method == 'GET':
        wishlist = services.view_wishlists(wishlist_id)
        wishlist = services.view_wishlists(wishlist_id)
        return render_template('resources/showwl.html', wishlist=wishlist, wishlist_form=wishlist_form)


# Edit Wishlists
@ResourceBP.route('/wishlist/<int:wishlist_id>/edit', methods=['GET','POST'])
@login_required
def edit_wishlist_page(wishlist_id):
  wishlist_form = WishlistForm()
  wishlist = services.view_wishlists(wishlist_id)
  if request.method == 'GET':
    wishlist_form.description.data = wishlist['description']
    return render_template('resources/editwl.html', wishlist=wishlist, wishlist_form=wishlist_form)
  elif request.method == 'POST':
    if wishlist_form.validate_on_submit():
        sanitized_inputs = helpers.sanitize(request.form)
        name = sanitized_inputs['name']
        description = sanitized_inputs['description']
        wishlists = {
        'name': name,
        'description': description
        }
        edit_wishlist = services.edit_wishlist(wishlist_id, wishlists)
        print (type(wishlist_id))
        print (type(wishlists))
        print edit_wishlist
        if edit_wishlist.status_code == 202:
          flash(edit_wishlist.text, 'success')
          return redirect(url_for('.wishlist_page'))
        else:
          flash('Error in editing wishlist', 'danger')
          return render_template('resources/editwl.html', wishlist=wishlist, wishlist_form=wishlist_form)
    else:
      return render_template('resources/editwl.html', wishlist=wishlist, wishlist_form=wishlist_form)


# Accept Wishlist
@ResourceBP.route('/wishlist/<int:wishlist_id>/accept', methods=['GET','POST'])
@login_required
def accept_wishlist(wishlist_id):
    wishlist_form = WishlistForm()
    wishlist = services.view_wishlists(wishlist_id)
    if request.method == 'GET':
        return render_template('resources/showwl.html',wishlist_form=wishlist_form, wishlist=wishlist)
    elif request.method == 'POST':
        accept_wishlist = services.accept_wishlists(wishlist_id)
        print accept_wishlist.status_code
        if accept_wishlist.status_code == 202:
            flash('Wishlist successfully accepted', 'success')
            return redirect(url_for('.wishlist_page'))
        else:
            flash('Error in accepting wishlist', 'danger')
            return redirect(url_for('.wishlist_page'))
    else:
        return render_template('resources/showwl.html',
                               wishlist=wishlist,
                               wishlist_form=wishlist_form)


# Reject Wishlist
@ResourceBP.route('/wishlist/<int:wishlist_id>/reject', methods=['POST'])
@login_required
def reject_wishlist(wishlist_id):
    wishlist_form = WishlistForm()
    wishlist = services.view_wishlists(wishlist_id)
    if request.method == 'GET':
        return render_template('resources/showwl.html',wishlist_form=wishlist_form, wishlist=wishlist)
    elif request.method == 'POST':
        reject_wishlist = services.reject_wishlists(wishlist_id)
        print reject_wishlist.status_code
        if reject_wishlist.status_code == 202:
            flash('Wishlist successfully rejected', 'success')
            return redirect(url_for('.wishlist_page'))
        else:
            flash('Error in accepting wishlist', 'danger')
            return redirect(url_for('.wishlist_page'))
    else:
        return render_template('resources/showwl.html',
                               wishlist=wishlist,
                               wishlist_form=wishlist_form)


# Delete Wishlist
@ResourceBP.route('/wishlist/<wishlist_id>/delete', methods=['GET'])
@login_required
def delete_wishlist_page(wishlist_id):
    if request.method == 'GET':
        delete_wishlist = services.delete_wishlist(wishlist_id)
        if delete_wishlist.status_code == 202:
            flash('Wishlist successfully deleted', 'success')
            return redirect(url_for('.wishlist_page'))
        else:
            flash('Error in deleting wishlist', 'danger')
        return redirect(url_for('.wishlist_page'))


# Archive Wishlist
@ResourceBP.route('/wishlist/archived', methods=['GET'])
@login_required
def archived_wishlist_page():
    #wishlists = services.get_archived_wishlists()
    wishlists = filter(lambda wishlist: wishlist['status'] == 'REJECTED' or \
    wishlist['status'] == 'BANNED' or wishlist['status'] == 'ARCHIVED', services.get_wishlists())
    return render_template("resources/archivedwl.html", wishlists=wishlists)


# Restore Wishlist
@ResourceBP.route('/wishlist/<wishlist_id>/restore', methods=['GET', 'POST'])
@login_required
def restore_wishlist(wishlist_id):
    if request.method == 'GET':
        restore_wishlist = services.restore_wishlists(wishlist_id)
        if restore_wishlist.status_code == 202:
            flash('Successfully restored.', 'success')
        else:
            flash(restore_wishlist.text, 'danger')
        return redirect(url_for('.archived_wishlist_page'))
            


# Updated Resources Page
@ResourceBP.route('/updates', methods=['GET'])
@login_required
def update_page():
    updates = services.get_resources(mode='unarchived')
    return render_template("resources/updated_index.html", updates=updates)


# View Updated Resource List Detail
@ResourceBP.route('/updates/<int:update_id>', methods=['GET'])
@login_required
def view_update_page(update_id):
    update_form = UpdateForm()
    if request.method == 'GET':
        updates = services.view_updates(int(update_id))
        for updated in updates:
            update = updated
            return render_template('resources/updated_show.html', update=update, update_form=update_form)



# Accept Updated Resource List
@ResourceBP.route('/updates/<int:update_id>/accept', methods=['GET', 'POST'])
@login_required
def accept_update(update_id):
    update_form = UpdateForm()
    update = services.view_resource(update_id)
    if request.method == 'GET':
        return render_template('resources/updated_show.html', update_form=update_form, update=update)
    elif request.method == 'POST':
        snapshot_code = update['snapshot_code']
        accept_update = services.accept_updates(update_id , snapshot_code)
        if accept_update.status_code == 202:
            flash('Update successfully accepted', 'success')
            return redirect(url_for('.update_page'))
        else:
            flash('Error in accepting update', 'danger')
            return redirect(url_for('.update_page'))
    else:
        return render_template('resources/updated_show.html',
                               update_form=update_form, update=update)


# Reject Updated Resource List
@ResourceBP.route('/updates/<int:update_id>/reject', methods=['POST'])
@login_required
def reject_update(update_id):
    update_form = UpdateForm()
    update = services.view_resource(update_id)
    if request.method == 'GET':
        return render_template('resources/updated_show.html', update_form=update_form, update=update)
    elif request.method == 'POST':
        snapshot_code = update['snapshot_code']
        reject_update = services.reject_updates(update_id , snapshot_code)
        if reject_update.status_code == 202:
            flash('Update resource successfully rejected', 'success')
            return redirect(url_for('.update_page'))
        else:
            flash('Error in rejecting update', 'danger')
            return redirect(url_for('.update_page'))
    else:
        return render_template('resources/updated_show.html',
                               update_form=update_form, update=update)

# Pending Resources Page
@ResourceBP.route('/pendings', methods=['GET'])
@login_required
def pending_page():
    resources = services.get_resources(mode='pending')
    return render_template("resources/pending_index.html", resources=resources)


# View Pending Resource Detail
@ResourceBP.route('/pending/resource/<int:resource_id>', methods=['GET'])
@login_required
def view_pending_page(resource_id):
    resource_form = ResourceForm()
    if request.method == 'GET':
        resource = services.view_resource(resource_id)
        return render_template('resources/pending_show.html',
                               resource=resource,
                               resource_form=resource_form)


# Pending Wishlist Page
@ResourceBP.route('/pending-wishlist', methods=['GET'])
@login_required
def pending_wishlist_page():
    wishlists = filter(lambda wishlist: wishlist['status'] == 'PENDING', services.get_pending_wishlist())
    return render_template("resources/pendingindex_wl.html", wishlists=wishlists)



# View Pending Wishlist Detail
@ResourceBP.route('/wishlist/<int:wishlist_id>', methods=['GET'])
@login_required
def view_pending_wishlist_page(wishlist_id):
    wishlist_form = WishlistForm()
    if request.method == 'GET':
        wishlist = services.view_wishlists(wishlist_id)
        wishlist = services.view_wishlists(wishlist_id)
        return render_template('resources/pendingshow_wl.html',
                               wishlist=wishlist, wishlist_form=wishlist_form)