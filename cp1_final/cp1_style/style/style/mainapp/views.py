from django.shortcuts import render
import os
import psycopg2
import joblib
import requests
from bs4 import BeautifulSoup as bs
import torch

def change(li):
    result = []
    for i in li:
        if i == 0:
            result.append(['top','half'])
        elif i == 1 or i==6:
            result.append( ['top','pk'])
        elif i == 2 or i==3 or i==7 or i==8:
            result.append( ['top','shirts'])
        elif i == 4 or i == 9:
            result.append( ['top','knit'])
        elif i == 5:
            result.append( ['top','long'])
        elif i == 10:
            result.append( ['top','hood'])
        elif i == 11:
            result.append( ['top', 'mantoman'])
        elif i == 12:
            result.append( ['top','sleeveless'])
        elif i == 13:
            result.append( ['bot','cot'])
        elif i == 14 or i ==16:
            result.append( ['bot','half'])
        elif i == 15:
            result.append( ['bot','denim'])
        elif i == 17:
            result.append( ['bot','slax'])
        elif i == 18 or i == 19:
            result.append( ['bot','training'])
        elif i == 20:
            result.append( ['bot','leggings'])
        elif i == 21:
            result.append( ['skirt','mini'])
        elif i == 22:
            result.append( ['skirt','midi'])
        elif i == 24:
            result.append( ['skirt','long'])
        else:
            result.append( [None] )
    return result

def label(majorcategories,subcategories):
    label = {
        'top' :{
            'etc':0,
            'hood':1,
            'knit':2,
            'long':3,
            'mantoman':4,
            'pk':5,
            'shirts':6,
            'sleeveless':7,
            'half':8
        },
        'out' : {
            'cardigan':9,
            'fleece':10,
            'hood':11
        },
        'bot':{
            'cot':12,
            'denim':13,
            'etc':14,
            'half':15,
            'leggings':16,
            'slax':17,
            'training':18
        },
        'skirt':{
            'mini':19,
            'midi':20,
            'long':21
        }
        }
    
    if majorcategories == 'top':
        maj = 0
    elif majorcategories == 'out':
        maj = 1
    elif majorcategories == 'bot':
        maj = 2
    else:
        maj = 3

    sub = label[majorcategories][subcategories]
    return maj,sub
    
def loadimg(url):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    myurl = url
    resp = requests.get(myurl,headers=hdr)
    soup = bs(resp.content,'lxml')
    corp = soup.find('div','product-img').find('img')['src']
    name = soup.find('span','product_title').find('em').get_text()
    return corp[2:], name

    
def size_to(size):
    if (size == 0.0) or (size == 7.0):
        size = "XS"
    elif (size == 1.0) or (size == 8.0):
        size = "S"
    elif (size == 2.0) or (size == 9.0):
        size = "M"
    elif (size == 3.0) or (size == 10.0):
        size ="L"
    elif (size == 4.0) or (size == 11.0):
        size ="XL"
    elif (size == 5.0) or (size == 12.0):
        size = "2XL"
    else:
        size="3XL"
    return size
            
model = joblib.load('mainapp/knn_one.pkl')

#아래 정보를 입력
user = 'fuusaujh'
password = 'KPbDgG1NtOXKVcU_rstsh0xMTFDChg0J'
host_product = 'jelani.db.elephantsql.com'
dbname = '	fuusaujh'
port='5432'

product_connection_string = "dbname={dbname} user={user} host={host} password={password} port={port}"\
                            .format(dbname=dbname,
                                    user=user,
                                    host=host_product,
                                    password=password,
                                    port=port)    
try:
    conn = psycopg2.connect(product_connection_string)
except:
    print("I am unable to connect to the database")

conn.autocommit=True


# Create your views here.
ENROLLED_DATA = 'static/enrolled_data'

def info(request):
    return render(request, 'mainapp/info.html')

def door_page(request):
    return render(request, 'mainapp/home.html')

