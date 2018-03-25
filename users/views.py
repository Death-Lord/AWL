from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import users, forum, analyse_image, chatbot_save, vehicle
from django.core.mail import send_mail
import hashlib
from sendsms import api
from django.urls import reverse
import os

def index(request):
    try:
        user = users.objects.get(id=request.session['user_id'])
    except:
        user=NULL
    print(user)
    return render(request, 'users/index.html',{'user':user,})

def vehicles(request):
    if request.method=='POST':
        name=request.POST.get('name','')
        reg_no=request.POST.get('reg_no','')
        date=request.POST.get('date','')
        vehicle_save=vehicle(name=name, reg_no=reg_no, date=date)
        user_save = users.objects.get(id = request.session['user_id'])
        send_mail(
                'Registeration Successful',
                'Vehicle registered, its a remainder to renew your pollution certificate after 6 months',
                'skalra912@gmail.com',
                [user_save.email],
                fail_silently=False,
                )
        vehicle_save.save()
        return render(request,'users/message_display.html',{'success':'Vehicle Registered and check your maild id for more details.'})
    else:
        return render(request,'users/vehicle.html')

def display_users(request):
    user = users.objects.all()
    context = {'user':user}
    return render(request, 'users/display_users.html', context)

def display_specific_users(request,user_id):
    user = get_object_or_404(users, pk=user_id)
    context = {'user':user}
    return render(request, 'users/display_specific_users.html', context)

def display_detail(request, user_id):
    user = get_object_or_404(users, pk = user_id)
    context = {'user':user}
    return render(request, 'users/display_detail.html', context)

def register_user(request):
    if request.method=='POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        user_name = request.POST.get('user_name', '')
        password = request.POST.get('password', '')
        hash_password = hashlib.md5(password.encode())
        user_check = users.objects.filter(user_name = user_name)
        if user_check:
            context = {'error':'User name already exists please choose a new one.'}
            return render(request, 'users/message_display.html',context)
        else:
            user_check = users.objects.filter(email = email)
            if user_check:
                context = {'error':'There is an account already assosciated with the entered email.'}
                return render(request, 'users/message_display.html',context)
            else:
                send_mail(
                        'Follow the given link to register yourself',
                        'http://127.0.0.1:8000/validate_registeration/{}/{}/{}/{}/{}'.format(first_name, last_name, email, user_name, hash_password.hexdigest()),
                        'skalra912@gmail.com',
                        [email],
                        fail_silently=False,
                        )
                return render(request, 'users/message_display.html', {'message':'Check your email for further instructions'})
    else:
        return render(request,'users/register.html')

def login_user(request):
    if request.method=='POST':
        user_name = request.POST.get('user_name', '')
        password = request.POST.get('password', '')
        hash_password = hashlib.md5(password.encode())
        try:
            user_login = users.objects.get(user_name = user_name, password=hash_password.hexdigest())
            request.session['user_id'] = user_login.id
            return HttpResponseRedirect(reverse('index'))
        except:
            return render(request, 'users/message_display.html',{'error':'No User Found'})
    else:
        return render(request, 'users/login.html')

def validate_registeration(request, first_name, last_name, email, user_name, password):
    user_save = users(first_name=first_name, last_name=last_name, email = email, user_name=user_name, password=password)
    user_save.save()
    return HttpResponseRedirect(reverse('profile_pic', args=(user_save.id,)))

def profile_pic(request, user_id):
    return render(request, 'users/profile_pic.html', {'user_id':user_id})

def profile_pic_upload(request, user_id):
    if request.method=='POST':
        user_save = users.objects.get(id = user_id)
        profile_pic = request.FILES.get('profile_pic', '')
        user_save.profile_pic = profile_pic
        user_save.save()
        return render(request, 'users/message_display.html', {'success':'Profile Picture uploaded Successfully'})

