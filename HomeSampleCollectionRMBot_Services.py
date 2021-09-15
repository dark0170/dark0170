import os
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from botx import settings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from django.core.mail import EmailMultiAlternatives
import math, random
import pymongo
from twilio.rest import Client
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import json
import pprint
from fuzzywuzzy import fuzz 
from fuzzywuzzy import process 
from .nlp_engine.faq_engine_updated_for_G import Faq_Engine
from .nlp_engine .faq_funcation import FAQ_Extractor
from django.core.mail import send_mail
from .nlp_engine.train_faq import faq_training
from .work_flow_designer.ui_data_to_db import UidataToDatabase
from .work_flow_designer.db_data_to_ui import DataBaseToUi


# print(upload_img)
me = os.path.join(BASE_DIR, "media")



path = "C:/Bitnami/wampstack-7.1.26-0/apache2/htdocs/media"
mongo_conn = pymongo.MongoClient()


db_base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_base_path_json = os.path.join(db_base_dir, "FAQ",'nlp_engine')

with open(os.path.join(db_base_path_json,  "config_file.json"), "r") as fp:
            db_name = json.load(fp)




db = mongo_conn[db_name["data_base"]]




##############################
####
#### Common Bot Services
### Synonames

############# Synomaes service #######

@csrf_exempt
def faq_synonyms(request):
    synonym = JSONParser().parse(request)
    # synonym = [{"key": "improve forecast accuracy",
    #             "value": "IFA"},
    #            {"key": "Product Engineering",
    #             "value": "PE"}
    #            ]
    import pymongo
    print("synonym response===>",synonym)
    ######
    # synonames
    # synomanes={"key":"Product Engineering",
    #             "value":"PE"}
    # ######
    con_dic=[]
    find_flag = False
    try:
        #mongo_conn = pymongo.MongoClient()
        #db = mongo_conn["salesforce"]
        col = db["f_a_q"]
        col_data = col.find({})
        queation_list = []
        for o in col_data:
            # print(i['question'])
            for sno in synonym:
                if sno['key'].lower() in o['question'].lower():
                    find_flag=True
                    # print(i['question'])
                    my_q_list = o['question'].split("#")
                    #print("my q list==>", my_q_list)
                    # my_new_questions_list(system generated)
                    system_generated = []
                    for i in my_q_list:
                        if sno['key'].lower() in i.lower():
                            #print("===>", i)
                            system_generated.append(i.lower().replace(sno['key'].lower(), sno['value']))

                    print("---->", system_generated)
                    #print("original-->", (o['question']))
                    for s in system_generated:
                        o['question'] += "#sys: " + s

                    #print("original + sys-->", (o['question']))
                    col_new = db["f_a_q"]
                    # col_new.update_one({},{"$set":{o['question']}})
                    col.update_one({'_id': o['_id']}, {"$set": {"question": o['question']}})
                    # col_new.update_one({'_id': o['_id']}, {"$set": {"sys": o['question']}})
                    # col_new.update_one({'_id': o['_id']}, {"$set": {"sys": system_generated}},upsert=False)
                    # col_new.update_one({'_id': o['_id']}, {"$addToSet": {"sys": system_generated}})
                    # break
                    # print(my_q_list)
        #con_dic=[{
        #    'type': 'text',
        #    'sequence': '',
        #    'value': "Synonym added successfully"
        #}]
        if find_flag==True:
            con_dic=[{
                'type': 'text',
                'sequence': '',
                'value': "Synonym added successfully"
            }]
        if find_flag == False:
            con_dic = [{
                'type': 'text',
                'sequence': '',
                'value': "FAQ Training for this Synonym is not available"
            }]
    except Exception as e:
        print("Exception in faq_synonyms",e)
        con_dic = [{
            'type': 'text',
            'sequence': '',
            'value': "Unable to add Synonym"
        }]



    return JsonResponse(con_dic, safe=False)

#### ##############################
@csrf_exempt
def task_synonym(request):
    synonym = JSONParser().parse(request)
    # synonym = [{"key": "Bolt expertns",
    #             "value": "BE"},
    #            {"key": "Bolt expertns",
    #             "value": "Bolt EXX"},
    #            {"key": "PRODUCT DEVELOPMENT lifecycle",
    #             "value": "PDL aaaaaaaaaa"},
    #
    #            ]
    print("user response===>",synonym)
    try:
        import pymongo
        #mongo_conn = pymongo.MongoClient()
        #db = mongo_conn["salesforce"]
        col = db["training_data_updated"]
        col_data = col.find({})
        queation_list = []
        for o in col_data:
            # print(o['patterns'])
            # print(type(o['patterns']))
            for sno, p in zip(synonym, o['patterns']):
                if sno['key'].lower() in p.lower():
                    system_generated = []
                    for i in o['patterns']:
                        if sno['key'].lower() in i.lower():
                            # print("===>", i)
                            system_generated.append(i.lower().replace(sno['key'].lower(), sno['value']))
                    #print("system_generated ---->", system_generated)
                    ###add to existing pattern list
                    for s in system_generated:
                        o['patterns'].append("sys: " + s)
                    #
                    #print("original + sys-->", (o['patterns']))
                    col_new = db["training_data_updated"]
                    # col_new.update_one({},{"$set":{o['question']}})
                    col.update_one({'_id': o['_id']}, {"$set": {"patterns": o['patterns']}})
        con_dic = [{
            'type': 'text',
            'sequence': '',
            'value': "Synonym added successfully"
        }]
    except Exception as e:
        print("Exception in task synonym",e)
        con_dic = [{
            'type': 'text',
            'sequence': '',
            'value': "Unable to add Synonym"
        }]

    return JsonResponse(con_dic, safe=False)



@csrf_exempt
def feed_back_thanks(request):
    con_dict = {}
    con_dict =  [{"type": "text",
                "sequence": "1",
                "value": "Thanks for your valuable feeedback ... we feel appreciated."
            }]
    return JsonResponse(con_dict, safe=False)


@csrf_exempt
def dynamic_recom(request):
    con_dict = {}
    con_dict =  [{
                    "title" : "Group",
                    "task" : "",
                    "link" : "",
                    "utterance" : "Group",
                    "recomend_flag" : ""
                },{
                    "title" : "Group",
                    "task" : "",
                    "link" : "",
                    "utterance" : "Group",
                    "recomend_flag" : ""
                },
                {
                    "title" : "Group",
                    "task" : "",
                    "link" : "",
                    "utterance" : "Group",
                    "recomend_flag" : ""
                },
                {
                    "title" : "Group",
                    "task" : "",
                    "link" : "",
                    "utterance" : "Group",
                    "recomend_flag" : ""
                }]

    return JsonResponse(con_dict, safe=False)






@login_required(login_url='/')
def faq_data(request):
    con_dict = {}
    faq_detail = FAQ.objects.all()
    con_dict['faq_detail'] = faq_detail
    con_dict['username'] = request.user
    return render(request, 'FAQ_templates/db.html',con_dict)

@csrf_exempt
def work_flow_data(request):
    con_dict = {}
    db_names = ""
    print("==================== in work_flow_data UI TO DB ============")


    data = JSONParser().parse(request)
    ui_obj = UidataToDatabase()
    db_names = db_name["data_base"]
    
    if data:
 
        for i in data["ui_data"]:
    
    
            ui_obj.intent_to_task(i,db_names )
            con_dict = ["data uploaded"]
    return JsonResponse(con_dict, safe=False)


@csrf_exempt
def work_flow_data_save(request):

    data = JSONParser().parse(request)
    db_to_ui_obj = DataBaseToUi()


    print("==================== in work_flow_data_save DB TO UI ============")

    converted_db_to_ui = db_to_ui_obj.ui_generator(db_name["data_base"] )
    con_dict = ["data uploaded"]
    return JsonResponse(converted_db_to_ui, safe=False)



@csrf_exempt
def get_train_data(request):
    train_list_flag = True

    dict_train = {}
    train_data_list = []
    data = JSONParser().parse(request)
    tag = data["taskName"]
    training_data = db["training_data_updated"].find({"tag":tag})
    for each_train in training_data:
                for each_pattern in each_train["patterns"]:
                   
                    train_data_list.append(each_pattern)
    if not train_data_list:
        train_list_flag = False
    print(train_data_list)
    dict_train["taskName"] = tag
    dict_train["trainList"] = train_data_list
    dict_train["train_list_flag"] = train_list_flag



    return JsonResponse(dict_train, safe=False)



@csrf_exempt
def save_train_data(request):
    data = JSONParser().parse(request)
   
    

    task_name = data["taskName"]
    each_data = data["trainList"]

    
    list_var = []
    trainingData_dict = {}

    trainingData_dict["tag"] = task_name
    
    for each_training_data  in each_data:
            list_var.append(each_training_data)
    if list_var:
    
        trainingData_dict["patterns"] = list_var
        

        # tag  = db_conn["train_chek"].find()
        try:
            db["training_data_updated"].update({"tag":trainingData_dict["tag"]},{"$set": trainingData_dict}, upsert = True)
            # db_conn["train_chek"].insert( deepcopy(trainingData_dict))

        
        except Exception as e:
            print(e, "---------task train_data ui to db-------------")

    responce = "updated traiining data"
    return JsonResponse(responce, safe=False)








@login_required
def faq_Create(request):
    dict_con = {}
    faq_detail = FAQ.objects.all()
    dict_con['faq_detail'] = faq_detail
    # print(request)
    upload_img = ""
    audio = ""
    video = ""
    doc = ""

    if request.method == 'POST' :

        # if request.FILES['faqimage'] or request.FILES['audio'] or request.FILES['video'] or request.FILES['doc']:
        question = request.POST['question']
        answer = request.POST['answer']

        question_seq = request.POST['question_seq']
        answer_seq = request.POST['answer_seq']
        audio_seq = request.POST['audio_seq']
        video_seq = request.POST['video_seq']
        image_seq = request.POST['image_seq']
        doc_seq = request.POST['doc_seq']

        try:
                upload_img = request.FILES['faqimage']
                audio = request.FILES['audio']
                video = request.FILES['video']
                doc = request.FILES['doc']
                fsi = FileSystemStorage(location= path+'/images')
                fsa = FileSystemStorage(location= path+'/audio')
                fsv = FileSystemStorage(location= path+'/video')
                fsd = FileSystemStorage(location= path+'/doc')
                filenamei = fsi.save(upload_img.name, upload_img)
                filenamea = fsa.save(audio.name, audio)
                filenamev = fsv.save(video.name, video)
                filenamed = fsd.save(doc.name, doc)
                uploaded_file_urli = fsi.url(filenamei)
                uploaded_file_urla = fsa.url(filenamea)
                uploaded_file_urlv = fsv.url(filenamev)
                uploaded_file_urld = fsd.url(filenamed)
        except Exception as e:
                print(e)

            # print(uploaded_file_urli)
        if upload_img:
            upload_img = upload_img.name
        else:
            upload_img = ""

        if audio:
            audio = audio.name
        else:
            audio = ""

        if video:
            video = video.name
        else:
            video = ""

        if doc:
            doc = doc.name
        else:
            doc = ""
        if len(faq_detail)==0:
                idss = 1
        else:
                idss =max(i.id for i in faq_detail)+1

        a = FAQ.objects.create(id=idss, question=question.strip() , answer=answer.strip(), audio=audio,
                                   video=video,image=upload_img, doc=doc, question_seq = question_seq,
                                  answer_seq =answer_seq,audio_seq =audio_seq,video_seq = video_seq,
                                 image_seq =image_seq,doc_seq =doc_seq)
        a.save()
    return render(request, 'FAQ_templates/db.html', dict_con)


@login_required
def faq_delete(request, id):
    dict_con = {}
    if len(FAQ.objects.all()) == 1:
        dict_con['last_one_data_error'] = "Sorry you can't Delete last Record. Becouse one data is mandatory "
    else:
        a = FAQ.objects.filter(id=id).delete()
        dict_con['a'] = a
    a = FAQ.objects.filter(id=id).delete()
    dict_con['a'] = a
    faq_detail = FAQ.objects.all()
    dict_con['faq_detail'] = faq_detail
    return render(request, 'FAQ_templates/db.html', dict_con)

