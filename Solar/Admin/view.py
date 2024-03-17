from flask import Blueprint,request, render_template,redirect,url_for,jsonify,abort,flash
from flask_login import login_required,current_user
from Solar.Admin.form import UplaodMainCategoriesForm,UplaodSubCategoriesForm,UplaodproductForm,UploadCompareForm,DynamicFormProduct,UploadForm
import os
from Solar.database import db
from Solar.bunny import obj_storage
from Solar import csrf
from bson import ObjectId
import threading
import time
import uuid
import random

Admin=Blueprint('Admin',__name__,template_folder='templates/Admin',static_folder='static')

@Admin.before_request
@login_required
def check_is_Admin():
    id=current_user.user_id
    if not(current_user.is_authenticated  and current_user.role=='Admin'):
        return "<h1>this is invalid</h1>"
    
@Admin.route("/")
def Admin_index():
    return render_template('Admin_index.html')

# Main
@Admin.route("/ShowMainCategory")
def ShowMainCategory():
    data=list(db.MainCategory.find())
    return render_template('Main/Admin_ShowMainCategory.html',data=data)


@Admin.route("/addMainCategory",methods=['GET','POST'])
def add_main_category():
    form=UplaodMainCategoriesForm()
    if form.validate_on_submit():
        data={'name':form.name.data,
              'SubCategory':[]}
        db.MainCategory.insert_one(data)
        return redirect(url_for("Admin.ShowMainCategory"))
    return render_template( "Main/Admin_AddMainCategory.html" ,form = form )

@Admin.route("/deleteMainCategory/<string:id>", methods = ['GET','POST'])
def delete_main_category(id):
    data=db.MainCategory.find_one( {"_id": ObjectId(id)})
    for i in data['SubCategory']:
        data2=list(db.SubCategory.find({"_id":ObjectId(i)}))
        for j in data2:
            db.Product.delete_many({'_id': {'$in': j['Product']}})
    db.SubCategory.delete_many({'_id': {'$in': data['SubCategory']}})
    db.MainCategory.delete_one( {"_id": ObjectId(id)})
    return redirect(url_for("Admin.ShowMainCategory"))

@Admin.route("/editMainCategory",methods=['GET','POST'])
def edit_main_category():
    return 'edit_main_categories'

# Sub
@Admin.route("/ShowSubCategory/<string:subcat>")
def ShowSubCategory(subcat):
        data=db.MainCategory.find_one({"_id":ObjectId(subcat)})
        x=list(db.SubCategory.find({'_id':{ "$in" : data["SubCategory"] }}))
        return render_template ('Sub/Admin_ShowSubCategory.html',data=x,subcat=subcat)
   
@Admin.route("/ShowSubCategory/<string:subcat>/addSubCategory",methods=['GET','POST'])
def add_sub_category(subcat):
    form=UplaodSubCategoriesForm()
    if form.validate_on_submit():
        insert_result ={'name':form.name.data,
              'Product':[],
              'compare':[]}
        db.SubCategory.insert_one(insert_result)
        db.MainCategory.update_one(
                    {'_id': ObjectId(subcat)},
                    {'$push': {'SubCategory': ObjectId(insert_result['_id'])}}
                                )
        return redirect(url_for('Admin.ShowSubCategory', subcat=subcat))
    return render_template('sub/Admin_addSubCategory.html',form=form)

@Admin.route("/ShowSubCategory/<string:subcat>/addSubCategory/<string:id>",methods=['GET'])
def delete_sub_category(id,subcat):
    data=db.SubCategory.find_one_and_delete({"_id":ObjectId(id)})
    for i in data['Product']:
        data1=db.Product.find_one({"_id":ObjectId(i)})
        print('location',data1['fileLocation'])
        obj_storage.DeleteFile(data1['fileLocation'])
    db.Product.delete_many({'_id': {'$in': data['Product']}})
    db.MainCategory.update_one({'_id':ObjectId(subcat)},{"$pull":{'SubCategory':ObjectId(id)}})
    return redirect(url_for('Admin.ShowSubCategory',subcat=subcat))



@Admin.route("/editSubCategory",methods=['GET','POST'])
def edit_sub_category():
    return 'edit_sub_categories'

#product
@Admin.route("/ShowProduct/<string:main_id>/<string:sub_id>")
def ShowProduct(main_id,sub_id):
    #got an error routing issue opposite assinig sub_id to main_id vice versa
    # so i use main_id
    data=db.SubCategory.find_one({"_id":ObjectId(main_id)})
    x=list(db.Product.find({'_id':{ "$in" : data["Product"] }}))
    return render_template('Product/Admin_showProduct.html',data=x,sub_id=sub_id,main_id=main_id)