def logout(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return render(request, 'users/message_display.html', {'message':'You are logged out Successfully'})
def forgot_password(request):
    if request.method=='POST':
        field1 = request.POST.get('email/user_name','')
        try:
            user = users.objects.get(email = field1)
            send_mail(
                    'Follow the given link to reset your password',
                    'http://127.0.0.1:8000/reset_password/{}'.format(user.id),
                    'skalra912@gmail.com',
                    [user.email],
                    fail_silently=False,
                    )
            return render(request, 'users/message_display.html', {'message':'Check your email for further instructions'})
        except:
            try:
                user = users.objects.get(user_name = field1)
                send_mail(
                        'Follow the given link to reset your password',
                        'http://127.0.0.1:8000/reset_password/{}'.format(user.id),
                        'skalra912@gmail.com',
                        [user.email],
                        fail_silently=False,
                        )
                return render(request, 'users/message_display.html', {'message':'Check your email for further instructions'})
            except:
                return render(request, 'users/message_display.html', {'error':'No user with entered email/username registered.'})
    else:
        return render(request, 'users/forgot_password.html')

def reset_password(request, user_id):
    if request.method == 'POST':
        password = request.POST.get('password', '')
        reenter_password = request.POST.get('reenter_password', '')
        if password == reenter_password:
            user = users.objects.get(id = user_id)
            hash_password = hashlib.md5(password.encode())
            user.password = hash_password.hexdigest()
            user.save()
            return render(request, 'users/message_display.html', {'success':'Password Changed Successfully'})
        else:
            return render(request, 'users/message_display.html', {'error':'Passwords dont match'})
    else:
        return render(request, 'users/reset_password.html', {'user_id':user_id})

def account_details(request, user_id):
    user=users.objects.get(id=user_id)
    imgurl= user.profile_pic
    img=[]
    img=str(imgurl).split('/')
    url = os.path.join(img[1],img[2])
    return render(request, 'users/account_details.html',{'baseurl':url})
def soundmeter(request):
    if request.method == 'POST':
        time = request.POST.get('time','')
        import os
        try:
            os.remove('meter.txt')
        except:
            pass
        cmd = 'soundmeter --collect --seconds {} --log meter.txt'.format(time)
        os.system(cmd)
        files = open('meter.txt', 'r')
        data_list=files.readlines()
        date = (data_list[0].split(" "))[0]
        decible_value=[]
        import datetime
        currentDT = datetime.datetime.now()
        date = str(currentDT).split(" ")[0]
        beg_time=str(currentDT).split(" ")[1]
        time = time.split(".")[0]
        for i in range(len(data_list)):
            value = ((data_list[i].split(","))[1].split(" "))[1]
            len_value=len(value)
            value=value[0:len(value)-1]
            if value =='Timeout':
                break
            decible_value.append(value)
        decible_value_int=[]
        for i in decible_value:
            decible_value_int.append(int(i))
        max_value=max(decible_value_int)
        min_value=min(decible_value_int)
        avg = sum(decible_value_int)/len(decible_value_int)
        return render(request, 'users/soundmeter.html', {'result':True, 'date':date,'beg_time':beg_time,'data':decible_value,'max':max_value,'min':min_value,'avg':avg})
    else:
        return render(request, 'users/soundmeter.html')

def forum_portal(request):
    post = forum.objects.all()
    return render(request, 'forum/forum.html',{'posts':post})

def submit_post(request):
    if request.method == 'POST':
        post = request.POST.get('post','')
        user = users.objects.get(id=request.session['user_id'])
        imgurl= user.profile_pic
        img=[]
        img=str(imgurl).split('/')
        url = os.path.join(img[1],img[2])
        name = '{} {}'.format(user.first_name, user.last_name)
        post_save=forum(post=post,user=name, url = url)
        post_save.save()
    return render(request, 'users/message_display.html',{'success':'Post Submitted Successfully'})

def chatbot(request):
    if request.method == 'POST':
        question=request.POST.get('question', '')
        user=users.objects.get(id=request.session['user_id'])
        imgurl= user.profile_pic
        img=[]
        img=str(imgurl).split('/')
        url = os.path.join(img[1],img[2])
        save = chatbot_save(message=question, by='You', url = url)
        save.save()
        import watson_developer_cloud

        # Set up Conversation service.
        conversation = watson_developer_cloud.ConversationV1(
          username = 'b3f0d60e-41c1-401b-a571-700ec98cbf85', # replace with username from service key
          password = 'vuawQL0Rx3Ve', # replace with password from service key
          version = '2017-05-26'
        )
        workspace_id = '7294a6f7-66da-438d-85f1-d1fd26bbeb23' # replace with workspace ID
          # Send message to Conversation service.
        response = conversation.message(
            workspace_id = workspace_id,
            input = {
              'text': question
            }
          )

          # If an intent was detected, print it to the console.
        if response['intents']:
            print('Detected intent: #' + response['intents'][0]['intent'])

          # Print the output from dialog, if any.
        if response['output']['text']:
            print(response['output']['text'][0])
        ans = response['output']['text'][0]
        save = chatbot_save(message=ans,by='Chatbot')
        save.save()
        data = chatbot_save.objects.all()
        return render(request, 'chatbot/chatbot.html', {'data':data})
    else:
        instance = chatbot_save.objects.all()
        instance.delete()
        return render(request,'chatbot/chatbot.html')

def air_api(request):
    if request.method == 'POST':
        city = request.POST.get('city', '')
        from geopy.geocoders import Nominatim
        geolocator = Nominatim()
        location = geolocator.geocode(city)
        import requests
        import json
        import time
        import urllib.request
        def POLLUTIONREPORT(lattitude,longitude,address):
            url="http://api.airpollutionapi.com/1.0/aqi?"
            request_url = url + "lat="+lattitude+"&"+"lon="+longitude+"&APPID="+'aqnhvq4fsvjuo36ep11tb8lg53'
            response = urllib.request.urlopen(request_url).read()
            json_obj = str(response,'utf-8')
            pollution_data = json.loads(json_obj)
            #for key,value in pollution_data['data'].items():
                #print(key,":",value)
            return{"city":address,"Quality":pollution_data['data']['text'],"Alert":pollution_data['data']['alert'],"Value":pollution_data['data']['value'],"Temperature":pollution_data['data']['temp']}
            #print("Quality :",pollution_data['data']['text'])
            #print("Alert :",pollution_data['data']['alert'])
            #print("Value :",pollution_data['data']['value'])
            #print("Temperature :",pollution_data['data']['temp'])

        report = POLLUTIONREPORT(str(location.latitude), str(location.longitude), str(city))
        for key, value in report.items():
            print(key,":",value)
        return render(request, 'air_api/air_api.html',{'data':report.items()})
    else:
        return render(request, 'air_api/air_api.html')

def upload_image(request):
    if request.method=='POST':
        image = request.FILES.get('image','')
        image_upload = analyse_image(image=image)
        image_upload.save()
        return HttpResponseRedirect(reverse('analyse_uploaded_image', args=(str(image),)))
    else:
        return render(request, 'users/upload_image.html')

def analyse_uploaded_image(request, image):
    data = analyse_image.objects.get(image='staticFiles/analyse_image/{}'.format(image))
    url = 'analyse_image/{}'.format(image)
    path = '/home/sagar/loginandregister/staticFiles/analyse_image/{}'.format(image)
    import boto3
    client=boto3.client('rekognition','us-west-2')

    with open(path, 'rb') as image:
        response = client.detect_labels(Image={'Bytes': image.read()})

    print('Detected labels in ' + path)
    labels=[]
    for label in response['Labels']:
        print (label['Name'] + ' : ' + str(label['Confidence']))
        labels.append(label['Name'])
    if 'Pollution' in labels and 'Factory' in labels:
        data.pollution_data='Air Pollution'
        data.save()
        pollution='Air Pollution'
        return render(request, 'users/result_image.html',{'pollution':pollution})
    if 'Pollution' in labels and 'Water' in labels:
        data.pollution_data='Water Pollution'
        data.save()
        pollution='Water Pollution'
        return render(request, 'users/result_image.html',{'pollution':pollution})