@login_required
def faq_edit_pre(request, id):
    dict_con = {}
    faq_edit_detail = FAQ.objects.get(id=id)
    dict_con['faq_edit_detail'] = faq_edit_detail
    return render(request, 'FAQ_templates/db.html', dict_con)


@login_required
def faq_edit(request):
    dict_con = {}
    faq_detail = FAQ.objects.all()
    dict_con['faq_detail'] = faq_detail
    # print(request)
    upload_img = ""
    audio = ""
    video = ""
    doc = ""

    if request.method == 'POST' :
        # if request.FILES['faqimage'] or request.FILES['audio'] or request.FILES['video'] or request.FILES['doc']:
            ids = request.POST['idss']
            question = request.POST['question']
            answer = request.POST['answer']

            question_seq = request.POST['question_seq']
            answer_seq = request.POST['answer_seq']
            audio_seq = request.POST['audio_seq']
            video_seq = request.POST['video_seq']
            image_seq = request.POST['image_seq']
            doc_seq = request.POST['doc_seq']
            try:
                upload_img = request.FILES['faqimage']
                audio = request.FILES['audio']
                video = request.FILES['video']
                doc = request.FILES['doc']

                # print(upload_img)
                me = os.path.join(BASE_DIR, "media")
                # print(me+upload_img.name)
                path = "C:/Bitnami/wampstack-7.1.26-0/apache2/htdocs/media"
                fsi = FileSystemStorage(location= path+'/images')
                fsa = FileSystemStorage(location= path+'/audio')
                fsv = FileSystemStorage(location= path+'/video')
                fsd = FileSystemStorage(location= path+'/doc')
                filenamei = fsi.save(upload_img.name, upload_img)
                filenamea = fsa.save(audio.name, audio)
                filenamev = fsv.save(video.name, video)
                filenamed = fsd.save(doc.name, doc)
                uploaded_file_urli = fsi.url(filenamei)
                uploaded_file_urla = fsa.url(filenamea)
                uploaded_file_urlv = fsv.url(filenamev)
                uploaded_file_urld = fsd.url(filenamed)

                # print(uploaded_file_urli)
            except Exception as e:
                    print("FAQ EDIT",e)
            if upload_img:
                upload_img = upload_img.name
            else:
                upload_img = ""

            if audio:
                audio = audio.name
            else:
                audio = ""

            if video:
                video = video.name
            else:
                video = ""

            if doc:
                doc = doc.name
            else:
                doc = ""


            FAQ.objects.get(id=ids).update( question=question , answer=answer, audio=audio,
                                   video=video,image=upload_img, doc=doc,question_seq = question_seq,
                                  answer_seq =answer_seq,audio_seq =audio_seq,video_seq = video_seq,
                                 image_seq =image_seq,doc_seq =doc_seq )

    return render(request, 'FAQ_templates/db.html', dict_con)
@csrf_exempt
def ok_thanks(request):
   con_dict =  [{"type": "text",
                "sequence": "1",
                "value": "worked"
            }]
   return JsonResponse(con_dict, safe=False)

@csrf_exempt
def flow(request):
   con_dict =  [{"type": "text",
                "sequence": "1",
                "value": "val"
            }]
   return JsonResponse(con_dict, safe=False)

@csrf_exempt
def identifier(request):
    data = JSONParser().parse(request)
    if "identifire" in data:
        get_id = data["identifire"]
     
        if get_id:
            con_dict =["yesssss data available"]
    else:
        con_dict = ["data not available"]
    return JsonResponse(con_dict, safe=False)






@csrf_exempt
def otp_sender(request):
    data = JSONParser().parse(request)
    email_id = ["priyankas.light@gmail.com", "bhujbalashwini5@gmail.com", "shejad@gmail.com"]
    mob_num = (data["mob_num"])
    #======================Generat otp===============================================
    digits = "0123456789"
    OTP = "" 
    for i in range(4) : 
        OTP += digits[math.floor(random.random() * 10)] 

    db["number_matcher"].update({},{'$push': {'random_number': OTP}})
 #==================== send otp on email====================================
 

    message ="OTP number for the given mobile number i.e " + mob_num +"to verify telecom bot is "+OTP+" Please provide us"
    Subject = "Telecom bot otp"
    filexlsx = settings.os.path.join(settings.BASE_DIR, 'German_Pension_Reform_2018.pdf')
    emaildata = EmailMultiAlternatives(Subject, message, settings.EMAIL_HOST_USER,email_id)

    emaildata.content_subtype = "html"

    # emaildata.attach_file(filexlsx) #you can send mulitpal email as like

    emaildata.send()

    # con_dict = {"message": OTP}

    # return JsonResponse(con_dict, safe=False)
    
    # account_sid = 'AC1ee7e3dd0cfe66bdef0c43fb6a80e94b'
    # auth_token = 'aa1d6692ddecbe54c07897fda30e5397'
    # client = Client(account_sid, auth_token)
    # message = "This is your otp code"+OTP +"Please provide us to verify"
    # message = client.messages \
    #                 .create(
    #                     body=OTP ,
    #                     from_='+17403138321',
    #                     to=data["mob_num"]
    #                 )

    # print(message.sid)
    con_dict = {}
    return JsonResponse(con_dict, safe=False)

@csrf_exempt
def match_otp(request):
    data = JSONParser().parse(request)
    

    num_list = db["number_matcher"].find({},{"random_number":1})
    con_dict = (num_list[0]["random_number"])

    return JsonResponse(con_dict, safe=False)

@csrf_exempt
def auto_search(request):
    query = {}
    query = JSONParser().parse(request)
    list_match_string =[]
    final_list = []
    list_query = []
   
    collection = db['training_data']
    for obj in collection.find():
        for key , value in obj.items():
            if isinstance(value, list):
                list_query.extend(value)
   
   
    if "user_query" in query:
        if query["user_query"]:
            results = process.extract(query["user_query"], list_query)
            for ind, each_question in enumerate(results):
                # list_match_string.append(each[0])
                temp_dict = {}
                temp_dict ={"label":each_question[0], "value":0+ind}
                # print(each_question )
                final_list.append(temp_dict)
        
    else:
        results = []

    # print(final_list)
    

    

    return JsonResponse(final_list, safe=False)



@csrf_exempt
def all_list(request):
    list_query = []

    lists = []
    faq_col = db["f_a_q"]
    faq = faq_col.find()
    for each_faq in faq:
        if "#" not in (each_faq["question"]):
            lists.append(each_faq["question"])
            list_query.extend(lists)
        if "question" in each_faq:
            if "#" in (each_faq["question"]):
                n_list = each_faq["question"].split("#")
                list_query.extend(n_list)

            # list_query.extend(each_faq)

    collection = db['training_data']
    for obj in collection.find():
        for key, value in obj.items():
            if isinstance(value, list):
                list_query.extend(value)

    return JsonResponse(list_query, safe=False)


@csrf_exempt
def has_kb(request):
    con_dict ={"data":"has kb"}
    return JsonResponse(con_dict, safe=False)


@csrf_exempt
def no_kb(request):
    con_dict ={"data":"no kb"}
    return JsonResponse(con_dict, safe=False)


@csrf_exempt
def all_surrender_value(request):
    con_dict ={"message":"PLC123, PLC5667"}

    return JsonResponse(con_dict, safe=False)

@csrf_exempt
def surrender_value(request):
    # con_dict={}
    # data = JSONParser().parse(request)
    # print(data)
    # con_dict["message"]="The surrender value is 20k USD for {0}".format(data["policies_no"])

    data_items=[{
        'type':'type',
        'sequence':'',
        'value':'The surrender value is 20k USD'
         }]

    #con_dict={'type': 'type', 'sequence': '1','value':"The surrender value is 20k USD"}
    # con_dict.extend({
    #     "type": type,
    #     "sequence": '1',
    #     "value": 'The surrender value is 20k USD'
    # })

    #con_dict.append([{'type': 'text', 'sequence': '1','value':"The surrender value is 20k USD"}])

    return JsonResponse(data_items, safe=False)


@csrf_exempt
def ok_thanks(request):

    con_dict = "great thanks"

    return JsonResponse(con_dict, safe=False)

@csrf_exempt
def request_no(request):
    import random
    rand=(random.randint(100, 999))
    data_item=[{
        'type': 'text',
        'sequence': '',
        'value': 'The request number is REQ '+str(rand)
    }]
    #con_dict ={"message":"Le numéro de requête est REQ "+str(rand)}

    return JsonResponse(data_item, safe=False)

@csrf_exempt
def list_of_products(request):
    # add = "https://www.howtogermany.com/pages/private-pension-plans.html"
    # text = "Product_1"
    # con_dict = """<a href="http://https://www.howtogermany.com/pages/private-pension-plans.html" target="_blank">Product_1</a>"""
    # con_dict = {"text": "Product_1: <https://www.howtogermany.com/pages/private-pension-plans.html>"}
    # con_dict={"message": "1. Product_1  2. Product_2"}
    con_dict = {
        "message": """<a href="https://en.wikipedia.org/wiki/Pensions_in_Germany" target="_blank">Product_1</a>""" "       " "      " """<a href="https://www.howtogermany.com/pages/german-retirement.html" target="_blank">Product_2</a>  """}
    return JsonResponse(con_dict, safe=False)

@csrf_exempt
def policy_email(request):
    data = JSONParser().parse(request)


    email_id = []
    for k, v in data.items():

        if k == "new_policy_email":
            email_id.append(v)

        elif k == "nominee_email":
            email_id.append(v)

    Subject = "****Policy Mail****"

    Message = "This mail about Policy request is successfully generated"
    send_mail(Subject, Message, settings.EMAIL_HOST_USER, email_id)
    con_dict = ""
    return JsonResponse(con_dict, safe=False)


@csrf_exempt
def FAQ_training(request):
    #===================== for faq training =====================#
    # faq_obj.max_cosine_value("hi")
    faq_obj = faq_training()
    faq_obj.faq("hi")

    con_dict ={"message":"FAQ Trained"}

    return JsonResponse(con_dict, safe=False)

@csrf_exempt
def faq_task(request):
     #===================== for faq service as ask recommendation    =====================#

    response_text_list = []
    fin_list = []
    context_data ={}
    data = JSONParser().parse(request)
    user_uttarance = data["user_uttarance"]

    faq_obj=Faq_Engine()
    faq_extractor = FAQ_Extractor()

    faq_list = faq_obj.faq_engine1(user_uttarance)

    if faq_list:


        extracted_ans = faq_extractor.faq_extractor_function(faq_list)

    else:

        extracted_ans=[{
        'type': 'text',
        'sequence': '',
        'value': 'Hey buddy...! please try with different keywords'
        }]
    return JsonResponse(extracted_ans, safe=False)
@csrf_exempt
def faq_ask(request):
    response_text_list = []
    fin_list = []
    context_data ={}
    data = JSONParser().parse(request)
    user_uttarance = data["user_uttarance"]

    faq_obj=Faq_Engine()
    faq_extractor = FAQ_Extractor()

    faq_list = faq_obj.faq_engine1(user_uttarance)

    if faq_list:


        extracted_ans = faq_extractor.faq_extractor_function(faq_list)

    else:

        extracted_ans=[{
            'type': 'text',
            'sequence': '',
            'value': 'Hey buddy...! please try asking a different way.'
            }]

    return JsonResponse(extracted_ans, safe=False)

@csrf_exempt
def tricontes_call(request):
    data=[{
        'type': 'text',
        'sequence': '',
        'value': 'Perfect! We will get back to you:), Thanks for visit'
    }]
    return JsonResponse(data, safe=False)

@csrf_exempt
def tricontes_training(request):
    data=[{
        'type': 'text',
        'sequence': '',
        'value': 'Hey.. Thanks for visit'
    }]
    return JsonResponse(data, safe=False)

