from django.shortcuts import render ,  redirect
from django.http import HttpResponse
from pymongo import MongoClient

from PIL import Image, ImageTk
import io
from bson import Binary
import base64
import gridfs

from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django import template
register = template.Library()


# Create your views here.

URI = "mongodb://127.0.0.1:27017"
client = MongoClient(URI)
db = client['FamilyTree']

gfs = gridfs.GridFS(db)


def home(request) :
    return render(request , 'new_base.html')
    
    
def show_data(request) :
    mydata = db.tree.find({"perant_id" : ""})
    dict_data = {'data' : mydata}
    return render(request , 'show_data_n.html' , dict_data)
    
def insert_action(request) :
    count = db.tree.find({}).count()
    id = count + 1
    iname = request.POST.get('tname')
    gender = request.POST.get('gender')
    add = request.POST.get('tadd')
    tel = request.POST.get('ttel')
    prt_name = request.POST.get('tprt_name')
    brd = request.POST.get('tbrd')
    job = request.POST.get('tjob')
    if 'myimg' in request.FILES :
        myfile = request.FILES['myimg']
        fs = FileSystemStorage()
        image = fs.save(str(id)+'.jpeg', myfile)
        image  = settings.MEDIA_ROOT +"/" + image
        with open(image, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
       
    else :
          #myfile = './default.jpg'
          #fs = FileSystemStorage()
          #image = fs.save(str(id)+'.jpeg', myfile)
          image  = './default.jpg'
          with open('./default.jpg', "rb") as image_file:
              encoded_string = base64.b64encode(image_file.read())
    #print (encoded_string)
    record = {"_id" : str(id) , "id" : str(id) , "name" : iname , "perant_id" : '' , "address" : add , "telephone" : tel ,
              "parent_name" : prt_name , "birthday" : brd , "job" : job , "image" : image , "img" : encoded_string , "gender" : gender}
    try :
        db.tree.insert_one(record)
    except Exception as ex :
           return HttpResponse(ex , record)
    #return HttpResponse('Record has been inserted')
    return redirect ('showdata') # name of path in urls
    
def insert_data(request) :
    return render(request , 'insert_data.html')
    
    
def item_detail(request , id) :
    branchs = db.tree.find({"perant_id" : id})
    item_det = db.tree.find_one({"id"  : id})
    parent = item_det["perant_id"]
    img = item_det["img"]
    #stored = gfs.put(img, filename="images")
    #pil_img = Image.open(io.BytesIO(item_det['img']))
    #img_opj = ImageTk.PhotoImage(pil_img)
    #decode = base64.decodebytes(img) #img.decode()
    #img_tag = "item_det:img/png;base64,{0}".format(decode) # base64.decodebytes(img) -- format(decode)
    #img_tag = base64.b64decode(gfs.get(stored).read())
    #img_tag = gfs.get(stored).read()
    #img_tag =  "data:image/jpeg;base64,img"
    #img_tag = base64.decodebytes(img)
    #decode=img.decode()
    #decode = base64.decodebytes(img)
    #img_tag = '<img alt="sample" src="data:image/jpeg;base64,{0}">'.format(decode)
    #return HttpResponse(img_tag)
    #register.filter('img_decode' , img_decode) 
    img_tag = img.decode()
    if parent ==  "" : 
        part_gen = "Male"
    else :
        prt_item = db.tree.find_one({"id"  : parent})
        part_gen = prt_item["gender"] 
    flname = get_fullname(id)
    dict_data = {'data' : branchs , 'item_data' : item_det , "image" : img_tag , 'fullname' : flname , "parent_gen" : part_gen}
    return render(request , 'item_detail.html' , dict_data)
    
    
def new_branch(request , id) :
    item_det = db.tree.find_one({"id"  : id})
    dict_data = {'item_data' : item_det}
    return render(request , 'new_branch.html' , dict_data)


def insert_branchs(request , id) :
    #print(id)
    prt_id = id
    count = db.tree.find({}).count()
    id = count + 22
    #print(id)
    iname = request.POST.get('tname')
    gender = request.POST.get('gender')
    add = request.POST.get('tadd')
    tel = request.POST.get('ttel')
    prt_name = request.POST.get('tprt_name')
    brd = request.POST.get('tbrd')
    job = request.POST.get('tjob')
    if 'myfile' in request.FILES :
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        image = fs.save(str(id)+'.jpeg', myfile)
        image  = settings.MEDIA_ROOT +"/" + image
        with open(image, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
       
    else :
          #myfile = './default.jpg'
          #fs = FileSystemStorage()
          #image = fs.save(str(id)+'.jpeg', myfile)
          image  = './default.jpg'
          with open('./default.jpg', "rb") as image_file:
              encoded_string = base64.b64encode(image_file.read())
    
    record = {"_id" : str(id) , "id" : str(id) , "name" : iname , "perant_id" : prt_id , "address" : add , "telephone" : tel ,
              "parent_name" : prt_name , "birthday" : brd , "job" : job , "image" : image , "img" : encoded_string , "gender" : gender}
    #print(record)
    try :
        print('before insert')
        db.tree.insert_one(record)
        print('after insert')
        #return redirect ('showdata') # name of path in urls
    except Exception as ex :
           print(ex)
           return HttpResponse(ex , record)
           
    #return HttpResponse('Record has been inserted')
    print('Record has been inserted')
    return redirect ('showdata') # name of path in urls
    
    
def edit_item(request , id) :
    item_det = db.tree.find_one({"id"  : id})
    flname = get_fullname(id)
    dict_data = {'item_data' : item_det  , 'fullname' : flname}
    return render(request , 'edit_item.html' , dict_data)
    
    
    
def update_item(request , id) :
    #print(id)
    #prt_id = id
    #count = db.tree.find({}).count()
    #id = count + 1
    #print(id)
    item = db.tree.find_one({"id"  : id})
    prt_id = item["perant_id"]
    iname = request.POST.get('tname')
    gender = request.POST.get('gender')
    add = request.POST.get('tadd')
    tel = request.POST.get('ttel')
    prt_name = request.POST.get('tprt_name')
    brd = request.POST.get('tbrd')
    job = request.POST.get('tjob')
    if 'myimg' in request.FILES :
        myfile = request.FILES['myimg']
        fs = FileSystemStorage()
        image = fs.save(str(id)+'.jpeg', myfile)
        image  = settings.MEDIA_ROOT +"/" + image
        with open(image, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
       
    else :
              encoded_string = item["img"]
    
    cup_name = request.POST.get('cup_name')
    cup_add = request.POST.get('cup_add')
    dod = request.POST.get('dod')
    
    record = {"_id" : str(id) , "id" : str(id) , "name" : iname , "perant_id" : prt_id , "address" : add , "telephone" : tel ,
              "parent_name" : prt_name , "birthday" : brd , "job" : job ,  "img" : encoded_string , "gender" : gender ,   "cup_name" : cup_name , "cup_add" : cup_add , "dod" : dod }
    #print(record)
    try :
        #print('before insert')
        db.tree.update({"_id" : id } , {"$set" :{"name" : iname , "perant_id" : prt_id , "address" : add , 
        "telephone" : tel ,"parent_name" : prt_name , "birthday" : brd , "job" : job ,  "img" : encoded_string , 
        "gender" : gender ,  "cup_name" : cup_name , "cup_add" : cup_add , "dod" : dod }})
        #print('after insert')
        #return redirect ('showdata') # name of path in urls
    except Exception as ex :
           print('error')
           return HttpResponse(ex , record)
           #print('error')
    #return HttpResponse('Record has been inserted')
    print('Record has been inserted')
    return redirect ('showdata') # name of path in urls
    
    
    
def get_fullname(id) :
     item = db.tree.find_one({"id"  : id})
     parent = item["perant_id"]
     if parent ==  "" : 
        return item["name"]
        
     else :
          if item["gender"] == "Male" :
             sub = " بن "
          elif item["gender"] == "Female" :
             sub = " بنت "
          
          return item["name"] + sub + get_fullname(item["perant_id"])
       
         
    

def insert_image(request):
    with open(request.GET["image_name"], "rb") as image_file:
         encoded_string = base64.b64encode(image_file.read())
    print (encoded_string)
    abc=db.tee.insert({"image":encoded_string})
    return HttpResponse("inserted")

def retrieve_image(request):
    data = db.tee.find()
    data1 = json.loads(dumps(data))
    img = data1[0]
    img1 = img['image']
    decode=img1.decode()
    img_tag = '<img alt="sample" src="data:image/png;base64,{0}">'.format(decode)
    return HttpResponse(img_tag)
    



