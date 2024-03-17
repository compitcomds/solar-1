from dotenv import load_dotenv
from flask import Flask, jsonify,render_template,jsonify,session,redirect,url_for,request,flash,abort
from config import *
from flask_wtf import CSRFProtect
from Solar.database import db
from Solar.form import homepageform1, homepageform2,contactform,productquery
from Solar.Auth.otp import SendTYmessage
from bson import ObjectId
from flask_login import login_required,current_user


load_dotenv(override=True)

app = Flask(__name__)
app.config.from_object(Config)

csrf =CSRFProtect(app)

from Solar.Auth.view import Auth
app.register_blueprint(Auth,url_prefix='/')

from Solar.Admin.view import Admin
app.register_blueprint(Admin,url_prefix='/admin')

from Solar.User.view import User
app.register_blueprint(User,url_prefix='/user')

from Solar.Blog.view import Blog
app.register_blueprint(Blog,url_prefix='/BlogAdmin')

from Solar.Banner.view import Banner
app.register_blueprint(Banner,url_prefix='/BannerAdmin')

from Solar.SmallBanner.view import SmallBanner
app.register_blueprint(SmallBanner,url_prefix='/SmallBannerAdmin')

def getToppro():
    list=[]
    data=db.topPro.find()
    for i in data:
        data2=db.Product.find_one(i['top'])
        list.append(data2)
    return list

def getladder():
    data={}
    data_product=db.SubCategory.find()
    for i in data_product:
        data[i['_id']]=i['name']
    return data


@app.context_processor
def nav_item():
    data_categories = list(db.MainCategory.find())
    is_admin = current_user.is_authenticated and current_user.role == 'Admin'
    return {'data_categories': data_categories, 'is_admin': is_admin}

@app.route('/',methods=['GET','POST'])
def index():
    data_top_product=getToppro()
    data_small_banner=list(db.smallbanner.find())
    data_big_banner=list(db.banner.find())
    data_blog=list(db.blog.find())
    form=homepageform1()
    form2=homepageform2()
    if form.validate_on_submit():
        data1={'name':form.name.data,
              'contact-information':form.number.data,
              'email':form.email.data,
              'Avg Monthly Electricity Bill (Rs)':form.ameb.data,
              'pin code':form.pincode.data,
              'companyName':'Non-resident',
            'date':str(datetime.now().strftime('%Y-%m-%d'))
              }
        SendTYmessage(form.email.data)
        db.solarEnq.insert_one(data1)
        ## send thanks message
        return redirect (url_for('index'))

    if form2.validate_on_submit():
        data2={'name':form2.name.data,
              'contact-information':form2.number.data,
              'email':form2.email.data,
              'Avg Monthly Electricity Bill (Rs)':form2.ameb.data,
              'pin code':form2.pincode.data,
              'companyName':form2.companyName.data,
            'date':str(datetime.now().strftime('%Y-%m-%d'))

              }
        db.solarEnq.insert_one(data2)
        SendTYmessage(form.email.data)
        return redirect (url_for('index'))
    return render_template('index.html',data_small_banner=data_small_banner,data_big_banner=data_big_banner,data_top_product=data_top_product,data_blog=data_blog,form=form,form2=form2)

@app.route('/bigBanner')
def bigBanner():
    data=['asd','qwe']
    return jsonify (data)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/subcategories/<string:id>')
def subcategories(id):
    qwe=getladder()
    data_product_list=[]
   
    data=db.MainCategory.find({'_id':ObjectId(id)})
    list_ofsubcat=(list(data[0]['SubCategory']))
    for i in list_ofsubcat:
        x=db.SubCategory.find_one(i)
        # this will delete
         
        for j in x['Product']:
            data_product_list.append(db.Product.find_one({'_id':ObjectId(j)}))
    data_sideNav=list(db.MainCategory.find())
    return render_template('subcategories.html',qwe=qwe,data=data_product_list,data_sideNav=data_sideNav)