@csrf_exempt
def tricontes_ask_question(request):
    data=[{
        'type': 'text',
        'sequence': '',
        'value': 'Please ask your question'
    }]
    return JsonResponse(data, safe=False)

##### Tricontes GermanBot Services ####
@csrf_exempt
def tricontes_german_call(request):
    data=[{
        'type': 'text',
        'sequence': '',
        'value': 'Perfekt! Wir werden uns bei dir melden'
    }]
    return JsonResponse(data, safe=False)

@csrf_exempt
def tricontes_german_training(request):
    data=[{
        'type': 'text',
        'sequence': '',
        'value': 'Schade, welche Fragen hast du den noch?  Vielleicht kann ich dich ja doch noch überzeugen '
    }]
    return JsonResponse(data, safe=False)

@csrf_exempt
def tricontes_geraman_ask_question(request):
    data=[{
        'type': 'text',
        'sequence': '',
        'value': 'Bitte stellen Sie Ihre Frage'
    }]
    return JsonResponse(data, safe=False)

############ APRICOT SERVICES #####
@csrf_exempt
def apricot_process(request):
    data_item=[{
        'type': 'document',
        'sequence': '',
        "value": """https://en.wikipedia.org/wiki/Apricot"""

    }]
    return JsonResponse(data_item, safe=False)


@csrf_exempt
def Archieved_version(request):
    data_item=[{
        'type': 'document',
        'sequence': '',
        "value": """https://gethelp.wildapricot.com/en/articles/516-version-history"""

    }]
    return JsonResponse(data_item, safe=False)

@csrf_exempt
def customer_care(request):
    data_item=[{
        'type': 'text',
        'sequence': '',
        'value': """Please don't hesitate to call me at [123-456-7891] for Customer Care Support. If you have any further questions or concerns, let us know. We are here 24/7 and always happy to help. Take care"""
    }]
    #con_dict ={"message":"Le numéro de requête est REQ "+str(rand)}

    return JsonResponse(data_item, safe=False)


@csrf_exempt
def new_updates(request):
    data_item=[{
        'type': 'document',
        'sequence': '',
        "value": """https://en.wikipedia.org/wiki/News"""

    }]
    return JsonResponse(data_item, safe=False)

################################################################
########## NBFC SERVICES ########## START #######
######NBFC####
@csrf_exempt
def salary_loan(request):
    data = JSONParser().parse(request)

    salary = []
    liability = []
    total = []
    # import pdb
    # db.set_trace()
    for k, v in data.items():

        if k == "number":
            salary.append(v)
        if k == "liabilities":
            liability.append(v)

            yearly = int(salary[0]) * 12

            total = int(yearly) - int(liability[0])

            if yearly >= int(liability[0]):

                if int(total) <= 20000:
                    data_item = [{
                        'type': 'text',
                        'sequence': '',
                        "value": "You are eligible for 2 lakh rupees amount of loan."
                    }]

                elif int(total) > 20000 and int(total) < 50000:
                    data_item = [{
                        'type': 'text',
                        'sequence': '',
                        "value": "You are eligible for 5 lakh rupees amount of loan."
                    }]

                elif int(total) >= 50000:
                    data_item = [{
                        'type': 'text',
                        'sequence': '',
                        "value": "You are eligible for 10 lakh rupees amount of loan."
                    }]

            else:
                data_item = [{
                    'type': 'text',
                    'sequence': '',
                    "value": "You are not eligible for loan."
                }]

    return JsonResponse(data_item, safe=False)


@csrf_exempt
def loan_status(request):
    # import pdb
    # pdb.set_trace()
    data1 = JSONParser().parse(request)
    mongo_conn = pymongo.MongoClient()
    db = mongo_conn["nbfc_bot_new"]
    data = db["los"]
    # data_item=[]
    mobile = []
    for k, v in data1.items():

        if k == "mobile_no":
            mobile.append(v)

            for i in data.find({"mobile": mobile[0]}):
                # total = i["current_emi"]
                total = int(i["mobile"])
                # print(total)
                if total == int(mobile[0]):
                    var = i["status"]
                    # print(var)
                    data_item = [{
                        'type': 'text',
                        'sequence': '',
                        "value": var

                    }]
                    # data_item.append(data_item1)
                    # break
                else:
                    data_item = [{
                        'type': 'text',
                        'sequence': '',
                        "value": "Entered mobile number is not valid."
                    }]
                    # data_item.append(data_item1)

    return JsonResponse(data_item, safe=False)


@csrf_exempt
def loan_sanction(request):
    # import pdb
    # pdb.set_trace()
    data1 = JSONParser().parse(request)
    mongo_conn = pymongo.MongoClient()
    db = mongo_conn["nbfc_bot_new"]
    data = db["los"]
    # data_item=[]
    mobile = []
    for k, v in data1.items():

        if k == "mobile_no":
            mobile.append(v)

            for i in data.find({"mobile": mobile[0]}):
                # total = i["current_emi"]
                total = int(i["mobile"])
                # print(total)
                if total == int(mobile[0]):
                    var = i["sanction_amt"]
                    # print(var)
                    data_item = [{
                        'type': 'text',
                        'sequence': '',
                        "value": f"Your sanctioned amount is: Rs.{var}"

                    }]
                    # data_item.append(data_item1)
                    # break
                else:
                    data_item = [{
                        'type': 'text',
                        'sequence': '',
                        "value": "Entered mobile number is not valid."
                    }]
                    # data_item.append(data_item1)

    return JsonResponse(data_item, safe=False)


###### LMS #######
@csrf_exempt
def penal_charges(request):
    # import pdb
    # pdb.set_trace()
    data1 = JSONParser().parse(request)
    import pymongo

    user_nm = []
    for k, v in data1.items():
        if k == "username":
            user_nm.append(v)

    import pymongo
    mongo_conn = pymongo.MongoClient()
    db = mongo_conn["nbfc_bot_new"]
    col = db["los"]
    data = col.find({"username": user_nm[0]})
    for each_data in data:
        sanction_amt = each_data['sanction_amt']
        # 1 % is the penal chargers on sanctioned amount
        para = 100 / 1
        penal_charges = int(sanction_amt) / int(para)
        # print("penal charges on your loan amount are: ", penal_charges)
        data_item = [{
            'type': 'text',
            'sequence': '',
            "value": "Penal charges on your loan amount is : Rs.{0}".format(penal_charges)
        }]
    return JsonResponse(data_item, safe=False)


@csrf_exempt
def current_mode_of_payment(request):
    data1 = JSONParser().parse(request)
    import pymongo

    user_nm = []
    for k, v in data1.items():
        if k == "username":
            user_nm.append(v)

    import pymongo
    mongo_conn = pymongo.MongoClient()
    db = mongo_conn["nbfc_bot_new"]
    col = db["los"]
    data = col.find({"username": user_nm[0]})
    for i in data:
        current_mode_of_payment = i['mode_of_payment']
        # print("your current mode of payment is", current_mode_of_paymanet)

        data_item = [{
            'type': 'text',
            'sequence': '',
            "value": "Your current mode of payment is : {0}".format(current_mode_of_payment)
        }]
    return JsonResponse(data_item, safe=False)


@csrf_exempt
def change_mode_of_payment(request):
    data1 = JSONParser().parse(request)
    import pymongo

    user_nm = []
    change_mode = []
    pick_up_loc = []
    pick_up_date = []
    for k, v in data1.items():
        if k == "username":
            user_nm.append(v)
        if k == "mode":
            change_mode.append(v)
        if k == "pick_date":
            pick_up_date.append(v)
        if k == "pick_location":
            pick_up_loc.append(v)

    import pymongo
    mongo_conn = pymongo.MongoClient()
    db = mongo_conn["nbfc_bot_new"]
    col = db["los"]
    change_mode_of_payment_is = change_mode[0]
    col.update_one({"username": user_nm[0]}, {"$set": {"mode_of_payment": change_mode_of_payment_is}})
    data = col.find({"username": user_nm[0]})
    for i in data:
        # current_mode_of_paymanet = i['mode_of_payment']
        # print("your current mode of payment is", current_mode_of_paymanet)

        current_mode_of_payment = i['mode_of_payment']

        if current_mode_of_payment.lower() == "imps":
            data_item = [{
                'type': 'text',
                'sequence': '',
                "value": f"""Your changed mode of payment is : {current_mode_of_payment}

<b>Your beneficiary details are:</b>
Beneficiary Account Holder : Admin
Beneficiary Account Number: 045001000567
Bank and branch name : Nell bank , pune
IFSC Code : NELLINFO
                """
            }]

        elif current_mode_of_payment.lower() == "neft":
            data_item = [{
                'type': 'text',
                'sequence': '',
                "value": f"""Your changed mode of payment is : {current_mode_of_payment}

<b>Your beneficiary details are:</b>
Beneficiary Account Holder : Admin
Beneficiary Account Number: 045001000567
Bank and branch name : Nell Infotech bank , pune
IFSC Code : NELLINFO
                            """
            }]

        elif current_mode_of_payment.lower() == "gateway":
            a = "https://retail.onlinesbi.com/personal/tax_retail.html"
            link = "<a target=_blank href={0} >gateway payment </a>".format(a)
            data_item = [{
                'type': 'text',
                'sequence': '',
                "value": f"""Your changed mode of payment is : {current_mode_of_payment}
<b>Click here for:</b> {link}
                            """
            }]

        elif current_mode_of_payment.lower() == "cheque":
            data_item = [{
                'type': 'text',
                'sequence': '',
                "value": f"""Your mode of payment is : {current_mode_of_payment}
<br>We will pick up your cheque on: <b>{pick_up_date[0]}</b>
from your given address:
<b>{pick_up_loc[0]}</b>
                    """

            }]

    return JsonResponse(data_item, safe=False)


@csrf_exempt
def outsatnding_amt(request):
    # import pdb
    # pdb.set_trace()
    data1 = JSONParser().parse(request)
    mongo_conn = pymongo.MongoClient()
    db = mongo_conn["nbfc_bot_new"]
    data = db["los"]

    ad = []
    for k, v in data1.items():
        if k == "username":
            # number.append(v)
            ad.append(v)
            # mob_no=mob[0]
            for i in data.find({'username': ad[0]}):
                # if i['admin'] == 'admin1':
                sanction_amt = i['sanction_amt']
                emi_paid = i['emi_paid']
                outsatnding_amt = int(sanction_amt) - int(emi_paid)
                data_item = [{
                    'type': 'text',
                    'sequence': '',
                    "value": f"Your outstanding amount is: {outsatnding_amt} rupees."
                }]
                # data_i.append(data_item)
        return JsonResponse(data_item, safe=False)