def cody_page(request):
    if request.method == 'POST':
        cur = conn.cursor()
        age = int(request.POST.get('age'))
        gender = request.POST.get('gender')
        height = float(request.POST.get('height'))
        weight = float(request.POST.get('weight'))
        majorcategories = request.POST.get('majorcategories')
        subcategories = request.POST.get('subcategories')
        cur.execute("""
            INSERT INTO mainapp_information_user VALUES(%s, %s, %s, %s, %s, %s)
        """,(gender, age, height, weight, majorcategories, subcategories))
        conn.commit()
        maj = label(majorcategories,subcategories)[0]
        sub = label(majorcategories,subcategories)[1]
        size = model.predict([[gender,height,weight,maj,sub]])[0]
        cur.execute(f"""
            SELECT link, product_sales FROM clothing.{majorcategories} where sub like '%{subcategories}%' order by product_sales desc limit 1""")
        lst = cur.fetchall()
        conn.commit()
        cur.close()
        site = lst[0][0]
        load = loadimg(lst[0][0])
        new_src = load[0]
        name = load[1] 
        size=size_to(size)
        return render(request, 'mainapp/cody/result.html', context={'age': age, 'gender': gender, 'height': height, 'weight': weight, 'majorcategories': majorcategories, 'subcategories': subcategories, 'size':size, 'link':site, 'newurl':new_src, 'name':name})
    else:
        return render(request, 'mainapp/cody.html', context={'age': 'age'})

def reco_result(request):
    if request.method == "POST":
        cur = conn.cursor()
        results = []
        for (root, directories, files) in os.walk(ENROLLED_DATA):
            for file in files:
                file_path = os.path.join(root, file)
                model = torch.hub.load('ultralytics/yolov5', 'custom', path='mainapp/best_clo.pt')
                result = model(file_path)
                print(result)
                names = list(result.pandas().xyxy[0]['name'])
                classes = list(result.pandas().xyxy[0]['class'])
                top_list = list(filter(lambda x: x.startswith('top'), names))
                bot_list = list(filter(lambda x: x.startswith('bot'), names))
                top_class = None
                bot_class = None
                result_class_list = []
                # results.append(names)
                # results.append(classes)
                if len(top_list) > 0:
                    top = top_list[0]
                    top_index = names.index(top)
                    top_class = classes[top_index]
                    result_class_list.append(top_class)
                if len(bot_list) > 0:
                    bot = bot_list[0]
                    bot_index = names.index(bot)
                    bot_class = classes[bot_index]
                    result_class_list.append(bot_class)
                    # results.append(result_class_list)
                major_sub = change(result_class_list)
                # results.append(major_sub)
                for item in major_sub:
                    cur.execute(f"""
                        SELECT link FROM clothing.{item[0]} where sub like '%{item[1]}%' order by product_sales desc limit 1
                    """)
                    url = cur.fetchone()[0]
                    print(url)
                    img_url = loadimg(url)[0]
                    img_name = loadimg(url)[1]
                    results.append([img_name,url, img_url])
                    print(results)
                os.remove(file_path)
        return render(request, 'mainapp/reco/result.html', context={'results': results})

def review_page(request):
    if request.method == 'POST':
        cur = conn.cursor()
        gender = request.POST.get('gender')
        recommend = request.POST.get('exampleRadios')
        what = request.POST.get('exampleRadios1')
        cur.execute("""
            INSERT INTO mainapp_review_user (gender, recommend, what) VALUES( %s, %s, %s)
        """, (gender, recommend, what))
        conn.commit()
        cur.close()
        return render(request, 'mainapp/review.html')
    else:
        return render(request, 'mainapp/review.html')

def reco_page(request):
    if request.method == "POST":
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' :  #   ajax  
            if not os.path.exists(ENROLLED_DATA): #  settings            
                os.makedirs(ENROLLED_DATA,exist_ok=True) #     
            for k,file_obj in request.FILES.items(): #            
                with open('%s/%s'%(ENROLLED_DATA,file_obj.name),"wb") as f: #    
                    for chunk in file_obj.chunks():   
                        f.write(chunk)  #chunk      
    return render(request, 'mainapp/reco.html')

def thnk(request):
    if request.method == "POST":
        return render(request, 'mainapp/review/thankyou.html')