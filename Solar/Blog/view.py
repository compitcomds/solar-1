from flask import Blueprint, jsonify,abort,render_template,redirect,url_for, request,flash
from flask_login import login_required,current_user
from Solar.database import db
from Solar.Blog.form import UploadBlog,UpdateBlog
from bson import ObjectId
from Solar.bunny import obj_storage
import os
from werkzeug.utils import secure_filename
import os
from werkzeug.utils import secure_filename
from datetime import datetime

Blog=Blueprint('Blog',__name__,template_folder='templates/Blog',static_folder='')



@Blog.before_request
@login_required
def check_is_User():
    id=current_user.user_id
    if not(current_user.is_authenticated  and current_user.role=='Admin'):
        return "<h1>this is invalid</h1>","403"

@Blog.route('/')
def ShowBlog():
    data=db.blog.find()
    return render_template('showBlog.html',data=data)



@Blog.route('/AddBlog', methods=['GET', 'POST'])
def AddBlog():
    form = UploadBlog()  # Instantiate the form class
    if form.validate_on_submit():
        data = {
            'heading': form.heading.data,
            'date':str(datetime.now())[0:10],
            'para1': form.para1.data,
            'para2': form.para2.data,
            'para3': form.para3.data,
            'para4': form.para4.data,
            'para5': form.para5.data,
            'image_link':'https://www.youtube.com/watch?v=SmaY7RfBgas&list=RDGg48H-lrZHo&index=25'
        }
        result = db.blog.insert_one(data)

        _id = result.inserted_id  # Get the '_id' of the inserted document

        # Get the file from the request
        file = form.image.data
        folder_name = data['heading']

        # Use current working directory for the directory
        folder_path = os.path.join('blogFiles',folder_name)
        os.makedirs(folder_path, exist_ok=True)
        # Split the original filename and extension
        filename, file_extension = os.path.splitext(secure_filename(file.filename))
        # Generate a new filename using the _id, original filename, and secure_filename
        new_filename = f"{str(_id)}{file_extension}"
        file_path=os.path.join(folder_path, new_filename)
        file.save(file_path)
        sp = os.path.join('dynamic content', 'blog',folder_path ,str(_id)+file_extension)
        obj_storage.PutFile(file_path, storage_path=sp)
        os.remove(file_path)
        data_url = 'stocksales.b-cdn.net'+'/'+str('dynamic content')+ '/' + 'blog' + '/'+'blogFiles'+'/' + str(folder_name)+'/' +new_filename
        db.blog.find_one_and_update({'_id': _id}, {'$set': {'image_link': data_url,'fileLocation':sp}})
        return redirect(url_for('Blog.ShowBlog'))

    return render_template('add_blog.html', form=form)

@Blog.route('/delete/<string:blogid>')
def DeleteBolg(blogid):
    x=db.blog.find_one_and_delete({'_id':ObjectId(blogid)})
    if x :
        flash(message='deleted successfully',category='success')
        obj_storage.DeleteFile(x['fileLocation'])
        return redirect (url_for('Blog.ShowBlog'))
    else:
        flash(message='not able to delete',category='error')
        return redirect (url_for('Blog.ShowBlog'))

@Blog.route('/update_blog/<string:blog_id>', methods=['GET', 'POST'])
def update_blog(blog_id):
    # Assuming you retrieve blog data based on blog_id from the database
    blog_data = db.blog.find_one({'_id':ObjectId(blog_id)})
    form = UpdateBlog(**blog_data)
    if form.validate_on_submit():
        print('ooooooooooooo')
        data={'heading':form.heading.data,
              'para1':form.para1.data,
              'para2':form.para2.data,
              'para3':form.para3.data,
              'para4':form.para4.data,
              'para5':form.para5.data
              }
        print(data)
        db.blog.update_one({'_id':ObjectId(blog_id)},{'$set':data})
        # db.blog.insert_one(data)
        return redirect(url_for('Blog.ShowBlog'))
    return render_template('update_blog.html', form=form, blog_id=blog_id)