@csrf_exempt
def request_waive_charges(request):
    # import pdb
    import pymongo
    # pdb.set_trace()
    data1 = JSONParser().parse(request)
    mongo_conn = pymongo.MongoClient()
    db = mongo_conn["nbfc_bot_new"]
    data = db.los
    # data_item = []
    username = []
    # transaction_type = []
    # transaction_amt = []
    for k, v in data1.items():
        if k == "username":
            username.append(v)
            # transaction_type.append(v)
            # transaction_amt.append(v)
            username = username[0]
            for i in data.find({'username': str(username)}):
                if i['username'] == str(username):
                    if (data1['transaction_type']).lower() == 'dd':
                        # "You have selected DD trasnsaction_type"
                        if data1['transaction_amt'] <= "10000":
                            charges = int(data1['transaction_amt']) * 0.02 / 100
                        elif data1['transaction_amt'] == "10000" and data1['transaction_amt'] <= "50000":
                            charges = int(data1['transaction_amt']) * 0.04 / 100
                        elif data1['transaction_amt'] == "50000" and data1['transaction_amt'] <= "100000":
                            charges = int(data1['transaction_amt']) * 0.05 / 100
                        else:
                            charges = int(data1['transaction_amt']) * 0.10 / 100

                        data_item = [{
                            'type': 'text',
                            'sequence': '',
                            "value": f"You have charged Rs.: {charges}"
                        }]

                    elif (data1['transaction_type']).lower() == "neft":

                        # print("You have selected NEFT trasnsaction_type")
                        if data1['transaction_amt'] <= "10000":
                            charges = int(data1['transaction_amt']) * 0.002 / 100
                        elif data1['transaction_amt'] == "10000" and data1['transaction_amt'] <= "50000":
                            charges = int(data1['transaction_amt']) * 0.004 / 100
                        elif data1['transaction_amt'] == "50000" and data1['transaction_amt'] <= "100000":
                            charges = int(data1['transaction_amt']) * 0.005 / 100
                        else:
                            charges = int(data1['transaction_amt']) * 0.01 / 100

                        data_item = [{
                            'type': 'text',
                            'sequence': '',
                            "value": f"You have charged Rs.: {charges}"
                        }]

                    elif (data1['transaction_type']).lower() == "gateway":
                        # print("You have selected GATEWAY trasnsaction_type")
                        if data1['transaction_amt'] <= "10000":
                            charges = int(data1['transaction_amt']) * 0.01 / 100
                        elif data1['transaction_amt'] == "10000" and data1['transaction_amt'] <= "50000":
                            charges = int(data1['transaction_amt']) * 0.02 / 100
                        elif data1['transaction_amt'] == "50000" and data1['transaction_amt'] <= "100000":
                            charges = int(data1['transaction_amt']) * 0.03 / 100
                        else:
                            charges = int(data1['transaction_amt']) * 0.5 / 100
                        data_item = [{
                            'type': 'text',
                            'sequence': '',
                            "value": f"You have charged Rs.: {charges}"
                        }]

                    elif (data1['transaction_type']).lower() == "imps":
                        # print("You have selected GATEWAY trasnsaction_type")
                        if data1['transaction_amt'] <= "10000":
                            charges = int(data1['transaction_amt']) * 0.015 / 100
                        elif data1['transaction_amt'] == "10000" and data1['transaction_amt'] <= "50000":
                            charges = int(data1['transaction_amt']) * 0.025 / 100
                        elif data1['transaction_amt'] == "50000" and data1['transaction_amt'] <= "100000":
                            charges = int(data1['transaction_amt']) * 0.035 / 100
                        else:
                            charges = int(data1['transaction_amt']) * 0.50 / 100
                        data_item = [{
                            'type': 'text',
                            'sequence': '',
                            "value": f"You have charged Rs.: {charges}"
                        }]

                    else:
                        data_item = [{
                            'type': 'text',
                            'sequence': '',
                            "value": f"Invalid Transaction Type... "
                        }]

                # data_item.append(data_item1)
                return JsonResponse(data_item, safe=False)


@csrf_exempt
def waive_charges(request):
    data = JSONParser().parse(request)

    email_id = []
    for k, v in data.items():

        if k == "email":
            email_id.append(v)

        data_item = [{
            'type': 'text',
            'sequence': '',
            "value": f"Thank you for your response. We will contact you soon."
        }]
    return JsonResponse(data_item, safe=False)


@csrf_exempt
def emi_tenure(request):
    # import pdb
    # pdb.set_trace()
    data1 = JSONParser().parse(request)
    mongo_conn = pymongo.MongoClient()
    db = mongo_conn["nbfc_bot_new"]
    data = db.los
    # data_item = []
    name = []
    pay = []
    choice = []
    # import pdb
    # pdb.set_trace()
    for k, v in data1.items():
        if k == "username":
            name.append(v)
        if k == "will_pay":
            pay.append(v)
        if k == "option":
            choice.append(v)

    for i in data.find({"username": name[0]}):
        sanc_amt = int(i["sanction_amt"])
        cur_emi = int(i["current_emi"])
        tenure_data = int(i["tenure"])
        emi_p = int(i["emi_paid"])
        select = choice[0].lower()

        if select == "reduce":
            new_reduced_emi = (sanc_amt - int(pay[0]) - emi_p) / tenure_data
            data.update_one({"username": name[0]}, {"$set": {"new_reduced_emi": str(new_reduced_emi)}})

            data_item = [{
                'type': 'text',
                'sequence': '',
                "value": f"Your newly reduced EMI will be: {new_reduced_emi} rupees."
            }]

        elif select == "reduce tenure":
            new_reduced_tenure = (sanc_amt - int(pay[0]) - emi_p) / cur_emi
            round_tenure = round(new_reduced_tenure)
            data.update_one({"username": "admin"}, {"$set": {"new_reduced_tenure": str(round_tenure)}})

            data_item = [{
                'type': 'text',
                'sequence': '',
                "value": f"Your newly reduced Tenure will be: {round_tenure} months."
            }]

        else:
            data_item = [{
                'type': 'text',
                'sequence': '',
                "value": f"Not valid."
            }]

    return JsonResponse(data_item, safe=False)


@csrf_exempt
def principal_amount(request):
    # import pdb
    # pdb.set_trace()
    data1 = JSONParser().parse(request)
    mongo_conn = pymongo.MongoClient()
    db = mongo_conn["nbfc_bot_new"]
    data = db.los
    # data_item = []
    name = []
    pay = []
    for k, v in data1.items():
        if k == "username":
            name.append(v)

            for i in data.find({"username": name[0]}):
                san_amt = i["sanction_amt"]
                # "sanction_amt" : "400000"
                emi = i["emi_paid"]
                # "emi_paid" : "88000"
                interest = int(san_amt) * float(0.1)
                # interest = 40000
                total_amt_to_pay = int(san_amt) + interest
                interest1 = (int(total_amt_to_pay) - int(emi)) * float(0.1)
                foreclose_paying_amt = int(total_amt_to_pay) - int(emi) + float(interest1)
                # p = 352000
                # interest = int(san_amt) * float(0.1)
                principal_amt = int(total_amt_to_pay) - int(emi)
                total_interest = 0.1 * principal_amt
                data_item = [{
                    'type': 'text',
                    'sequence': '',
                    "value": f"""Your remaining amount to pay is: Rs.{foreclose_paying_amt}
                               <br>Your principle amount is: Rs.{principal_amt} and Interest is: Rs.{total_interest}."""

                }]

        return JsonResponse(data_item, safe=False)


@csrf_exempt
def p_payment_mode(request):
    data1 = JSONParser().parse(request)
    import pymongo
    # import pdb
    # pdb.set_trace()
    user_nm = []
    change_mode = []
    pick_up_date = []
    pick_up_loc = []
    for k, v in data1.items():
        if k == "username":
            user_nm.append(v)
        if k == "mode":
            change_mode.append(v)
        if k == "pick_date":
            pick_up_date.append(v)
        if k == "pick_location":
            pick_up_loc.append(v)

    import pymongo
    mongo_conn = pymongo.MongoClient()
    db = mongo_conn["nbfc_bot_new"]
    col = db["los"]
    change_mode_of_payment_is = change_mode[0]
    col.update_one({"username": user_nm[0]}, {"$set": {"mode_of_payment": change_mode_of_payment_is}})
    data = col.find({"username": user_nm[0]})
    for i in data:
        # current_mode_of_paymanet = i['mode_of_payment']
        # print("your current mode of payment is", current_mode_of_paymanet)

        current_mode_of_payment = i['mode_of_payment']

    if current_mode_of_payment.lower() == "neft":
        data_item = [{
            'type': 'text',
            'sequence': '',
            "value": f"""Your mode of payment is :{current_mode_of_payment}
<br><b>Your beneficiary details are:</b>
Beneficiary Account Holder : Admin
Beneficiary Account Number: 045001000567
Bank and branch name : Nell bank , pune
IFSC Code : NELLINFO
                           """
        }]

    elif current_mode_of_payment.lower() == "imps":
        data_item = [{
            'type': 'text',
            'sequence': '',
            "value": f"""Your mode of payment is :{current_mode_of_payment}

<b>Your beneficiary details are:</b>
Beneficiary Account Holder : Admin
Beneficiary Account Number: 045001000567
Bank and branch name : nell bank , pune
IFSC Code : NELLINFO
                            """
        }]

    elif current_mode_of_payment.lower() == "gateway":
        a = "https://retail.onlinesbi.com/personal/tax_retail.html"
        link = "<a target=_blank href={0} >gateway payment </a>".format(a)
        data_item = [{
            'type': 'text',
            'sequence': '',
            "value": f"""Your mode of payment is :{current_mode_of_payment}
<b>Click here for:</b> {link}
                            """
        }]

    elif current_mode_of_payment.lower() == "cheque":
        data_item = [{
            'type': 'text',
            'sequence': '',
            "value": f"""Your mode of payment is : {current_mode_of_payment}  
<br>We will pick up your cheque on: <b>{pick_up_date[0]}</b>
from your given address:
<b>{pick_up_loc[0]}</b>
                    """
        }]

    return JsonResponse(data_item, safe=False)


####### Validation of OTP from email/mobile ################
from django.http import HttpResponse


@csrf_exempt
def my_otp_match(request):
    data = JSONParser().parse(request)
    enterted_otp = data['otp']

    # user_input = input("Enter your OTP")

    import pymongo
    mongo_conn = pymongo.MongoClient()
    db = mongo_conn["nbfc_bot_new"]
    col = db["otp"]
    data = col.find({"ID": "admin"})
    db_otp = [i['otp_data'] for i in data]
    # user_input = input("Enter your otp")
    output = []
    if enterted_otp == db_otp[0]:
        output1 = "yes"
        # output.append(output1)
    else:
        output1 = "no"
        # output.append(output1)
    return HttpResponse(output1)


# from django.http import HttpResponse
# @csrf_exempt
# def myview(request):
#     text="return this string"
#     return HttpResponse(text)

########################################################
###### MOBILE OTP SENDER #################

@csrf_exempt
def send_otp_to_mobile(request):
    data = JSONParser().parse(request)
    mobile_no = data['mobile_no']
    ####################### GENERATE OTP NO####################
    import random as r
    bot_otp = ""
    for i in range(4):
        bot_otp += str(r.randint(1, 9))
    # print("Your One Time Password is ")
    # print(otp)

    ####################################SMS SENDING ####################
    import requests

    url = "https://www.fast2sms.com/dev/bulk"
    payload = "sender_id=FSTSMS&message=Your OTP for NBFS Bot is {0}&language=english&route=p&numbers={1}".format(
        bot_otp, mobile_no)
    headers = {'authorization': "ya2fkilF7FGkUf3K1M7Xv7BSof2QLEgaXPx1v8YnEpERgx3bcBItSWvEJXRt",
               'Content-Type': "application/x-www-form-urlencoded", 'Cache-Control': "no-cache", }
    # print(payload)

    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)

    ################### SAVE OTP ###################
    import pymongo
    mongo_conn = pymongo.MongoClient()
    db = mongo_conn["nbfc_bot_new"]
    col = db["otp"]
    col.update_one({"ID": "admin"}, {"$set": {"otp_data": bot_otp}})

    #########################################################
    output1 = "OTP has sent to Your mobile number {0}".format(mobile_no)
    data_item = [{
        'type': 'text',
        'sequence': '',
        "value": output1

    }]
    return JsonResponse(data_item, safe=False)


@csrf_exempt
def send_otp_to_email(request):
    ##############################SEND OTP TO EMAIL ################3
    # https://realpython.com/python-send-email/
    data = JSONParser().parse(request)
    import email, smtplib, ssl

    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from os import path

    ##################################################### OTP NO GENERATOR ####+++++++++++++++++++++++++++++++++++++++++++++++
    import random as r
    otp = ""
    for i in range(4):
        otp += str(r.randint(1, 9))
    # print("Your One Time Password is ")
    # print(otp)
    #############

    subject = "OTP"
    body = "Your OTP is: {0}".format(otp)

    ################################################## MAIL SENDING#################
    # sender_address = 'nell.paresh@gmail.com'
    # sender_pass = 'Test@123'
    sender_email = "nell.paresh@gmail.com"
    receiver_email = data['user_email']
    password = "Test@123"

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    message.attach(MIMEText(body, "plain"))

    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)

    ######################################################### OTP VERIFICATION ###################
    ######## SAVE OTP #############
    import pymongo
    mongo_conn = pymongo.MongoClient()
    db = mongo_conn["nbfc_bot_new"]
    col = db["otp"]
    col.update_one({"ID": "admin"}, {"$set": {"otp_data": otp}})
    # data = col.find({"ID": "admin"})

    # data_item=[{
    #    'type': 'text',
    #    'sequence': '',
    #    "value": """OTP has sent on your email id"""

    # }]
    return JsonResponse(safe=False)