from flask import request
from werkzeug.utils import secure_filename
el=[]
def task(pl,sp):
    print("Started Task ...")
    print(threading.current_thread().name)
    time.sleep(0.1)
    try:
        obj_storage.PutFile(pl, storage_path=sp)
        os.remove(pl)
        print("completed .....")
    except:
        el.append(pl)
    else:
        if pl in el:
            obj_storage.PutFile(pl, storage_path=sp)
            os.remove(pl)
            el.remove(pl)
            print("completed .....")
import os

@Admin.route("/addproduct/<string:main_id>/<string:sub_id>", methods=['GET', 'POST'])
def add_product(sub_id, main_id):
    n = 0
    compare_list = db.SubCategory.find_one({'_id': ObjectId(main_id)})
    compare_list = compare_list['compare']
    field_names = compare_list
    data = None
    form = DynamicFormProduct.create_form(field_names, data)
    if form.validate_on_submit():
        data = {'name': form.name.data,
                'discription': form.description.data,                
                'price': form.price.data,
                'brand':form.brand.data,
                'productid':form.productid.data,
                'minimumOrderUnit':form.minimumOrderUnit.data,
                'height':form.height.data,
                'width':form.width.data,
                'weight':form.weight.data,
                'compare_parameter': {},
                'top':form.top.data}
        print(data)
        data['product_id']=str(uuid.uuid4())[0:5]            
        for field_name in field_names:
            field_value = getattr(form, field_name['name']).data
            data['compare_parameter'][field_name['name']] = field_value
        for file in ['photos1', 'photos2', 'photos3', 'photos4']:
            photo_file = request.files.get(file)
            n = n + 1
            if photo_file and photo_file.filename != '':
                folder_name = data['product_id']
                folder_path = os.path.join('files', folder_name)
                # Create the directory if it doesn't exist
                os.makedirs(folder_path, exist_ok=True)
                original_filename = secure_filename(photo_file.filename)
                file_extension = os.path.splitext(original_filename)[1]
                new_filename = f"{folder_name}-{n}{file_extension}"
                new_filename=new_filename.lower()
                file_path = os.path.join(folder_path, new_filename)
                photo_file.save(file_path)
                print(file_path)
                # storage_path = os.path.join('dynamic content', 'products', folder_name)
                sp=os.path.join('dynamic content', 'products', folder_name[:5],new_filename)
                print(sp)
                threading.Thread(target=task, args=(file_path,sp)).start()
                data[file] = 'stocksales.b-cdn.net'+'/'+str('dynamic content')+ '/' + 'products' + '/' + str(folder_name)+'/' +new_filename
            data['fileLocation']=f"dynamic content/products/{folder_name}/"
        productAdd = db.Product.insert_one(data)
        print(form.top.data)
        if form.top.data :
                db.topPro.insert_one({'top':productAdd.inserted_id})
        else:
            try:
                db.topPro.delete_one({'top':productAdd.inserted_id})
            except:
                pass
        db.SubCategory.update_one(
            {'_id': ObjectId(main_id)},
            {'$push': {'Product': productAdd.inserted_id}})
        return redirect(url_for('Admin.ShowProduct', sub_id=sub_id, main_id=main_id))
    return render_template('Product/Admin_addProduct.html', form=form)
   
@Admin.route("/deleteproduct/<string:main_id>/<string:sub_id>/<string:product_id>",methods=['GET'])
def delete_product(main_id,sub_id,product_id):
    
    data=db.Product.find_one_and_delete({"_id":ObjectId(product_id)})
    obj_storage.DeleteFile(data['fileLocation'])
    db.SubCategory.update_one({"_id": ObjectId(sub_id)}, {'$pull': {'Product': ObjectId(product_id)}})
    return redirect (url_for('Admin.ShowProduct',main_id=sub_id,sub_id=main_id))

@Admin.route("/editproduct",methods=['GET','POST'])
def edit_product():
    form=UplaodproductForm()
    if form.validate_on_submit():
        data={'name':form.name.data}
        # logic
    return 'edit_compare'