@app.route('/product_list/<string:main_id>/<string:sub_id>')
def product_list(main_id,sub_id):
    list_of_product=[]
    list_of_subcat_name=[]
    qwe=getladder()
    data=db.MainCategory.find({'_id':ObjectId(main_id)})
    # this will delete
    data_sideNav=list(db.MainCategory.find())
    list_ofsubcat=(list(data[0]['SubCategory']))
    for i in list_ofsubcat:
        x=db.SubCategory.find_one(i)
        # list_of_subcat_name.append(x['name'])
    x=list(db.SubCategory.find({'_id':ObjectId(sub_id)}))
    for i in x[0]['Product']:
        list_of_product.append(db.Product.find_one({'_id':ObjectId(i)}))
    return render_template('subcategories.html',qwe=qwe,data=list_of_product,data_sideNav=data_sideNav,list_of_subcat_name=list_of_subcat_name)
from datetime import datetime

@app.route('/productdetails/<string:prod_id>',methods=['GET','POST'])
def productdetails(prod_id):
    data=db.Product.find_one({'_id':ObjectId(prod_id)})
    form=productquery()
    if form.validate_on_submit():
        form_data={
            'name':form.name.data,
            'email':form.email.data,
            'number':form.number.data,
            'netQty':form.netQty.data,
            'product_name':data['name'],
            'product_id':data['_id'],
            'date':str(datetime.now().strftime('%Y-%m-%d'))
        }
        db.productQuery.insert_one(form_data)
        flash('Your query has been sent!','sm')
        SendTYmessage(form.email.data)
        return redirect(url_for('productdetails', prod_id = prod_id))
    return render_template('productDetails.html',data=data,form=form)

import json
def getsimilarproductlist(prod_id):
    data_list = []

    
    # Convert prod_id to ObjectId
    prod_id_obj = ObjectId(prod_id)
    
    data = db.SubCategory.find({
        "Product": prod_id_obj
    })
    
    for item in data:
        for product_id in item['Product']:
            product_obj = db.Product.find_one({"_id": product_id})
            if product_obj:
                data_list.append({'name': product_obj['name'], "id": str(product_obj['_id'])})
    return ({'data': data_list})

@app.route('/getinfoproduct')
def getinfoproduct():
    try:
        id = request.args.get('id')
        if not id:
            return jsonify({'error': 'Name parameter is required'}), 400

        data = db.Product.find_one({'_id': ObjectId(id)})
        if data:
            # Convert ObjectId to string before jsonify
            data['_id'] = str(data['_id'])
            return jsonify(data), 200
        else:
            return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

### get a route thata get the infoprmation to the route ###

@app.route('/compare/<string:id>')
def compare(id):
    a = getsimilarproductlist(id)
    data = db.Product.find_one({'_id': ObjectId(id)})
    qw = request.args
    pro1 = qw.get('pro1')
    pro2 = qw.get('pro2')
    pro3 = qw.get('pro3')
    # Fetching data from MongoDB and converting cursors to lists
    data1 = list(db.Product.find({'_id': ObjectId(pro1)})) if pro1 else []
    data2 = list(db.Product.find({'_id': ObjectId(pro2)})) if pro2 else []
    data3 = list(db.Product.find({'_id': ObjectId(pro3)})) if pro3 else []

    return render_template('compare.html', data=data, data1=data1, data2=data2, data3=data3, a=a)
@app.route('/contact_us', methods=['GET','POST'])
def contactus():
    form=contactform()
    if form.validate_on_submit():
        data={
            'name':form.name.data,
            'email':form.email.data,
            'number':form.number.data,
            'subject':form.subject.data,
            'message':form.message.data,
            'date':str(datetime.now().strftime('%Y-%m-%d'))
        }
        db.contact.insert_one(data)
        SendTYmessage(data['email'])
        return redirect(url_for('contactus'))
    return render_template('contact.html',form=form)


@app.route('/blogs')
def blogs():
    data=list(db.blog.find())
    return render_template('blog.html',data=data)
   
@app.route('/blogs/<blog_id>')
def blogDetails(blog_id):
    try:
        related_data=list(db.blog.find())
        related_data=related_data[:4]
        data=list(db.blog.find({'_id':ObjectId(blog_id)}))
        return render_template('blogDetails.html',data=data,related_data=related_data)
    except:
        abort(404)