@csrf_exempt
def send_mail_attachment_for_statement(request):
    data = JSONParser().parse(request)

    import email, smtplib, ssl
    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from os import path

    # receiver_email = data['user_email']
    subject = "NBFC Bot account statement"
    body = "This mail is from NBFC Bot. Please find the attachment for your detail account statement."
    # sender_address = 'nell.paresh@gmail.com'
    # sender_pass = 'Test@123'
    sender_email = "nell.paresh@gmail.com"
    receiver_email = data['user_email']
    password = "Test@123"
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails
    # Add body to email
    message.attach(MIMEText(body, "plain"))
    import os
    # path1 = os.path.join(os.path.dirname(os.path.dirname(__file__)))
    # print(path)
    # final_path= path + "/attchment/"+'dataclean.pdf'
    # filename = final_path  # In same directory as script
    filename = path.relpath(
        "C:/Program Files/Apache Software Foundation/Tomcat 9.0/webapps/NELL_BOT/media/pdf/statement.pdf")
    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)
    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )
    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()
    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
    final_data_item = []
    data_item1 = {
        'type': 'text',
        'sequence': '1',
        "value": "Your account statement has been sent on your email id."
    }
    data_item2 = {
        'type': 'document',
        'sequence': '2',
        "value": 'http://ec2-3-19-215-125.us-east-2.compute.amazonaws.com:8080/NELL_BOT/media/pdf/statement.pdf'
    }
    final_data_item.append(data_item1)
    final_data_item.append(data_item2)

    return JsonResponse(final_data_item, safe=False)


@csrf_exempt
def send_mail_attachment_for_request_invoice(request):
    data = JSONParser().parse(request)

    import email, smtplib, ssl
    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from os import path

    # receiver_email = data['user_email']
    subject = "NBFC Bot Request Invoice"
    body = "This mail is from NBFC Bot. Please find the attachment for your detail invoice."
    # sender_address = 'nell.paresh@gmail.com'
    # sender_pass = 'Test@123'
    sender_email = "nell.paresh@gmail.com"
    receiver_email = data['user_email']
    password = "Test@123"
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails
    # Add body to email
    message.attach(MIMEText(body, "plain"))
    import os
    # path1 = os.path.join(os.path.dirname(os.path.dirname(__file__)))
    # print(path)
    # final_path= path + "/attchment/"+'dataclean.pdf'
    # filename = final_path  # In same directory as script
    filename = path.relpath(
        "C:/Program Files/Apache Software Foundation/Tomcat 9.0/webapps/NELL_BOT/media/pdf/sample_invoice.pdf")
    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)
    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )
    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()
    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
    final_data_item = []
    data_item1 = {
        'type': 'text',
        'sequence': '1',
        "value": "Your requested invoice has been sent on your email id."
    }
    data_item2 = {
        'type': 'document',
        'sequence': '2',
        "value": """http://ec2-3-19-215-125.us-east-2.compute.amazonaws.com:8080/NELL_BOT/media/pdf/sample_invoice.pdf"""

    }
    final_data_item.append(data_item1)
    final_data_item.append(data_item2)

    return JsonResponse(final_data_item, safe=False)


@csrf_exempt
def send_mail_attachment_for_schedule_amt(request):
    data = JSONParser().parse(request)

    import email, smtplib, ssl
    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from os import path

    # receiver_email = data['user_email']
    subject = "NBFC Bot Schedule amount"
    body = "This mail is from NBFC Bot. Please find the attachment for your detail EMI schedule."
    # sender_address = 'nell.paresh@gmail.com'
    # sender_pass = 'Test@123'
    sender_email = "nell.paresh@gmail.com"
    receiver_email = data['user_email']
    password = "Test@123"
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails
    # Add body to email
    message.attach(MIMEText(body, "plain"))
    import os
    # path1 = os.path.join(os.path.dirname(os.path.dirname(__file__)))
    # print(path)
    # final_path= path + "/attchment/"+'dataclean.pdf'
    # filename = final_path  # In same directory as script
    filename = path.relpath(
        "C:/Program Files/Apache Software Foundation/Tomcat 9.0/webapps/NELL_BOT/media/pdf/loan_emi_schedule.pdf")
    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)
    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )
    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()
    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
    final_data_item = []
    data_item1 = {
        'type': 'text',
        'sequence': '1',
        "value": "Your EMI schedule has been sent on your email id."
    }
    data_item2 = {
        'type': 'document',
        'sequence': '',
        "value": """http://ec2-3-19-215-125.us-east-2.compute.amazonaws.com:8080/NELL_BOT/media/pdf/loan_emi_schedule.pdf"""

    }

    final_data_item.append(data_item1)
    final_data_item.append(data_item2)

    return JsonResponse(final_data_item, safe=False)


@csrf_exempt
def send_mail_attachment_for_req_no_due_certificate(request):
    data = JSONParser().parse(request)

    import email, smtplib, ssl
    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from os import path

    # receiver_email = data['user_email']
    subject = "NBFC Bot No Due Certificate"
    body = "This mail is from NBFC Bot. Please find the attachment for your detail No Due Certificate."
    # sender_address = 'nell.paresh@gmail.com'
    # sender_pass = 'Test@123'
    sender_email = "nell.paresh@gmail.com"
    receiver_email = data['user_email']
    password = "Test@123"
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails
    # Add body to email
    message.attach(MIMEText(body, "plain"))
    import os
    # path1 = os.path.join(os.path.dirname(os.path.dirname(__file__)))
    # print(path)
    # final_path= path + "/attchment/"+'dataclean.pdf'
    # filename = final_path  # In same directory as script
    filename = path.relpath(
        "C:/Program Files/Apache Software Foundation/Tomcat 9.0/webapps/NELL_BOT/media/pdf/no_due_certificate.pdf")
    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)
    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )
    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()
    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
    final_data_item = []
    data_item1 = {
        'type': 'text',
        'sequence': '1',
        "value": "Your No Due Certificate has been sent to your email id."
    }
    data_item2 = {
        'type': 'document',
        'sequence': '',
        "value": """http://ec2-3-19-215-125.us-east-2.compute.amazonaws.com:8080/NELL_BOT/media/pdf/no_due_certificate.pdf"""

    }

    final_data_item.append(data_item1)
    final_data_item.append(data_item2)

    return JsonResponse(final_data_item, safe=False)


@csrf_exempt
def db_change_emi_date(request):
    import datetime as dt
    from django.http import JsonResponse
    # import pdb
    # pdb.set_trace()
    data1 = JSONParser().parse(request)
    mongo_conn = pymongo.MongoClient()
    db = mongo_conn["nbfc_bot_new"]
    data = db.los

    now = dt.datetime.now()
    current_yr = now.year
    current_mnth = now.month
    current_date = now.day

    # curr_date = dt.datetime.now()
    # data_item = []

    username = []
    for k, v in data1.items():
        if k == "username":
            username.append(v)
            username = username[0]
            for i in data.find({'username': str(username)}):
                if i['username'] == str(username):

                    my_emi_date = i['emi_date'].split('-')
                    print(my_emi_date)
                    if (str(my_emi_date[0]) >= str(current_date)):
                        if (str(my_emi_date[0]) <= data1['user_date']):
                            user_date1 = data1['user_date'] + '-' + my_emi_date[1] + '-' + my_emi_date[2]
                            data.update_one(
                                {"username": data1["username"]},
                                {"$set": {"emi_date": user_date1}})

                            data_item = [{
                                'type': 'text',
                                'sequence': '',
                                "value": f"Your EMI date is updated with : {user_date1}"
                            }]
                        else:
                            current_mnth += 1
                            user_date1 = data1['user_date'] + '-' + str(current_mnth) + '-' + my_emi_date[2]
                            data.update_one(
                                {"username": data1["username"]},
                                {"$set": {"emi_date": user_date1}})

                            data_item = [{
                                'type': 'text',
                                'sequence': '',
                                "value": f"Your EMI date is updated with : {user_date1}"
                            }]

                    else:
                        current_mnth += 1
                        user_date1 = data1['user_date'] + '-' + str(current_mnth) + '-' + my_emi_date[2]

                        data.update_one(
                            {"username": data1["username"]},
                            {"$set": {"emi_date": user_date1}})

                        data_item = [{
                            'type': 'text',
                            'sequence': '',
                            "value": f"Your EMI date is updated with : {user_date1}"
                        }]

                        # current_mnth = 13
                        if current_mnth == 13:
                            current_mnth = 1
                            current_yr += 1
                            user_date1 = data1['user_date'] + '-' + str(current_mnth) + '-' + str(current_yr)

                            data.update_one(
                                {"username": data1["username"]},
                                {"$set": {"emi_date": user_date1}})

                            data_item = [{
                                'type': 'text',
                                'sequence': '',
                                "value": f"Your next EMI date in  is : {user_date1}"
                            }]

                return JsonResponse(data_item, safe=False)


@csrf_exempt
def db_next_emi_date(request):
    import datetime as dt
    from django.http import JsonResponse
    # import pdb
    # pdb.set_trace()
    data1 = JSONParser().parse(request)
    mongo_conn = pymongo.MongoClient()
    db = mongo_conn["nbfc_bot_new"]
    data = db.los

    now = dt.datetime.now()
    current_yr = now.year
    current_mnth = now.month
    current_date = now.day
    # time = now.time()

    # curr_date = dt.datetime.now()
    # data_item = []
    username = []
    for k, v in data1.items():
        if k == "username":
            username.append(v)
            for i in data.find({'username': str(username[0])}):
                if i['username'] == str(username[0]):
                    my_emi_date = i['emi_date'].split('-')
                    if (str(my_emi_date[0]) >= str(current_date)):
                        your_this_month_emi_date = i["emi_date"]
                        data_item = [{
                            'type': 'text',
                            'sequence': '',
                            "value": f"Your next EMI date will be on :{your_this_month_emi_date}"}]

                    else:
                        current_mnth += 1
                        your_next_month_emi_date = str(my_emi_date[0]) + '-' + str(current_mnth) + '-' + str(current_yr)
                        data_item = [{
                            'type': 'text',
                            'sequence': '',
                            "value": f"Your next EMI date will be on : {your_next_month_emi_date}"
                        }]

                        # updated_date = f
                        data.update_one(
                            {"username": data1["username"]},
                            {"$set": {"emi_date": your_next_month_emi_date}})

                        # current_mnth = 13
                        if current_mnth == 13:
                            current_mnth = 1
                            current_yr += 1
                            your_next_yr_emi_date = str(my_emi_date[0]) + '-' + str(current_mnth) + '-' + str(
                                current_yr)
                            data_item = [{
                                'type': 'text',
                                'sequence': '',
                                "value": f"Your next EMI date will be on : {your_next_yr_emi_date}"
                            }]

                            data.update_one(
                                {"username": data1["username"]},
                                {"$set": {"emi_date": str(your_next_yr_emi_date)}})

                return JsonResponse(data_item, safe=False)


@csrf_exempt
def amount_validator(request):
    import re
    total = []
    data1 = JSONParser().parse(request)
    res1 = " ".join(re.findall("[a-zA-Z]+", data1["amount"]))
    res2 = " ".join(re.findall(r'\d+', data1["amount"]))
    # [int(ini_string) for s in ini_string.split() if ini_string.isdigit()]
    # print ("string result: ",str(res1))
    # res3 = int(res2)
    # print ("digit result: ",res3)
    # print(type(k))
    # print(type(res3))
    # output = ""
    if res1.lower() == "k" or res1.lower() == "thousand":
        res3 = int(res2)
        k = 1000
        final = res3 * int(k)
        total.append((final))
        output = "yes"

    elif res1.lower() == "lakh" or res1.lower() == "lac":
        res3 = int(res2)
        lakh = 100000
        final = res3 * int(lakh)
        total.append(final)
        output = "yes"

    elif data1["amount"] == res2:
        total.append(res2)
        output = "yes"

    elif data1["amount"] == " ":
        output = "no"

    else:
        output = "no"

    return HttpResponse(output)