#Product Details
@Admin.route("/viewProductDetails/<string:Product_id>/<string:Sub_id>/<string:Main_id>", methods=["GET","POST"])
def ViewProductDetails(Product_id,Sub_id,Main_id):
    Productdata=db.Product.find_one({'_id':ObjectId(Product_id)})
    # problem of resiprocale between sub_id and main_id
    compare_list=db.SubCategory.find_one({'_id':ObjectId(Main_id)})
    field_names=compare_list['compare']
    form=DynamicFormProduct.create_form(field_names,Productdata)
    if form.validate_on_submit():
        # data = {'name': form.name.data,'discription':form.description.data,'compare_parameter':{}}
        data = {'name': form.name.data,
                'discription': form.description.data,
                'brand':form.brand.data,
                'price': form.price.data,
                
                'productid':form.productid.data,
                'minimumOrderUnit':form.minimumOrderUnit.data,
                'height':form.height.data,
                'width':form.width.data,
                'weight':form.weight.data,
                'compare_parameter': {},
                'top':form.top.data}
        for field_name in field_names:
            field_value = getattr(form, field_name['name']).data
            data['compare_parameter'][field_name['name']]=field_value
        dataentry=db.Product.find_one_and_update({'_id':ObjectId(Product_id)},{'$set':data})
        if form.top.data :
                db.topPro.insert_one({'top':dataentry['_id']})
        else :
                try:
                    db.topPro.delete_one({'top':dataentry['_id']})
                except:
                    pass
        return redirect (url_for('Admin.ShowSubCategory',subcat=Sub_id))
    return render_template('ProductDetails/viewProductDetails.html',data=Productdata,form=form)

# compare
@Admin.route('/Compare/<string:sub_id>')
def Compare_Templates(sub_id):
    data = db.SubCategory.find_one({'_id': ObjectId(sub_id)})
    return render_template ('Compare/Admin_addcompare.html',sub_id=sub_id,data=data)

@Admin.route("/Compare/addcompare", methods=['POST'])
@csrf.exempt
def add_compare():
    if request.method == 'POST':
        data = request.json
        db.SubCategory.update_one({'_id':ObjectId(data["sub_id"])},{'$set':{"compare":data['property']}})
        # return redirect(url_for('Admin.Admin_index'))
    return "none"

@Admin.route('/selectimage/<string:product_id>')
def selectimage(product_id):
    data=db.Product.find_one({'_id':ObjectId(product_id)})
    return render_template('ProductDetails/selectImages.html',product_id=product_id,data=data)
#may be wru=itten i a way where i update files instade of uploading --> renaming --> deleting
@Admin.route('/changeimage/<string:product_id_mongo>/<string:image_name>/<string:product_id>' , methods=['GET','POST'])
def changeimage(product_id_mongo,image_name,product_id):
    form=UploadForm()
    if form.validate_on_submit():
        n = random.randint(1, 100)
        file = form.file.data
        folder_name = product_id
        folder_path = os.path.join('files', folder_name)
        os.makedirs(folder_path, exist_ok=True)
        original_filename = secure_filename(file.filename)
        file_extension = os.path.splitext(original_filename)[1]
        new_filename = f"{folder_name}-{n}{file_extension}"
        new_filename=new_filename.lower()
        file_path = os.path.join(folder_path, new_filename)
        file.save(file_path)
        sp=os.path.join('dynamic content', 'products', folder_name[:5],new_filename)   
        print(sp)     
        data_url = 'stocksales.b-cdn.net'+'/'+str('dynamic content')+ '/' + 'products' + '/' + str(folder_name)+'/' +new_filename
        obj_storage.PutFile(file_path, storage_path=sp)
        data_image=db.Product.find_one_and_update({'_id':ObjectId(product_id_mongo)},{'$set':{image_name:data_url}})
        data_image=data_image[image_name]
        path_of_delete_file=os.path.join('dynamic content', 'products',product_id,data_image[55:])
        print("path",path_of_delete_file)
        obj_storage.DeleteFile(path_of_delete_file)
        flash("Image has been uploaded successfully","success")
        os.remove(file_path)
        return redirect (url_for('Admin.selectimage',product_id=product_id_mongo))
    return render_template('ProductDetails/changeimage.html',form=form,product_id_mongo=product_id_mongo)

#################### route display the query ##############
@Admin.route('/showquery')
def showquery():
    return render_template('Query/Admin_showquery.html',data=list(db.solarEnq.find()))

@Admin.route('/showProductQuery')
def showProductQuery():
    return render_template('Query/Admin_showproductquery .html',data=list(db.productQuery.find()))
    
@Admin.route('/showcontactQuery')
def showcontactQuery():
    return render_template('Query/Admin_showcontact.html',data=list(db.contact.find()))
    
    