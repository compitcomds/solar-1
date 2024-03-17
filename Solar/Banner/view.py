from flask import Blueprint, jsonify,abort,render_template,redirect,url_for, request,flash
from flask_login import login_required,current_user
from Solar.database import db
from Solar.Banner.form import UploadForm
from bson import ObjectId
from Solar.bunny import obj_storage
import os
from werkzeug.utils import secure_filename

Banner=Blueprint('Banner',__name__,template_folder='templates/Banner',static_folder='')

@Banner.before_request
@login_required
def check_is_User():
    id=current_user.user_id
    if not(current_user.is_authenticated  and current_user.role=='Admin'):
        return "<h1>this is invalid</h1>","403"
    

@Banner.route('/')
def showBanner():
    data=list(db.banner.find())
    return render_template('admin_show_banner.html',data=data)



@Banner.route('/Admin_addBanner', methods=['GET','POST'])
def addBanner():
    form = UploadForm()
    if form.validate_on_submit():
        data={
            'title':form.title.data,
            'image_link':''
        }
        result = db.banner.insert_one(data)
        _id = result.inserted_id 
        file = form.file.data
        folder_name = data['title']
        # Use current working directory for the directory
        folder_path = os.path.join('bannerfile',folder_name)
        os.makedirs(folder_path, exist_ok=True)
        # Split the original filename and extension
        filename, file_extension = os.path.splitext(secure_filename(file.filename))
        # Generate a new filename using the _id, original filename, and secure_filename
        new_filename = f"{str(_id)}{file_extension}"
        file_path=os.path.join(folder_path, new_filename)
        file.save(file_path)
        sp = os.path.join('dynamic content','banner',folder_path ,str(_id)+file_extension)
        obj_storage.PutFile(file_path, storage_path=sp)
        os.remove(file_path)
        data_url = 'stocksales.b-cdn.net'+'/'+str('dynamic content')+ '/' + 'banner' + '/'+'bannerfile'+'/' + str(folder_name)+'/' +new_filename
        db.banner.find_one_and_update({'_id': _id}, {'$set': {'image_link': data_url,'fileLocation':sp}})
        return redirect(url_for('Banner.showBanner'))
    return render_template('add_banner.html', form=form)

@Banner.route('/deletebanner/<string:banner_id>')
def deleteBanner(banner_id):
    x=db.banner.find_one_and_delete({'_id':ObjectId(banner_id)})
    if x :
        flash(message='deleted successfully',category='success')
        obj_storage.DeleteFile(x['fileLocation'])
        return redirect(url_for('Banner.showBanner'))
    else:
        flash(message='not able to delete',category='error')
        return redirect(url_for('Banner.showBanner'))