################## NBFC BOT#####END##############

##############################################
#### Nella Bot Services ##### Start###
@csrf_exempt
def email_sender(request):
    data = JSONParser().parse(request)

    email_id = []
    for k, v in data.items():

        if k == "email":
            email_id.append(v)

        # elif k == "nominee_email":
        #     email_id.append(v)

    Subject = "****Job Mail****"

    Message = """

Dear Candidate, 

                We acknowledge receipt of your resume and application for a position at Nell Infotech Pvt. Ltd. and sincerely appreciate your interest in our company.
                We will screen all applicants and select candidates whose qualifications seem to meet our needs. We will carefully consider your application during the 
                initial screening and will contact you if you are selected to continue in the recruitment process. 
                We wish you every success.


Regards,

Nell Infotech Pvt. Ltd.
Office no.2, 2nd floor,
Sahyadri House
bavdhan, Pune - 411021
Mobile: 9850088916, 9890575963
Email: connect@nellinfotech.com
       sheetal.jadhav@nellinfotech.com

"""
    send_mail(Subject, Message, settings.EMAIL_HOST_USER, email_id)

    name = []
    for k, v in data.items():

        if k == "text":
            name.append(v)

    mobile = []
    for k, v in data.items():

        if k == "mobile_no":
            mobile.append(v)

    Subject1 = "****Nell Bot : Resume****"

    Message1 = """

    Respected HR, 

                    The candidate {0} has successfully registered at Nell Infotech Pvt. Ltd. looking for job openings with his/her mail id
                    {1} and contact number {2}.


    Thank you,

    Name: {0}
    Email: {1}
    Contact: {2}




    """.format(name[0], email_id[0], mobile[0])

    mail = ["connect@nellinfotech.com"]
    # mail = ["dnyanesh.bhujbal11@gmail.com"]
    send_mail(Subject1, Message1, settings.EMAIL_HOST_USER, mail)
    # Message1.attach_file('http://ec2-18-218-142-38.us-east-2.compute.amazonaws.com:8080/NELL_BOT/media/pdf/invoice.pdf')
    #
    # msg = EmailMessage('****attachment****', 'Hi, This is nell infotech', 'acm15aug@gmail.com',
    #                    ['samarthsami120@email.com'])
    # msg.content_subtype = "html"
    # msg.attach_file("E:/SaM/NellaDEV_Core/FAQ/abc.pdf")
    # msg.send()

    con_dict = [{
        'type': 'text',
        'sequence': '',
        "value": "Thanks for applying at Nell Infotech. We will contact you soon."

    }]
    return JsonResponse(con_dict, safe=False)


@csrf_exempt
def email_query(request):
    data = JSONParser().parse(request)

    email_id = []
    for k, v in data.items():

        if k == "email":
            email_id.append(v)

    Subject = "****Query Mail****"

    Message = """

Dear Candidate, 

                Thank you so much for your query. We will contact you soon.

Regards,

Nell Infotech Pvt. Ltd.
Office no.2, 2nd floor,
Sahyadri House
bavdhan, Pune - 411021
Mobile: 9850088916, 9890575963
Email: connect@nellinfotech.com
       sheetal.jadhav@nellinfotech.com

"""
    send_mail(Subject, Message, settings.EMAIL_HOST_USER, email_id)
    # con_dict = "mail sent successfully. ."

    name = []
    for k, v in data.items():

        if k == "text":
            name.append(v)

    mobile = []
    for k, v in data.items():

        if k == "mobile_no":
            mobile.append(v)

    query_text = []
    for k, v in data.items():

        if k == "query":
            query_text.append(v)

    Subject1 = "****Nell Bot : Enquiry****"

    Message1 = """

        Respected HR, 

                        A person {0} has some queries: "{3}." sent by his/her email id {1} and contact number: {2}.


        Thank you,

        Name: {0}
        Email: {1}
        Contact: {2}




        """.format(name[0], email_id[0], mobile[0], query_text[0])

    mail = ["connect@nellinfotech.com"]

    send_mail(Subject1, Message1, settings.EMAIL_HOST_USER, mail)

    con_dict = [{
        'type': 'text',
        'sequence': '',
        "value": "Thanks for your query. We will contact you soon."

    }]
    return JsonResponse(con_dict, safe=False)


@csrf_exempt
def request_demo(request):
    # import pdb
    # pdb.set_trace()
    data = JSONParser().parse(request)

    email_id = []
    demo_text = []
    for k, v in data.items():

        if k == "email":
            email_id.append(v)

        if k == "demo":
            demo_text.append(v)

        # elif k == "nominee_email":
        #     email_id.append(v)

    Subject = "****Demo Mail****"

    Message = """

Dear Candidate, 

                Thank you for your interest in chats bots. We will contact you soon.

Regards,

Nell Infotech Pvt. Ltd.
Office no.2, 2nd floor,
Sahyadri House
bavdhan, Pune - 411021
Mobile: 9850088916, 9890575963
Email: connect@nellinfotech.com
       sheetal.jadhav@nellinfotech.com

""".format(demo_text[0])
    send_mail(Subject, Message, settings.EMAIL_HOST_USER, email_id)
    # con_dict = "mail sent successfully. ."

    name = []
    for k, v in data.items():

        if k == "text":
            name.append(v)

    mobile = []
    for k, v in data.items():

        if k == "mobile_no":
            mobile.append(v)

    Subject1 = "****Nell Bot : Request Demo****"

    Message1 = """

        Respected HR, 

                        A person {0} may need relevance information about "{3}", interest sent by his/her email id {1} and contact number: {2}.


        Thank you,

        Name: {0}
        Email: {1}
        Contact: {2}




        """.format(name[0], email_id[0], mobile[0], demo_text[0])

    mail = ["connect@nellinfotech.coms"]

    send_mail(Subject1, Message1, settings.EMAIL_HOST_USER, mail)

    con_dict = [{
        'type': 'text',
        'sequence': '',
        "value": "Thank you for your interest. We will contact you soon."

    }]
    return JsonResponse(con_dict, safe=False)
###################################END ############################


##############################################################
########################## Sales force Service#########
@csrf_exempt
def sales_force_email_service(request):
    import email, smtplib, ssl
    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    para = JSONParser().parse(request)

    # para = {
    #     "username": "admin",
    #     #"migration_type": "pilot rollout",
    #     "upload_flag": "yes",
    #     "upload_file_loc": "C:\\Program Files\\Apache Software Foundation\\Tomcat 9.0\\webapps\\NELL_BOT\\media\\pdf\\nell_bot",
    #     #"key_features_aware": "yes",
    #     #"lightning_experience": "yes",
    #     #"readiness_check": "yes",
    #     #"upload_doc": "D://abc.xlsx,D://xyz.csv",
    #     #"company_name": "test",
    #     #"email": "acm_test@gmail.com",
    #     "user_id": "yjmk7nbt4e1mshisvsd3x3k88nucwe7f",
    #     #"unsupported_editions": "no",
    #     #"lightning_migration": "abc_test",
    #     #"active_user": "120",
    #     "action_url": "http://ec2-18-218-142-38.us-east-2.compute.amazonaws.com:8080/Salesforce-Services/saveMigrationAssistant",
    #     "triggerName": "pilot_task"
    # }

    ############## Find a key ####
    if 'company_name' in para:
        company_name_0 = para['company_name']
    else:
        company_name_0 = "NA"

    if 'email' in para:
        email_1 = para['email']
    else:
        email_1 = "NA"

    if 'active_user' in para:
        active_user_2 = para['active_user']
    else:
        active_user_2 = "NA"

    if 'migration_type' in para:
        migration_type_3 = para['migration_type']
    else:
        migration_type_3 = "NA"

    if 'key_features_aware' in para:
        aware_abt_feature_lighting_exp_4 = para['key_features_aware']
    else:
        aware_abt_feature_lighting_exp_4 = "NA"

    if 'unsupported_editions' in para:
        unsupported_edi_5 = para['unsupported_editions']
    else:
        unsupported_edi_5 = "NA"

    if 'lightning_experience' in para:
        aware_lighting_transition_6 = para['lightning_experience']
    else:
        aware_lighting_transition_6 = "NA"

    if 'readiness_check' in para:
        readiness_chk_7 = para['readiness_check']
    else:
        readiness_chk_7 = "NA"

    if 'lightning_migration' in para:
        sales_force_edi_for_ligt_8 = para['lightning_migration']
    else:
        sales_force_edi_for_ligt_8 = "NA"

    ############## End Find Key ########################

    subject = "SalesForce Lightning Migration Assistant Survey"
    body = f'''Migration assistant survey from.
            Company Name : {company_name_0}
            Email : {email_1}

            Details-

            Active users : {active_user_2}
            Migration type : {migration_type_3}
            Aware about features of Lightning Experience : {aware_abt_feature_lighting_exp_4}
            Unsupported edition : {unsupported_edi_5}
            Aware about lightning experience transition assistant : {aware_lighting_transition_6}
            Readiness check : {readiness_chk_7}
            Salesforce edition for lightning migration :{sales_force_edi_for_ligt_8}'''
    # para['readiness_check']
    sender_email = "nell.paresh@gmail.com"
    # receiver_email = "shamali.jagtap7@gmail.com","priyankas.light@gmail.com","bolt.today19@gmail.com","shejad@gmail.com","karbhariravi@gmail.com"
    receiver_email = ['acm15aug@gmail.com', 'shamali.jagtap7@gmail.com', 'priyankas.light@gmail.com',
                      'bolt.today19@gmail.com', 'shejad@gmail.com', 'karbhariravi@gmail.com']
    rec = ','.join(receiver_email)
    password = "Test@123"

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = rec
    message["Subject"] = subject
    # message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    # filename = "document.pdf"  # In same directory as script

    ################### Multi/Single Attachments##################
    ################################################33
    if 'upload_doc' in para:
        all_upload_doc_1 = para['upload_doc']
        all_upload_doc = all_upload_doc_1.replace("//", "/")
        files = all_upload_doc.split(",")

        ##files=['document.pdf']

        from email.mime.application import MIMEApplication
        ############ Sending Multiple Attchment########
        for f in files:  # add files to the message
            # dir_path = "G:/test_runners/selenium_regression_test_5_1_1/TestReport"
            # file_path = os.path.join(dir_path, f)
            file_path = os.path.join(f)
            attachment = MIMEApplication(open(file_path, "rb").read(), _subtype="txt")
            attachment.add_header('Content-Disposition', 'attachment', filename=f)
            message.attach(attachment)

    ###############################################################222222222222222222

    #########################################################2222222222222

    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)

    ####################### Save Data To MongoDB ####################
    from pymongo import MongoClient
    conn = MongoClient()
    # database
    db = conn.bot
    # Created or Switched to collection names: my_gfg_collection
    collection = db.sales_force_survey
    rec_id1 = collection.insert_one(para)
    # print("Data inserted with record ids", rec_id1)
    ######################## End Save Data ###################

    con_dict = [{
        'type': 'text',
        'sequence': '1',
        "value": "Thanks for submitting details our team will get back to you."

    }]
    return JsonResponse(con_dict, safe=False)
#####################################################end
######################################################################





########### ################## ################## ################## ##################


##### HomeSampleCollectionRMBot Get task by user Sevice #####
###################################################################

@csrf_exempt
def hscrmb_getTaskByUser(request):
    # import pdb
    # pdb.set_trace()
    json_data = JSONParser().parse(request)
    name = []
    data_item = []
    for k, v in json_data.items():
        if k == "username":
            name.append(v)
        patient = [
            {
                "title": "Home Collection Request",
                "task": "#redirect-HomeCollectionRequest",
                "link": "",
                "utterance": "Home Collection Request",
                "recomend_flag": ""
            },
            {
                "title": "View Home Collection Request Status",
                "task": "#redirect-ViewHomeCollectionRequestStatus",
                "link": "",
                "utterance": "I want View my Home collection Request Status",
                "recomend_flag": ""
            }
        ]

        admin = [
            {
                "title": "Assign Collection Request",
                "task": "#redirect-AssignCollectionRequest",
                "link": "",
                "utterance": "Assign Collection Request",
                "recomend_flag": ""
            },
            {
                "title": "View Collection Request",
                "task": "#redirect-ViewCollectionRequest",
                "link": "",
                "utterance": "View Collection Request",
                "recomend_flag": ""
            },
            {
                "title": "Create Home Collection Request",
                "task": "#redirect-CreateHomeCollectionRequest",
                "link": "",
                "utterance": "Create Home Collection Request",
                "recomend_flag": ""
            },
            {
                "title": "Update Collection Request Status",
                "task": "#redirect-UpdateCollectionRequestStatus",
                "link": "",
                "utterance": "Update Collection Request Status",
                "recomend_flag": ""
            }
        ]

        field_agent = [
            {
                "title": "View Assigned Request",
                "task": "#redirect-ViewAssignedRequest",
                "link": "",
                "utterance": "View Assigned Request",
                "recomend_flag": ""
            },
            {
                "title": "Update Request Status",
                "task": "#redirect-UpdateRequestStatus",
                "link": "",
                "utterance": "Update Request Status",
                "recomend_flag": ""
            }
        ]

        if name[0] == "admin":
            data_item = patient
        elif name[0] == "a":
            data_item = admin
        elif name[0] == "a":
            data_item = field_agent

    return JsonResponse(data_item, safe=False)




####################### HomeSampleCollectionRMBot hscrmb_task_action_service ##############################



@csrf_exempt
def hscrmb_task_action_servic(request):
    # import pdb
    # pdb.set_trace()
    json_data = JSONParser().parse(request)
    from pymongo import MongoClient
    mongo_conn = MongoClient()
    # database
    db = mongo_conn["HomeSampleCollectionRMBot"]
    col = db.hscrmb_patient_details_col


############################ Generating patient Id ##########3
    ###################################

    mydoc = col.find({"patientId": {"$exists": True}})
    num = []
    for x in mydoc:
        num.append(int(x["patientId"]))
    patientId = max(num) + 1
    print("patientId --->>>", patientId)

    mydoc1 = col.find({"Status": {"$exists": True}})
    num1 = []
    for x in mydoc1:
        num1.append((x["Status"]))
    Status = "Pending"

    my_data = {'patient_name': json_data['patient_name'], 'patient_email': json_data['patient_email'],
               'patient_contact_number': str(json_data['patient_contact_number']), 'patient_gender': json_data['patient_gender'],
               'Appointment_date': json_data['Appointment_date'],'patient_address': json_data['patient_address'],
               'patientId': str(patientId), 'Status': str(Status)}
    col.insert(my_data)

    con_dict = [{
        'type': 'text',
        'sequence': '',
        "value": "Data Submitted Successfully, Thank You..."

    }]

    return JsonResponse(con_dict, safe=False)



##### HomeSampleCollectionRMBot Get task by user Sevice #####
###################################################################

@csrf_exempt
def hscrmb_getYesNoByUser(request):
    # import pdb
    # pdb.set_trace()
    json_data = JSONParser().parse(request)
    name = []
    data_item = []
    for k, v in json_data.items():
        if k == "username":
            name.append(v)
        yes_no_recommendations = [
            {
                "title": "Yes",
                "task": "",
                "link": "",
                "utterance": "Yes",
                "recomend_flag": ""
            },
            {
                "title": "No",
                "task": "",
                "link": "",
                "utterance": "No",
                "recomend_flag": ""
            }
        ]


        if name[0] == "admin":
            data_item = yes_no_recommendations

    return JsonResponse(data_item, safe=False)


@csrf_exempt
def hscrmb_getDetailsByUser(request):
    json_data = JSONParser().parse(request)
    mongo_conn = pymongo.MongoClient()
    db = mongo_conn["HomeSampleCollectionRMBot"]
    col = db.hscrmb_patient_details_col
    hscrmb_patient_details_col = []

    for i in col.find({"Appointment_date": str(json_data["date"])}):
        print("i->", i)

        hscrmb_patient_details_col.append(i)

    final_dict = hscrmb_patient_details_col
    print("final_dict->", final_dict)

    for x in hscrmb_patient_details_col:
        del (x['_id'])
        x.update({'identifier': x['patientId']})
    final_dict = hscrmb_patient_details_col
    print("final_dict-->>", final_dict)
    # for i in col.find():
    data = []
    for i in col.find({"Appointment_date": str(json_data["date"])}):
        print("i->", i)

        data = [
            {
                "type": "text",
                "sequence": "1",
                "value": f"Here is the details of your current order",
                "displayMessage": None
            },
            {
                "type": "slider",
                "sequence": "2",
                "value": None,
                "displayMessage": None,
                "title": [
                    {
                        "name": "patient_name",
                        "position": "1"
                    },
                    {
                        "name": "patient_email",
                        "position": "2"
                    }
                    ,
                    {
                        "name": "patient_contact_number",
                        "position": "3"
                    }
                    ,
                    {
                        "name": "patient_gender",
                        "position": "4"
                    }
                    ,
                    {
                        "name": "Appointment_date",
                        "position": "5"
                    }
                    ,
                    {
                        "name": "patient_address",
                        "position": "6"
                    }
                    ,
                    {
                        "name": "Status",
                        "position": "7"
                    }
                    ,
                    {
                        "name": "patientId",
                        "position": "8"
                    }
                ],

                "data_items": final_dict
            }
        ]

    if len(data) == 0:
        data = [
            {
                "type": "text",
                "sequence": "",
                "value": f"No Requests for today, Thank You...",

            }]
    return JsonResponse(data, safe=False)

@csrf_exempt
def hscrmb_AssignStatus(request):
    # import pdb
    # pdb.set_trace()
    json_data = JSONParser().parse(request)
    print("json_data===>", json_data)
    from pymongo import MongoClient
    mongo_conn = MongoClient()
    # database
    db = mongo_conn["HomeSampleCollectionRMBot"]
    patient_details_col = db.hscrmb_patient_details_col

    for i in patient_details_col.find():
        if i['Status'] == "Pending":
            patient_details_col.update({"patientId": str(json_data["planId"])},
                                       {"$set": {"Status": "Assigned to Filed Agent"}})

            data = [{
                'type': 'text',
                'sequence': '',
                "value": f"Status : Assigned successfully...."

            }]

            return JsonResponse(data, safe=False)

@csrf_exempt
def hscrmb_testSlider(request):

    import pdb
    #pdb.set_trace()
    data = JSONParser().parse(request)
    mongo_conn = pymongo.MongoClient()
    db = mongo_conn["HomeSampleCollectionRMBot"]
    data = db.hscrmb_patient_details_col
    hscrmb_patient_details_col = []

    for i in data.find():
        print("i->",i)
        hscrmb_patient_details_col.append(i)
#         [{
# 	"_id" : ObjectId("611d8acd2107680998e8d21e"),
# 	"username" : "admin",
# 	"Name" : "sudarshan",
# 	"Email" : "s@12",
# 	"mobile" : 1212121212,
# 	"Gender" : "male",
# 	"date" : "21/08/2021",
# 	"user_id" : "pwb7jd3sobhav3zorbty7gxig31ak6mx",
# 	"triggerName" : "CreateHomeCollectionRequest"
# }]

    final_dict = hscrmb_patient_details_col
    print("final_dict->",final_dict)


    for x in hscrmb_patient_details_col:
        del (x['_id'])
        x.update({'identifier': x['patientId']})
    final_dict = hscrmb_patient_details_col

    # extracting data in json format
    data = [
        {
            "type": "text",
            "sequence": "1",
            "value": f"Here is the details of your current order",
            "displayMessage": None
        },
        {
            "type": "slider",
            "sequence": "2",
            "value": None,
            "displayMessage": None,
            "title": [
                {
                    "name": "patient_name",
                    "position": "1"
                },
                {
                    "name": "patient_email",
                    "position": "2"
                }
                ,
                {
                    "name": "patient_contact_number",
                    "position": "3"
                }
                ,
                {
                    "name": "patient_gender",
                    "position": "4"
                }
                ,
                {
                    "name": "Appointment_date",
                    "position": "5"
                }
                ,
                {
                    "name": "patient_address",
                    "position": "6"
                }
                ,
                {
                    "name": "Status",
                    "position": "7"
                }
                ,
                {
                    "name": "patientId",
                    "position": "8"
                }
            ],

            "data_items": final_dict
        }
    ]



    return JsonResponse(data, safe=False)


##########   fetch data      ##########
###################################
#################################

@csrf_exempt
def hscrmb_fetch(request):
    import pdb
    # pdb.set_trace()
    data = JSONParser().parse(request)
    mongo_conn = pymongo.MongoClient()
    db = mongo_conn["HomeSampleCollectionRMBot"]
    data = db.hscrmb_patient_details_col
    hscrmb_patient_details_col = []

    for i in data.find():
        print("i->", i)
        hscrmb_patient_details_col.append(i)

    final_dict = hscrmb_patient_details_col
    print("final_dict->", final_dict)

    for x in hscrmb_patient_details_col:
        del (x['_id'])
        x.update({'identifier': x['patientId']})
    final_dict = hscrmb_patient_details_col

    # extracting data in json format
    data = [
        {
            "type": "text",
            "sequence": "1",
            "value": f"Here is the details of your current order",
            "displayMessage": None
        },
        {
            "type": "slider",
            "sequence": "2",
            "value": None,
            "displayMessage": None,
            "title": [
                {
                    "name": "patient_name",
                    "position": "1"
                },
                {
                    "name": "patient_email",
                    "position": "2"
                }
                ,
                {
                    "name": "patient_contact_number",
                    "position": "3"
                }
                ,
                {
                    "name": "patient_gender",
                    "position": "4"
                }
                ,
                {
                    "name": "Appointment_date",
                    "position": "5"
                }
                ,
                {
                    "name": "patient_address",
                    "position": "6"
                }
                ,
                {
                    "name": "Status",
                    "position": "7"
                }
                ,
                {
                    "name": "patientId",
                    "position": "8"
                }
            ],

            "data_items": final_dict
        }
    ]

    return JsonResponse(data, safe=False)


@csrf_exempt
def hscrmb_fetchOne(request):
    # import pdb
    # pdb.set_trace()
    json_data = JSONParser().parse(request)
    mongo_conn = pymongo.MongoClient()
    db = mongo_conn["HomeSampleCollectionRMBot"]
    col = db.hscrmb_patient_details_col
    hscrmb_patient_details_col = []

    for i in col.find({"patient_contact_number": str(json_data["patient_contact_number"])}):
           print("i->", i)

           hscrmb_patient_details_col.append(i)

    final_dict = hscrmb_patient_details_col
    print("final_dict->", final_dict)

    for x in hscrmb_patient_details_col:
        del (x['_id'])
        x.update({'identifier': x['patientId']})
    final_dict = hscrmb_patient_details_col
    print("final_dict-->>", final_dict)
    # for i in col.find():
    data = []
    for i in col.find({"patient_contact_number": str(json_data["patient_contact_number"])}):
        print("i->", i)

        data = [
            {
                "type": "text",
                "sequence": "1",
                "value": f"Here is the details of your current order",
                "displayMessage": None
            },
            {
                "type": "slider",
                "sequence": "2",
                "value": None,
                "displayMessage": None,
                "title": [
                    {
                        "name": "patient_name",
                        "position": "1"
                    },
                    {
                        "name": "patient_email",
                        "position": "2"
                    }
                    ,
                    {
                        "name": "patient_contact_number",
                        "position": "3"
                    }
                    ,
                    {
                        "name": "patient_gender",
                        "position": "4"
                    }
                    ,
                    {
                        "name": "Appointment_date",
                        "position": "5"
                    }
                    ,
                    {
                        "name": "patient_address",
                        "position": "6"
                    }
                    ,
                    {
                        "name": "Status",
                        "position": "7"
                    }
                    ,
                    {
                        "name": "patientId",
                        "position": "8"
                    }
                ],

                "data_items": final_dict
            }
        ]

    if len(data) == 0:
            data = [
            {
                "type": "text",
                "sequence": "",
                "value": f"Invaild number",

            }]
    return JsonResponse(data, safe=False)

@csrf_exempt
def hscrmb_fetchUpdate(request):
    import pdb
    # pdb.set_trace()
    data = JSONParser().parse(request)
    mongo_conn = pymongo.MongoClient()
    db = mongo_conn["HomeSampleCollectionRMBot"]
    data = db.hscrmb_patient_details_col
    hscrmb_patient_details_col = []

    for i in data.find():
        print("i->", i)
        hscrmb_patient_details_col.append(i)

    final_dict = hscrmb_patient_details_col
    print("final_dict->", final_dict)

    for x in hscrmb_patient_details_col:
        del (x['_id'])
        x.update({'identifier': x['patientId']})
    final_dict = hscrmb_patient_details_col

    # extracting data in json format
    data = [
        {
            "type": "text",
            "sequence": "1",
            "value": f"Here is the details of your current order",
            "displayMessage": None
        },
        {
            "type": "slider",
            "sequence": "2",
            "value": None,
            "displayMessage": None,
            "title": [
                {
                    "name": "patient_name",
                    "position": "1"
                },
                {
                    "name": "patient_email",
                    "position": "2"
                }
                ,
                {
                    "name": "patient_contact_number",
                    "position": "3"
                }
                ,
                {
                    "name": "patient_gender",
                    "position": "4"
                }
                ,
                {
                    "name": "Appointment_date",
                    "position": "5"
                }
                ,
                {
                    "name": "patient_address",
                    "position": "6"
                }
                ,
                {
                    "name": "Status",
                    "position": "7"
                }
                ,
                {
                    "name": "patientId",
                    "position": "8"
                }
            ],

            "data_items": final_dict
        }
    ]

    return JsonResponse(data, safe=False)

@csrf_exempt
def hscrmb_UpdateStatus(request):
    # import pdb
    # pdb.set_trace()
    json_data = JSONParser().parse(request)
    print("json_data===>", json_data)
    from pymongo import MongoClient
    mongo_conn = MongoClient()
    # database
    db = mongo_conn["HomeSampleCollectionRMBot"]
    patient_details_col = db.hscrmb_patient_details_col

    for i in patient_details_col.find():
        if i['Status'] == "Sample collected":
            patient_details_col.update({"patientId": str(json_data["planId"])},
                                       {"$set": {"Status": "Report Ready"}})
            data = [{
                'type': 'text',
                'sequence': '',
                "value": f"Status : updated successfully..."

            }]

            return JsonResponse(data, safe=False)
        # if i['Status'] == "pending":
        #     patient_details_col.update({"patientId": str(json_data["planId"])},
        #                                {"$set": {"Status": "Assigned to Filed Agent"}})
        #     data = [{
        #         'type': 'text',
        #         'sequence': '',
        #         "value": f"Status : Assigned successfully...."
        #
        #     }]


        # elif i['Status'] == "Assigned to Filed Agent":
        #     patient_details_col.update({"patientId": str(json_data["planId"])},
        #                                {"$set": {"Status": "Sample collected"}})
        #     data = [{
        #         'type': 'text',
        #         'sequence': '',
        #         "value": f"Status : updated successfully..."
        #
        #     }]
        #
        # elif i['Status'] == "Sample collected":
        #     patient_details_col.update({"patientId": str(json_data["planId"])},
        #                                {"$set": {"Status": "Report Ready"}})
        #     data = [{
        #         'type': 'text',
        #         'sequence': '',
        #         "value": f"Status : updated successfully..."
        #
        #     }]





@csrf_exempt
def hscrmb_ViewStatus(request):
    json_data = JSONParser().parse(request)
    mongo_conn = pymongo.MongoClient()
    db = mongo_conn["HomeSampleCollectionRMBot"]
    col = db.hscrmb_patient_details_col
    hscrmb_patient_details_col = []

    for i in col.find({"patientId": str(json_data["patientId"])}):
        print("i->", i)
        hscrmb_patient_details_col.append(i)

    final_dict = hscrmb_patient_details_col
    print("final_dict->", final_dict)


    data = []
    for i in col.find({"patientId": str(json_data["patientId"])}):
        print("i->", i)

        name = i["patient_name"]
        status = i["Status"]
        patientId = i["patientId"]
        data = [
            {
                'type': 'text',
                'sequence': '',
                "value": f"<b> Patient Name --> {name} <br> Status --> {status}, <br> Patient Id --> {patientId}</b>"
            }
        ]

    if len(data) == 0:
            data = [
            {
                "type": "text",
                "sequence": "",
                "value": f"Invaild Patient Id ",

            }]
    return JsonResponse(data, safe=False)

@csrf_exempt
def hscrmb_View_Field_Agent(request):
    json_data = JSONParser().parse(request)
    mongo_conn = pymongo.MongoClient()
    db = mongo_conn["HomeSampleCollectionRMBot"]
    col = db.hscrmb_patient_details_col
    hscrmb_patient_details_col = []
    for i in col.find({"Status": "Assigned to Filed Agent"}):
           print("i->", i)

           hscrmb_patient_details_col.append(i)

    final_dict = hscrmb_patient_details_col
    print("final_dict->", final_dict)

    for x in hscrmb_patient_details_col:
        del (x['_id'])
        x.update({'identifier': x['patientId']})
    final_dict = hscrmb_patient_details_col
    print("final_dict-->>", final_dict)
    # for i in col.find():
    data = []
    for i in col.find({"Status": "Assigned to Filed Agent"}):
        print("i->", i)

        data = [
            {
                "type": "text",
                "sequence": "1",
                "value": f"Here is the details of your current order",
                "displayMessage": None
            },
            {
                "type": "slider",
                "sequence": "2",
                "value": None,
                "displayMessage": None,
                "title": [

                    {
                        "name": "patient_name",
                        "position": "1"
                    },
                    {
                        "name": "patient_email",
                        "position": "2"
                    }
                    ,
                    {
                        "name": "patient_contact_number",
                        "position": "3"
                    }
                    ,
                    {
                        "name": "patient_gender",
                        "position": "4"
                    }
                    ,
                    {
                        "name": "Appointment_date",
                        "position": "5"
                    }
                    ,
                    {
                        "name": "patient_address",
                        "position": "6"
                    }
                    ,
                    {
                        "name": "Status",
                        "position": "7"
                    }
                    ,
                    {
                        "name": "patientId",
                        "position": "8"
                    }
                ],

                "data_items": final_dict
            }
        ]

    if len(data) == 0:
            data = [
            {
                "type": "text",
                "sequence": "",
                "value": f"No Requests for today, Thank You",

            }]
    return JsonResponse(data, safe=False)

@csrf_exempt
def hscrmb_Update_View_Field_Agent(request):
    json_data = JSONParser().parse(request)
    mongo_conn = pymongo.MongoClient()
    db = mongo_conn["HomeSampleCollectionRMBot"]
    col = db.hscrmb_patient_details_col
    hscrmb_patient_details_col = []
    for i in col.find({"Status": "Assigned to Filed Agent"}):
           print("i->", i)

           hscrmb_patient_details_col.append(i)

    final_dict = hscrmb_patient_details_col
    print("final_dict->", final_dict)

    for x in hscrmb_patient_details_col:
        del (x['_id'])
        x.update({'identifier': x['patientId']})
    final_dict = hscrmb_patient_details_col
    print("final_dict-->>", final_dict)
    # for i in col.find():
    data = []
    for i in col.find({"Status": "Assigned to Filed Agent"}):
        print("i->", i)

        data = [
            {
                "type": "text",
                "sequence": "1",
                "value": f"Here is the details of your current order",
                "displayMessage": None
            },
            {
                "type": "slider",
                "sequence": "2",
                "value": None,
                "displayMessage": None,
                "title": [

                    {
                        "name": "patient_name",
                        "position": "1"
                    },
                    {
                        "name": "patient_email",
                        "position": "2"
                    }
                    ,
                    {
                        "name": "patient_contact_number",
                        "position": "3"
                    }
                    ,
                    {
                        "name": "patient_gender",
                        "position": "4"
                    }
                    ,
                    {
                        "name": "Appointment_date",
                        "position": "5"
                    }
                    ,
                    {
                        "name": "patient_address",
                        "position": "6"
                    }
                    ,
                    {
                        "name": "Status",
                        "position": "7"
                    }
                    ,
                    {
                        "name": "patientId",
                        "position": "8"
                    }
                ],

                "data_items": final_dict
            }
        ]

    if len(data) == 0:
            data = [
            {
                "type": "text",
                "sequence": "",
                "value": f"No Requests for today, Thank You",

            }]
    return JsonResponse(data, safe=False)


@csrf_exempt
def hscrmb_Update_Field_Agent(request):
    # import pdb
    # pdb.set_trace()
    json_data = JSONParser().parse(request)
    print("json_data===>", json_data)
    from pymongo import MongoClient
    mongo_conn = MongoClient()
    # database
    db = mongo_conn["HomeSampleCollectionRMBot"]
    patient_details_col = db.hscrmb_patient_details_col

    for i in patient_details_col.find():
        if i['Status'] == "Assigned to Filed Agent":
            patient_details_col.update({"patientId": str(json_data["planId"])},
                                       {"$set": {"Status": "Sample collected"}})

            data = [
                {
                    'type': 'text',
                    'sequence': '',
                    "value": f"Status : Updated successfully...."

                }
            ]


            return JsonResponse(data, safe=False)


@csrf_exempt
def hscrmb_Update_YesNo_Field_Agent(request):
    # import pdb
    # pdb.set_trace()
    json_data = JSONParser().parse(request)
    print("json_data===>", json_data)
    from pymongo import MongoClient
    mongo_conn = MongoClient()
    # database
    db = mongo_conn["HomeSampleCollectionRMBot"]
    patient_details_col = db.hscrmb_patient_details_col
    data_items = []
    if json_data["comment"] == "Yes".lower():
        my_data = {'comment': json_data['comment']}
        patient_details_col.insert(my_data)
        data = {
                'type': 'text',
                'sequence': '',
                "value": f" Comment Added  successfully...."

            }


        data_items.append(data)
    elif json_data["comment"] == "No".lower():
        data = {
                'type': 'text',
                'sequence': '',
                "value": f"Thank You"

            }
        data_items.append(data)

    return JsonResponse(data_items, safe=False)

##############
@csrf_exempt
def hscrmb_Update_Yes_Field_Agent(request):
    # import pdb
    # pdb.set_trace()
    json_data = JSONParser().parse(request)
    print("json_data===>", json_data)
    from pymongo import MongoClient
    mongo_conn = MongoClient()
    # database
    db = mongo_conn["HomeSampleCollectionRMBot"]
    patient_details_col = db.hscrmb_patient_details_col

    my_data = {'comment': json_data['comment']}
    patient_details_col.insert(my_data)
    data = [
        {
            'type': 'text',
            'sequence': '',
            "value": f" Comment Added  successfully...."

        }
    ]
    return JsonResponse(data, safe=False)


@csrf_exempt
def hscrmb_Update_No_Field_Agent(request):
    # import pdb
    # pdb.set_trace()
    json_data = JSONParser().parse(request)
    print("json_data===>", json_data)
    from pymongo import MongoClient
    mongo_conn = MongoClient()
    # database
    db = mongo_conn["HomeSampleCollectionRMBot"]
    patient_details_col = db.hscrmb_patient_details_col

    data = [
        {
            'type': 'text',
            'sequence': '',
            "value": f" Thank You ...."

        }
    ]
    return JsonResponse(data, safe=False)
